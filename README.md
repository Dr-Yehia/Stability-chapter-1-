# Chapter 1 Solver — ENERGY APPROACH ONLY

This solver intentionally uses **Energy Approach only** (`Π = U + V`) and does **not** use bifurcation formulation in the workflow/output.

## What it does now

- Reads `Nodes`, `Members`, `Loads` tables.
- Detects supported benchmark pattern automatically (no problem-number selection).
- Produces **step-by-step energy derivation**:
  1. geometry,
  2. total potential energy,
  3. equilibrium condition `∂Π/∂q = 0`,
  4. small-deflection simplification,
  5. critical condition,
  6. `Pcr`.

## Currently supported auto-detected systems

1. Single rigid bar + rotational spring at node 1 + end compressive load in -X.
2. Single rigid bar + vertical translational spring at node 2 + end compressive load in -X.

## Run

```bash
python -m pip install -r requirements.txt
streamlit run app.py
python -m pytest -q
```
