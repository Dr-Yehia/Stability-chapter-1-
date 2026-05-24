from dataclasses import dataclass
from typing import List


@dataclass
class StabilityInput:
    model: str
    L: float
    k: float


@dataclass
class DerivationStep:
    title: str
    expression: str
    substitution: str | None = None
    result: str | None = None


@dataclass
class StabilityResult:
    pcr: float
    unit_check: str
    critical_equation: str
    steps: List[DerivationStep]
    reference: str


SUPPORTED_MODELS = {
    "rigid_bar_rotational_spring": "§1.4.1 Rigid bar + rotational spring (small deflection)",
    "rigid_bar_translational_spring": "§1.4.2 Rigid bar + translational spring (small deflection)",
    "two_bar_system": "§1.4.3 Two-bar system (small deflection)",
    "three_bar_system": "§1.4.4 Three-bar system (small deflection)",
}


def _validate(inp: StabilityInput) -> None:
    if inp.model not in SUPPORTED_MODELS:
        raise ValueError(f"Unsupported model: {inp.model}")
    if inp.L <= 0:
        raise ValueError("L must be > 0")
    if inp.k <= 0:
        raise ValueError("k must be > 0")


def solve_critical_load(inp: StabilityInput) -> StabilityResult:
    _validate(inp)
    L, k = inp.L, inp.k

    if inp.model == "rigid_bar_rotational_spring":
        steps = [
            DerivationStep(
                title="1) Small-deflection equilibrium equation",
                expression="kθ − PLθ = 0   (book Eq. 1.4.1 / 1.4.7 form)",
                substitution=f"Substitute k={k:g}, L={L:g}",
            ),
            DerivationStep(
                title="2) Factor θ",
                expression="θ(k − PL) = 0",
                result="Non-trivial buckling requires k − PL = 0",
            ),
            DerivationStep(
                title="3) Solve for critical load",
                expression="Pcr = k/L",
                result=f"Pcr = {k:g}/{L:g} = {k/L:.10g}",
            ),
        ]
        return StabilityResult(
            pcr=k / L,
            unit_check="[k]/[L] (rotational spring case)",
            critical_equation="k − PL = 0",
            steps=steps,
            reference="Chen & Lui, Chapter 1, §1.4.1",
        )

    if inp.model == "rigid_bar_translational_spring":
        steps = [
            DerivationStep(
                title="1) Small-deflection equilibrium equation",
                expression="kL²θ − PLθ = 0   (book Eq. 1.4.10 / 1.4.16 form)",
                substitution=f"Substitute k={k:g}, L={L:g}",
            ),
            DerivationStep(
                title="2) Factor θ",
                expression="θ(kL² − PL) = 0",
                result="Non-trivial buckling requires kL² − PL = 0",
            ),
            DerivationStep(
                title="3) Solve for critical load",
                expression="Pcr = kL",
                result=f"Pcr = {k:g}×{L:g} = {k*L:.10g}",
            ),
        ]
        return StabilityResult(
            pcr=k * L,
            unit_check="[k]·[L] (translational spring case)",
            critical_equation="kL² − PL = 0",
            steps=steps,
            reference="Chen & Lui, Chapter 1, §1.4.2",
        )

    if inp.model == "two_bar_system":
        steps = [
            DerivationStep(
                title="1) Linearized equilibrium form",
                expression="(2/3)kLθ − Pθ = 0   (book Eq. 1.4.22 / 1.4.28 result)",
                substitution=f"Substitute k={k:g}, L={L:g}",
            ),
            DerivationStep(
                title="2) Non-trivial condition",
                expression="(2/3)kL − P = 0",
                result="Pcr = 3kL/2",
            ),
            DerivationStep(
                title="3) Numerical value",
                expression="Pcr = 1.5kL",
                result=f"Pcr = 1.5×{k:g}×{L:g} = {1.5*k*L:.10g}",
            ),
        ]
        return StabilityResult(
            pcr=1.5 * k * L,
            unit_check="force unit",
            critical_equation="(2/3)kL − P = 0",
            steps=steps,
            reference="Chen & Lui, Chapter 1, §1.4.3",
        )

    # three_bar_system
    steps = [
        DerivationStep(
            title="1) Characteristic matrix (small deflection)",
            expression="[[2k−PL, −k], [−k, 2k−PL]] [θ1 θ2]^T = 0   (book Eq. 1.4.31)",
            substitution=f"Substitute k={k:g}, L={L:g}",
        ),
        DerivationStep(
            title="2) Non-trivial condition",
            expression="det([[2k−PL, −k], [−k, 2k−PL]]) = 0",
            result="(2k−PL)^2 − k^2 = 0",
        ),
        DerivationStep(
            title="3) Eigenvalues and critical load",
            expression="P = {k/L, 3k/L}",
            result=f"Pcr = min({k/L:.10g}, {3*k/L:.10g}) = {k/L:.10g}",
        ),
    ]
    return StabilityResult(
        pcr=k / L,
        unit_check="force unit",
        critical_equation="(2k−PL)^2 − k^2 = 0",
        steps=steps,
        reference="Chen & Lui, Chapter 1, §1.4.4",
    )
