# Structural Stability — Chapter 1 Solver

Professional Streamlit prototype with explicit step-by-step derivations aligned with Chapter 1 benchmark equations from Chen & Lui.

## Run

```bash
python -m pip install -r requirements.txt
streamlit run app.py
```

## Automated tests

```bash
python -m pytest -q
```

## Implemented benchmark models (small-deflection)

1. §1.4.1 Rigid bar + rotational spring: \(P_{cr}=k/L\)
2. §1.4.2 Rigid bar + translational spring: \(P_{cr}=kL\)
3. §1.4.3 Two-bar system: \(P_{cr}=3kL/2\)
4. §1.4.4 Three-bar system: \(P_{cr}=k/L\) (lowest eigenvalue)

## Notes

- Output now includes structured derivation steps (equation, substitution, and final numerical result).
- This is still a benchmark solver; full arbitrary-geometry FEM/nonlinear workflow is a planned next phase.
