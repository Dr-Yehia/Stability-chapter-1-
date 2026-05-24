import pandas as pd
import streamlit as st
from solver import SUPPORTED_MODELS, StabilityInput, solve_critical_load

st.set_page_config(page_title="Chapter 1 Stability Solver", layout="wide")
st.title("Chapter 1 Stability Solver (Prototype)")
st.caption("Input by nodes/options (Yes/No), then solve benchmark models from Chapter 1.")

st.header("1) Node input template")
default_nodes = pd.DataFrame([
    {
        "Node_ID": 1, "X": 0.0, "Y": 0.0,
        "Has_Support": "Yes", "Support_Type": "Hinged",
        "Fix_Ux": "Yes", "Fix_Uy": "Yes", "Fix_Rz": "No",
        "Has_Rot_Spring": "Yes", "K_theta": 10.0,
        "Has_Vert_Spring": "No", "K_y": 0.0,
        "Has_Horz_Spring": "No", "K_x": 0.0,
        "Has_Point_Load": "No", "Active": "Yes"
    },
    {
        "Node_ID": 2, "X": 1.0, "Y": 0.0,
        "Has_Support": "No", "Support_Type": "Free",
        "Fix_Ux": "No", "Fix_Uy": "No", "Fix_Rz": "No",
        "Has_Rot_Spring": "No", "K_theta": 0.0,
        "Has_Vert_Spring": "Yes", "K_y": 10.0,
        "Has_Horz_Spring": "No", "K_x": 0.0,
        "Has_Point_Load": "Yes", "Active": "Yes"
    }
])

nodes_df = st.data_editor(default_nodes, num_rows="dynamic", use_container_width=True)

st.header("2) Loads (forces / moments + direction)")
default_loads = pd.DataFrame([
    {
        "Load_ID": 1, "Target_Type": "Node", "Target_ID": 2,
        "Has_Load": "Yes", "Load_Type": "Force", "Magnitude": 100.0,
        "Direction_Mode": "Global", "Dir_X": -1, "Dir_Y": 0,
        "Angle_deg": 0.0, "Mz_Sign": "CCW", "Active": "Yes"
    }
])
loads_df = st.data_editor(default_loads, num_rows="dynamic", use_container_width=True)

st.header("3) Solve a supported Chapter-1 model")
model = st.selectbox("Model", options=list(SUPPORTED_MODELS.keys()), format_func=lambda x: SUPPORTED_MODELS[x])
col1, col2 = st.columns(2)
with col1:
    L = st.number_input("L", min_value=1e-9, value=1.0, format="%.6f")
with col2:
    k = st.number_input("k", min_value=1e-9, value=10.0, format="%.6f")

if st.button("Solve"):
    res = solve_critical_load(StabilityInput(model=model, L=L, k=k))
    st.success(f"Critical load Pcr = {res.pcr:.6g}")
    st.markdown(f"**Characteristic equation:** `{res.equation}`")
    st.markdown("**Step-by-step (book style):**")
    for i, step in enumerate(res.steps, start=1):
        st.write(f"{i}. {step}")

st.divider()
st.subheader("Export templates")
st.download_button(
    "Download Nodes template CSV",
    data=nodes_df.to_csv(index=False).encode("utf-8"),
    file_name="nodes_template.csv",
    mime="text/csv",
)
st.download_button(
    "Download Loads template CSV",
    data=loads_df.to_csv(index=False).encode("utf-8"),
    file_name="loads_template.csv",
    mime="text/csv",
)
