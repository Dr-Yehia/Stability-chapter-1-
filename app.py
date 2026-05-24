import pandas as pd
import streamlit as st
from solver import solve_from_tables

st.set_page_config(page_title="Chapter 1 Energy Solver", layout="wide")
st.title("Chapter 1 Solver — Energy Approach Only")
st.caption("All outputs are generated from total potential energy Pi = U + V.")

st.markdown("### Nodes")
default_nodes = pd.DataFrame([
    {"Node_ID": 1, "X": 0.0, "Y": 0.0, "Has_Rot_Spring": "No", "K_theta": 0.0, "Has_Vert_Spring": "No", "K_y": 0.0, "Active": "Yes"},
    {"Node_ID": 2, "X": 1.0, "Y": 0.0, "Has_Rot_Spring": "Yes", "K_theta": 10.0, "Has_Vert_Spring": "No", "K_y": 0.0, "Active": "Yes"},
    {"Node_ID": 3, "X": 2.0, "Y": 0.0, "Has_Rot_Spring": "Yes", "K_theta": 10.0, "Has_Vert_Spring": "No", "K_y": 0.0, "Active": "Yes"},
    {"Node_ID": 4, "X": 3.0, "Y": 0.0, "Has_Rot_Spring": "No", "K_theta": 0.0, "Has_Vert_Spring": "No", "K_y": 0.0, "Active": "Yes"},
])
nodes_df = st.data_editor(default_nodes, num_rows="dynamic", use_container_width=True)

st.markdown("### Members")
default_members = pd.DataFrame([
    {"Member_ID": 1, "Start_Node": 1, "End_Node": 2, "Active": "Yes"},
    {"Member_ID": 2, "Start_Node": 2, "End_Node": 3, "Active": "Yes"},
    {"Member_ID": 3, "Start_Node": 3, "End_Node": 4, "Active": "Yes"},
])
members_df = st.data_editor(default_members, num_rows="dynamic", use_container_width=True)

st.markdown("### Loads")
default_loads = pd.DataFrame([
    {"Load_ID": 1, "Target_Type": "Node", "Target_ID": 1, "Has_Load": "Yes", "Load_Type": "Force", "Dir_X": 1, "Dir_Y": 0, "Active": "Yes"},
    {"Load_ID": 2, "Target_Type": "Node", "Target_ID": 4, "Has_Load": "Yes", "Load_Type": "Force", "Dir_X": -1, "Dir_Y": 0, "Active": "Yes"},
])
loads_df = st.data_editor(default_loads, num_rows="dynamic", use_container_width=True)

if st.button("Solve automatically (Energy only)"):
    try:
        result = solve_from_tables(nodes_df.to_dict("records"), members_df.to_dict("records"), loads_df.to_dict("records"))
        st.success(f"Detected: {result.detected_system}")
        st.success(f"Method: {result.method}")
        st.success(f"Critical load Pcr = {result.pcr:.10g}")
        st.write(f"Critical equation: `{result.critical_equation}`")
        st.markdown("### Step-by-step derivation")
        for i, s in enumerate(result.steps, 1):
            st.markdown(f"**Step {i}: {s.title}**")
            st.code(s.expression)
            if s.result:
                st.info(s.result)
    except Exception as e:
        st.error(str(e))
