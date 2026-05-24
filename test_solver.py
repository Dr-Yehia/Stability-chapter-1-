from solver import StabilityInput, solve_critical_load


def test_rotational_spring_pcr_and_reference():
    r = solve_critical_load(StabilityInput("rigid_bar_rotational_spring", L=2.0, k=10.0))
    assert abs(r.pcr - 5.0) < 1e-12
    assert "§1.4.1" in r.reference
    assert len(r.steps) >= 3


def test_translational_spring_pcr():
    r = solve_critical_load(StabilityInput("rigid_bar_translational_spring", L=2.0, k=10.0))
    assert abs(r.pcr - 20.0) < 1e-12


def test_two_bar_pcr():
    r = solve_critical_load(StabilityInput("two_bar_system", L=2.0, k=10.0))
    assert abs(r.pcr - 30.0) < 1e-12


def test_three_bar_pcr():
    r = solve_critical_load(StabilityInput("three_bar_system", L=2.0, k=10.0))
    assert abs(r.pcr - 5.0) < 1e-12


def test_invalid_inputs():
    try:
        solve_critical_load(StabilityInput("three_bar_system", L=0.0, k=10.0))
        assert False
    except ValueError:
        assert True
