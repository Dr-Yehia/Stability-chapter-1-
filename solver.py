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


def _is_yes(value) -> bool:
    return str(value).strip().lower() == "yes"


def _has_node_load(loads: list[dict], node_id: int, dir_sign: int) -> bool:
    for ld in loads:
        if not _is_yes(ld.get("Active", "Yes")):
            continue
        if not _is_yes(ld.get("Has_Load", "Yes")):
            continue
        if str(ld.get("Target_Type", "Node")) != "Node":
            continue
        if int(ld.get("Target_ID")) != int(node_id):
            continue
        if str(ld.get("Load_Type", "Force")) != "Force":
            continue

        dirx = float(ld.get("Dir_X", 0))
        diry = float(ld.get("Dir_Y", 0))
        if abs(diry) > 1e-12:
            continue

        if dir_sign > 0 and dirx > 0:
            return True
        if dir_sign < 0 and dirx < 0:
            return True
    return False


def solve_example_2_energy(k_value: float, L_value: float) -> SolveResult:
    pcr_numeric = k_value / L_value

    steps = [
        DerivationStep("1) Generalized coordinates", "q = {theta_A, theta_D}"),
        DerivationStep("2) Strain energy", "U = 1/2*k*(2*theta_A - theta_D)^2 + 1/2*k*(2*theta_D - theta_A)^2"),
        DerivationStep("3) Load potential", "W = -P*L*(3 - cos(theta_A) - cos(theta_D - theta_A) - cos(theta_D))"),
        DerivationStep("4) Total potential energy", "Pi = U + W"),
        DerivationStep("5) Equilibrium equation 1", "dPi/dtheta_A = 5*k*theta_A - 4*k*theta_D - P*L*(2*theta_A - theta_D) = 0"),
        DerivationStep("6) Equilibrium equation 2", "dPi/dtheta_D = -4*k*theta_A + 5*k*theta_D + P*L*(theta_A - 2*theta_D) = 0"),
        DerivationStep("7) Small-angle approximation", "sin(theta_A)≈theta_A, sin(theta_D)≈theta_D, sin(theta_D-theta_A)≈theta_D-theta_A"),
        DerivationStep("8) Matrix form", "[[5*k-2*P*L, -4*k+P*L], [-4*k+P*L, 5*k-2*P*L]] * [theta_A, theta_D]^T = [0,0]^T"),
        DerivationStep("9) Critical equation", "(5*k - 2*P*L)^2 - (-4*k + P*L)^2 = 0", "Factored: (k - P*L)*(3*k - P*L) = 0"),
        DerivationStep("10) Roots", "P = k/L, 3*k/L", "Smaller root is critical."),
        DerivationStep("11) Critical load", f"Pcr = k/L = {k_value:.10g}/{L_value:.10g} = {pcr_numeric:.10g}"),
        DerivationStep("12) Stability (second variation)", "d2Pi/dtheta_A^2 > 0, d2Pi/dtheta_D^2 > 0, determinant(Hessian) > 0"),
        DerivationStep("13) Stability determinant condition", "(5*k - 2*P*L)^2 > (-4*k + P*L)^2", "Equivalent: (k - P*L)*(3*k - P*L) > 0"),
        DerivationStep("14) Stable range", "P < k/L"),
    ]

    return SolveResult(
        detected_system="example_2_three_rigid_bars_two_rotational_springs",
        pcr=pcr_numeric,
        critical_equation="(5*k - 2*P*L)^2 - (-4*k + P*L)^2 = 0",
        steps=steps,
        method="Energy approach only",
    )


def _try_solve_example_2_energy(nodes: list[dict], active_members: list[dict], loads: list[dict]) -> SolveResult | None:
    if len(active_members) != 3:
        return None

    try:
        nA = _find_node(nodes, 1)
        nB = _find_node(nodes, 2)
        nC = _find_node(nodes, 3)
        nD = _find_node(nodes, 4)
    except Exception:
        return None

    xA, yA = float(nA["X"]), float(nA["Y"])
    xB, yB = float(nB["X"]), float(nB["Y"])
    xC, yC = float(nC["X"]), float(nC["Y"])
    xD, yD = float(nD["X"]), float(nD["Y"])

    if any(abs(y) > 1e-12 for y in [yA, yB, yC, yD]):
        return None

    L1 = xB - xA
    L2 = xC - xB
    L3 = xD - xC
    if L1 <= 0 or abs(L1 - L2) > 1e-9 or abs(L1 - L3) > 1e-9:
        return None

    kB = float(nB.get("K_theta", 0.0)) if _is_yes(nB.get("Has_Rot_Spring", "No")) else 0.0
    kC = float(nC.get("K_theta", 0.0)) if _is_yes(nC.get("Has_Rot_Spring", "No")) else 0.0
    if kB <= 0 or kC <= 0:
        return None
    if abs(kB - kC) > 1e-9:
        raise ValueError("Example (2) expects equal rotational springs at B and C.")

    has_left = _has_node_load(loads, 1, +1)
    has_right = _has_node_load(loads, 4, -1)
    if not (has_left and has_right):
        return None

    return solve_example_2_energy(kB, L1)


def solve_from_tables(nodes: list[dict], members: list[dict], loads: list[dict]) -> SolveResult:
    active_members = [m for m in members if _is_yes(m.get("Active", "Yes"))]

    ex2 = _try_solve_example_2_energy(nodes, active_members, loads)
    if ex2 is not None:
        return ex2

    if len(active_members) != 1:
        raise ValueError("Current solver expects exactly one active member unless Example (2) pattern is detected.")

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
        if _is_yes(ld.get("Active", "Yes"))
        and _is_yes(ld.get("Has_Load", "Yes"))
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

    k_theta_1 = float(n1.get("K_theta", 0.0)) if _is_yes(n1.get("Has_Rot_Spring", "No")) else 0.0
    k_theta_2 = float(n2.get("K_theta", 0.0)) if _is_yes(n2.get("Has_Rot_Spring", "No")) else 0.0
    k_y_2 = float(n2.get("K_y", 0.0)) if _is_yes(n2.get("Has_Vert_Spring", "No")) else 0.0

    if k_theta_1 > 0 and k_theta_2 == 0 and k_y_2 == 0:
        pcr = k_theta_1 / L
        steps = [
            DerivationStep("1) Geometry from coordinates", f"L = sqrt((x2-x1)^2 + (y2-y1)^2) = {L:.10g}"),
            DerivationStep("2) Total potential energy", "Pi(theta) = U + V = 1/2*k_theta*theta^2 - P*L*(1-cos(theta))"),
            DerivationStep("3) Equilibrium condition", "dPi/dtheta = k_theta*theta - P*L*sin(theta) = 0"),
            DerivationStep("4) Small-deflection form", "(k_theta - P*L)*theta = 0"),
            DerivationStep("5) Critical condition", "k_theta - P*L = 0"),
            DerivationStep("6) Critical load", f"Pcr = k_theta/L = {k_theta_1:.10g}/{L:.10g} = {pcr:.10g}"),
        ]
        return SolveResult("rigid_bar_rotational_spring_auto", pcr, "k_theta - P*L = 0", steps, method="Energy approach only")

    if k_theta_1 == 0 and k_theta_2 == 0 and k_y_2 > 0:
        pcr = k_y_2 * L
        steps = [
            DerivationStep("1) Geometry from coordinates", f"L = sqrt((x2-x1)^2 + (y2-y1)^2) = {L:.10g}"),
            DerivationStep("2) Kinematics", "delta = L*sin(theta)"),
            DerivationStep("3) Total potential energy", "Pi(theta) = U + V = 1/2*k_y*(L*sin(theta))^2 - P*L*(1-cos(theta))"),
            DerivationStep("4) Equilibrium condition", "dPi/dtheta = k_y*L^2*sin(theta)*cos(theta) - P*L*sin(theta) = 0"),
            DerivationStep("5) Small-deflection form", "(k_y*L - P)*L*theta = 0"),
            DerivationStep("6) Critical load", f"Pcr = k_y*L = {k_y_2:.10g}*{L:.10g} = {pcr:.10g}"),
        ]
        return SolveResult("rigid_bar_translational_spring_auto", pcr, "k_y*L - P = 0", steps, method="Energy approach only")

    raise ValueError("Input pattern not recognized yet for ENERGY-only solver.")
