import pandas as pd
import streamlit as st

from solver import SUPPORTED_MODELS, StabilityInput, solve_critical_load

st.set_page_config(page_title="Chapter 1 Stability Solver", layout="wide")
st.title("Structural Stability — Chapter 1 Solver")
st.caption("Professional step-by-step output aligned with Chapter 1 benchmark equations.")

with st.expander("Input templates (Nodes / Loads)", expanded=False):
    nodes = pd.DataFrame([
        {"Node_ID": 1, "X": 0.0, "Y": 0.0, "Has_Support": "Yes", "Support_Type": "Hinged", "Fix_Ux": "Yes", "Fix_Uy": "Yes", "Fix_Rz": "No", "Has_Rot_Spring": "Yes", "K_theta": 10.0, "Has_Vert_Spring": "No", "K_y": 0.0, "Has_Horz_Spring": "No", "K_x": 0.0, "Has_Point_Load": "No", "Active": "Yes"},
        {"Node_ID": 2, "X": 1.0, "Y": 0.0, "Has_Support": "No", "Support_Type": "Free", "Fix_Ux": "No", "Fix_Uy": "No", "Fix_Rz": "No", "Has_Rot_Spring": "No", "K_theta": 0.0, "Has_Vert_Spring": "Yes", "K_y": 10.0, "Has_Horz_Spring": "No", "K_x": 0.0, "Has_Point_Load": "Yes", "Active": "Yes"},
    ])
    loads = pd.DataFrame([
        {"Load_ID": 1, "Target_Type": "Node", "Target_ID": 2, "Has_Load": "Yes", "Load_Type": "Force", "Magnitude": 100.0, "Direction_Mode": "Global", "Dir_X": -1, "Dir_Y": 0, "Angle_deg": 0.0, "Mz_Sign": "CCW", "Active": "Yes"}
    ])
    nodes_df = st.data_editor(nodes, num_rows="dynamic", use_container_width=True)
    loads_df = st.data_editor(loads, num_rows="dynamic", use_container_width=True)
    st.download_button("Download nodes CSV", nodes_df.to_csv(index=False).encode(), "nodes_template.csv", "text/csv")
    st.download_button("Download loads CSV", loads_df.to_csv(index=False).encode(), "loads_template.csv", "text/csv")

st.subheader("Solve benchmark model")
model = st.selectbox("Model", list(SUPPORTED_MODELS.keys()), format_func=lambda k: SUPPORTED_MODELS[k])
col1, col2 = st.columns(2)
with col1:
    L = st.number_input("L", min_value=1e-12, value=1.0, format="%.6f")
with col2:
    k = st.number_input("k", min_value=1e-12, value=10.0, format="%.6f")

if st.button("Solve with detailed derivation"):
    result = solve_critical_load(StabilityInput(model=model, L=L, k=k))
    st.success(f"Critical load Pcr = {result.pcr:.10g}")
    st.write(f"Reference: {result.reference}")
    st.write(f"Critical condition: `{result.critical_equation}`")
    st.write(f"Unit check: {result.unit_check}")

    st.markdown("### Step-by-step (book style)")
    for i, step in enumerate(result.steps, 1):
        st.markdown(f"**Step {i}: {step.title}**")
        st.code(step.expression)
        if step.substitution:
            st.write(step.substitution)
        if step.result:
            st.info(step.result)
