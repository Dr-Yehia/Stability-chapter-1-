from dataclasses import dataclass


@dataclass
class StabilityInput:
    model: str
    L: float
    k: float


@dataclass
class StabilityResult:
    pcr: float
    equation: str
    steps: list[str]


SUPPORTED_MODELS = {
    "rigid_bar_rotational_spring": "Rigid bar supported by rotational spring (Ch.1 §1.4.1)",
    "rigid_bar_translational_spring": "Rigid bar supported by translational spring (Ch.1 §1.4.2)",
    "two_bar_system": "Two-bar system (Ch.1 §1.4.3)",
    "three_bar_system": "Three-bar system (Ch.1 §1.4.4)",
}


def solve_critical_load(inp: StabilityInput) -> StabilityResult:
    if inp.L <= 0:
        raise ValueError("L must be > 0")
    if inp.k <= 0:
        raise ValueError("k must be > 0")

    m = inp.model
    L = inp.L
    k = inp.k

    if m == "rigid_bar_rotational_spring":
        pcr = k / L
        equation = "kθ − PLθ = 0  =>  Pcr = k/L"
        steps = [
            "Small-deflection equilibrium about hinge: kθ = PLθ.",
            "Trivial solution θ=0 always exists.",
            "Non-trivial solution needs k−PL=0.",
            "Therefore Pcr = k/L.",
        ]
    elif m == "rigid_bar_translational_spring":
        pcr = k * L
        equation = "kL²θ − PLθ = 0  =>  Pcr = kL"
        steps = [
            "Small-deflection equilibrium gives kL²θ = PLθ.",
            "Non-trivial solution requires kL²−PL=0.",
            "Therefore Pcr = kL.",
        ]
    elif m == "two_bar_system":
        pcr = 1.5 * k * L
        equation = "(2/3)kLθ − Pθ = 0  =>  Pcr = 3kL/2"
        steps = [
            "From free-body equilibrium and spring compatibility.",
            "Linearized equation becomes (2/3)kLθ − Pθ = 0.",
            "Non-trivial solution gives Pcr = 3kL/2.",
        ]
    elif m == "three_bar_system":
        pcr = k / L
        equation = "det([[2k−PL, −k], [−k, 2k−PL]]) = 0 => P={k/L,3k/L}"
        steps = [
            "Write linearized equations in θ1, θ2.",
            "Form characteristic equation det(K−PG)=0.",
            "Eigenvalues are P1=k/L and P2=3k/L.",
            "Critical load is the smallest positive value: Pcr=k/L.",
        ]
    else:
        raise ValueError(f"Unsupported model: {m}")

    return StabilityResult(pcr=pcr, equation=equation, steps=steps)
