from solver import solve_from_tables


def test_auto_rotational_case():
    nodes = [
        {"Node_ID": 1, "X": 0, "Y": 0, "Has_Rot_Spring": "Yes", "K_theta": 10, "Has_Vert_Spring": "No", "K_y": 0, "Active": "Yes"},
        {"Node_ID": 2, "X": 1, "Y": 0, "Has_Rot_Spring": "No", "K_theta": 0, "Has_Vert_Spring": "No", "K_y": 0, "Active": "Yes"},
    ]
    members = [{"Member_ID": 1, "Start_Node": 1, "End_Node": 2, "Active": "Yes"}]
    loads = [{"Load_ID": 1, "Target_Type": "Node", "Target_ID": 2, "Has_Load": "Yes", "Load_Type": "Force", "Dir_X": -1, "Dir_Y": 0, "Active": "Yes"}]
    r = solve_from_tables(nodes, members, loads)
    assert abs(r.pcr - 10.0) < 1e-12


def test_auto_translational_case():
    nodes = [
        {"Node_ID": 1, "X": 0, "Y": 0, "Has_Rot_Spring": "No", "K_theta": 0, "Has_Vert_Spring": "No", "K_y": 0, "Active": "Yes"},
        {"Node_ID": 2, "X": 1, "Y": 0, "Has_Rot_Spring": "No", "K_theta": 0, "Has_Vert_Spring": "Yes", "K_y": 10, "Active": "Yes"},
    ]
    members = [{"Member_ID": 1, "Start_Node": 1, "End_Node": 2, "Active": "Yes"}]
    loads = [{"Load_ID": 1, "Target_Type": "Node", "Target_ID": 2, "Has_Load": "Yes", "Load_Type": "Force", "Dir_X": -1, "Dir_Y": 0, "Active": "Yes"}]
    r = solve_from_tables(nodes, members, loads)
    assert abs(r.pcr - 10.0) < 1e-12
