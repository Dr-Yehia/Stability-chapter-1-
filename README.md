# Chapter 1 Stability Solver (Prototype)

This prototype implements a Streamlit app and a solver for selected benchmark models from Chapter 1 of *Structural Stability (Chen & Lui)*.

## Run

```bash
python -m pip install -r requirements.txt
streamlit run app.py
```

## Implemented benchmark models

- Rigid bar + rotational spring: `Pcr = k/L`
- Rigid bar + translational spring: `Pcr = kL`
- Two-bar system: `Pcr = 3kL/2`
- Three-bar system: `Pcr = k/L` (lowest eigenvalue)

## Tests

```bash
python -m pytest -q
```
