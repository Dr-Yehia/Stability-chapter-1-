from solver import solve_from_tables


def test_example_2_energy_only():
    nodes = [
        {"Node_ID": 1, "X": 0, "Y": 0, "Has_Rot_Spring": "No", "K_theta": 0, "Has_Vert_Spring": "No", "K_y": 0, "Active": "Yes"},
        {"Node_ID": 2, "X": 1, "Y": 0, "Has_Rot_Spring": "Yes", "K_theta": 10, "Has_Vert_Spring": "No", "K_y": 0, "Active": "Yes"},
        {"Node_ID": 3, "X": 2, "Y": 0, "Has_Rot_Spring": "Yes", "K_theta": 10, "Has_Vert_Spring": "No", "K_y": 0, "Active": "Yes"},
        {"Node_ID": 4, "X": 3, "Y": 0, "Has_Rot_Spring": "No", "K_theta": 0, "Has_Vert_Spring": "No", "K_y": 0, "Active": "Yes"},
    ]
    members = [
        {"Member_ID": 1, "Start_Node": 1, "End_Node": 2, "Active": "Yes"},
        {"Member_ID": 2, "Start_Node": 2, "End_Node": 3, "Active": "Yes"},
        {"Member_ID": 3, "Start_Node": 3, "End_Node": 4, "Active": "Yes"},
    ]
    loads = [
        {"Load_ID": 1, "Target_Type": "Node", "Target_ID": 1, "Has_Load": "Yes", "Load_Type": "Force", "Dir_X": 1, "Dir_Y": 0, "Active": "Yes"},
        {"Load_ID": 2, "Target_Type": "Node", "Target_ID": 4, "Has_Load": "Yes", "Load_Type": "Force", "Dir_X": -1, "Dir_Y": 0, "Active": "Yes"},
    ]

    r = solve_from_tables(nodes, members, loads)
    assert r.method == "Energy approach only"
    assert r.detected_system == "example_2_three_rigid_bars_two_rotational_springs"
    assert abs(r.pcr - 10.0) < 1e-12
    assert any("2*theta_A - theta_D" in s.expression for s in r.steps)
    assert any("Pcr = k/L" in s.expression for s in r.steps)
    assert any("P < k/L" in s.expression for s in r.steps)


def test_auto_rotational_case_energy_only_still_supported():
    nodes = [
        {"Node_ID": 1, "X": 0, "Y": 0, "Has_Rot_Spring": "Yes", "K_theta": 10, "Has_Vert_Spring": "No", "K_y": 0, "Active": "Yes"},
        {"Node_ID": 2, "X": 1, "Y": 0, "Has_Rot_Spring": "No", "K_theta": 0, "Has_Vert_Spring": "No", "K_y": 0, "Active": "Yes"},
    ]
    members = [{"Member_ID": 1, "Start_Node": 1, "End_Node": 2, "Active": "Yes"}]
    loads = [{"Load_ID": 1, "Target_Type": "Node", "Target_ID": 2, "Has_Load": "Yes", "Load_Type": "Force", "Dir_X": -1, "Dir_Y": 0, "Active": "Yes"}]
    r = solve_from_tables(nodes, members, loads)
    assert abs(r.pcr - 10.0) < 1e-12
    assert r.method == "Energy approach only"
