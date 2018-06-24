
from .context import units, SoilProfile
import numpy as np


def case_a():
    profile = SoilProfile(unit_system='English', water_table=10)
    profile.add_layer(soil_type='cohesionless', height=16, tuw=90)
    total_a, pore_a, effective_a = profile.calculate_stress(6, kind='all')
    total_b, pore_b, effective_b = profile.calculate_stress(14, kind='all')

    return total_a, pore_a, effective_a, total_b, pore_b, effective_b


def test_case_a():
    total_a, pore_a, effective_a, total_b, pore_b, effective_b = case_a()

    assert total_a == 0.540 * units.kip / units.feet ** 2
    assert pore_a == 0.000 * units.kip / units.feet ** 2
    assert effective_a == 0.540 * units.kip / units.feet ** 2
    assert total_b == 1.260 * units.kip / units.feet ** 2
    assert pore_b == 0.2496 * units.kip / units.feet ** 2
    assert effective_b == 1.0104 * units.kip / units.feet ** 2


def case_b():
    profile = SoilProfile(unit_system='English', water_table=10)
    profile.add_layer(soil_type='cohesionless', height=5, tuw=90)
    profile.add_layer(soil_type='cohesive', height=11, tuw=110)
    total_a, pore_a, effective_a = profile.calculate_stress(6, kind='all')
    total_b, pore_b, effective_b = profile.calculate_stress(14, kind='all')

    return total_a, pore_a, effective_a, total_b, pore_b, effective_b


def test_case_b():
    total_a, pore_a, effective_a, total_b, pore_b, effective_b = case_b()

    np.testing.assert_almost_equal(total_a.magnitude, 0.560, 3)
    assert total_a.units == units.kip / units.feet ** 2
    assert pore_a == 0.000 * units.kip / units.feet ** 2
    np.testing.assert_almost_equal(effective_a.magnitude, 0.560, 3)
    assert effective_a.units == units.kip / units.feet ** 2
    assert total_b == 1.440 * units.kip / units.feet ** 2
    assert pore_b == 0.2496 * units.kip / units.feet ** 2
    assert effective_b == 1.1904 * units.kip / units.feet ** 2


def case_c():
    profile = SoilProfile(unit_system='English', water_table=-7)
    profile.add_layer(soil_type='cohesionless', height=4.5, tuw=90)
    profile.add_layer(soil_type='cohesive', height=4.5, tuw=110)
    total_a, pore_a, effective_a = profile.calculate_stress(-3, kind='all')
    total_b, pore_b, effective_b = profile.calculate_stress(7, kind='all')

    return total_a, pore_a, effective_a, total_b, pore_b, effective_b


def test_case_c():
    total_a, pore_a, effective_a, total_b, pore_b, effective_b = case_c()

    assert total_a == 0.2496 * units.kip / units.feet ** 2
    assert pore_a == 0.2496 * units.kip / units.feet ** 2
    assert effective_a == 0.000 * units.kip / units.feet ** 2
    assert total_b == 1.1168 * units.kip / units.feet ** 2
    np.testing.assert_almost_equal(pore_b.magnitude, 0.874, 3)
    assert pore_b.units == units.kip / units.feet ** 2
    np.testing.assert_almost_equal(effective_b.magnitude, 0.243, 3)
    assert effective_b.units == units.kip / units.feet ** 2
