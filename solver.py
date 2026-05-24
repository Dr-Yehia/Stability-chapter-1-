from dataclasses import dataclass
from typing import List
import math


@dataclass
class DerivationStep:
    title: str
    expression: str
    result: str | None = None


@dataclass
class SolveResult:
    detected_system: str
    pcr: float
    critical_equation: str
    steps: List[DerivationStep]
    method: str


def _find_node(nodes: list[dict], nid: int) -> dict:
    for n in nodes:
        if int(n["Node_ID"]) == nid:
            return n
    raise ValueError(f"Node {nid} not found")


def solve_from_tables(nodes: list[dict], members: list[dict], loads: list[dict]) -> SolveResult:
    """Energy-approach-only solver for current Chapter-1 benchmark bar-spring systems."""
    active_members = [m for m in members if str(m.get("Active", "Yes")).lower() == "yes"]
    if len(active_members) != 1:
        raise ValueError("Current solver expects exactly one active member (single rigid bar benchmark).")

    m = active_members[0]
    n1 = _find_node(nodes, int(m["Start_Node"]))
    n2 = _find_node(nodes, int(m["End_Node"]))

    x1, y1 = float(n1["X"]), float(n1["Y"])
    x2, y2 = float(n2["X"]), float(n2["Y"])
    L = math.hypot(x2 - x1, y2 - y1)
    if L <= 0:
        raise ValueError("Member length must be > 0")

    end_loads = [
        ld for ld in loads
        if str(ld.get("Active", "Yes")).lower() == "yes"
        and str(ld.get("Has_Load", "Yes")).lower() == "yes"
        and str(ld.get("Target_Type", "Node")) == "Node"
        and int(ld.get("Target_ID")) == int(n2["Node_ID"])
        and str(ld.get("Load_Type", "Force")) == "Force"
    ]
    if not end_loads:
        raise ValueError("Need a force at end node to define axial load direction.")

    ld = end_loads[0]
    dirx = float(ld.get("Dir_X", 0))
    diry = float(ld.get("Dir_Y", 0))
    if not (dirx < 0 and abs(diry) < 1e-12):
        raise ValueError("Current benchmark expects end force in negative global X direction.")

    k_theta_1 = float(n1.get("K_theta", 0.0)) if str(n1.get("Has_Rot_Spring", "No")).lower() == "yes" else 0.0
    k_theta_2 = float(n2.get("K_theta", 0.0)) if str(n2.get("Has_Rot_Spring", "No")).lower() == "yes" else 0.0
    k_y_2 = float(n2.get("K_y", 0.0)) if str(n2.get("Has_Vert_Spring", "No")).lower() == "yes" else 0.0

    if k_theta_1 > 0 and k_theta_2 == 0 and k_y_2 == 0:
        pcr = k_theta_1 / L
        steps = [
            DerivationStep("1) Geometry from coordinates", f"L = sqrt((x2-x1)^2 + (y2-y1)^2) = {L:.10g}"),
            DerivationStep("2) Total potential energy", "Π(θ) = U + V = 1/2·kθ·θ^2 − P·L(1−cosθ)"),
            DerivationStep("3) Equilibrium condition", "∂Π/∂θ = kθ·θ − P·L·sinθ = 0"),
            DerivationStep("4) Small-deflection form (sinθ≈θ)", "(kθ − P·L)θ = 0"),
            DerivationStep("5) Critical condition from non-trivial solution", "kθ − P·L = 0"),
            DerivationStep("6) Critical load", f"Pcr = kθ/L = {k_theta_1:.10g}/{L:.10g} = {pcr:.10g}"),
        ]
        return SolveResult("rigid_bar_rotational_spring_auto", pcr, "kθ − P·L = 0", steps, method="Energy approach only")

    if k_theta_1 == 0 and k_theta_2 == 0 and k_y_2 > 0:
        pcr = k_y_2 * L
        steps = [
            DerivationStep("1) Geometry from coordinates", f"L = sqrt((x2-x1)^2 + (y2-y1)^2) = {L:.10g}"),
            DerivationStep("2) Kinematics", "Vertical spring extension δ = L·sinθ"),
            DerivationStep("3) Total potential energy", "Π(θ) = U + V = 1/2·ky·(L·sinθ)^2 − P·L(1−cosθ)"),
            DerivationStep("4) Equilibrium condition", "∂Π/∂θ = ky·L^2·sinθ·cosθ − P·L·sinθ = 0"),
            DerivationStep("5) Small-deflection form", "(ky·L − P)·L·θ = 0"),
            DerivationStep("6) Critical condition and load", f"Pcr = ky·L = {k_y_2:.10g}×{L:.10g} = {pcr:.10g}"),
        ]
        return SolveResult("rigid_bar_translational_spring_auto", pcr, "ky·L − P = 0", steps, method="Energy approach only")

    raise ValueError("Input pattern not recognized yet for ENERGY-only solver. Use 2-node/1-member bar with either node1 rotational spring OR node2 vertical spring.")
