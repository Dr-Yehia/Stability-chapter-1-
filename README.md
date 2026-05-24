# Chapter 1 Auto Solver

This version solves from **input tables** (nodes/members/loads) without selecting "problem 1/2/3" manually.

## Current auto-detected systems

- Single rigid bar, node-1 rotational spring, node-2 compressive load in -X: `Pcr = kθ/L`
- Single rigid bar, node-2 vertical spring, node-2 compressive load in -X: `Pcr = ky*L`

## Example requested by user

- Node 1 = (0,0)
- Node 2 = (1,0)
- Rotational spring at node 1
- Force at node 2 in negative X

The solver detects the system and returns `Pcr` with step-by-step derivation.

## Run

```bash
python -m pip install -r requirements.txt
streamlit run app.py
python -m pytest -q
```
