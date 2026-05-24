# Chapter 1 Solver — ENERGY APPROACH ONLY

This solver uses only the Energy Approach (`Pi = U + V`) and provides step-by-step derivation output.

## Supported workflows

### 1) Example (2): three rigid bars A-B-C-D with two rotational springs
- Geometry: three equal spans `L`.
- Springs: equal rotational springs `k` at nodes B and C.
- Loads: node A in `+X`, node D in `-X`.
- Generalized coordinates: `theta_A`, `theta_D`.
- Uses:
  - `U = 1/2*k*(2*theta_A - theta_D)^2 + 1/2*k*(2*theta_D - theta_A)^2`
  - `W = -P*L*(3 - cos(theta_A) - cos(theta_D - theta_A) - cos(theta_D))`
  - `Pi = U + W`
- Returns:
  - `P = k/L, 3k/L`
  - `Pcr = k/L`
  - Stability condition from second variation ending in `P < k/L`.

### 2) Single-bar energy cases (kept for backward compatibility)
- Rigid bar + rotational spring at node 1 + compressive end load in `-X`.
- Rigid bar + vertical spring at node 2 + compressive end load in `-X`.

## Run

```bash
python -m pip install -r requirements.txt
python -m pytest -q
streamlit run app.py
```
