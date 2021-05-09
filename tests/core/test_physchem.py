# -*- coding: utf-8 -*-
from aguaclara.core.units import u
from aguaclara.core import physchem as pc
from aguaclara.core.physchem import DeprecatedFunctionError
import unittest


class QuantityTest(unittest.TestCase):
    def assertAlmostEqualQuantity(self, first, second, places=7):
        self.assertAlmostEqual(first.magnitude, second.magnitude, places)
        self.assertEqual(first.units, second.units, places)


class GasTest(QuantityTest):
    def test_density_air(self):
        self.assertWarns(
            UserWarning,
            pc.density_air,
            *(1 * u.atm, 28.97 * u.g / u.mol, 273 * u.K)
        )

    def test_density_gas(self):
        """Test the gas density function"""
        answer = 1.29320768 * u.kg / u.m ** 3
        self.assertAlmostEqualQuantity(
            pc.density_gas(1 * u.atm, 28.97 * u.g / u.mol, 273 * u.K), answer
        )
        answer = 2.06552481 * u.kg / u.m ** 3
        self.assertAlmostEqualQuantity(
            pc.density_gas(5 * u.atm, 10 * u.g / u.mol, 295 * u.K), answer
        )
        answer = 1.62487951 * u.kg / u.m ** 3
        self.assertAlmostEqualQuantity(
            pc.density_gas(101325 * u.Pa, 40 * u.g / u.mol, 300 * u.K), answer
        )
        answer = 0.20786108 * u.kg / u.m ** 3
        self.assertAlmostEqualQuantity(
            pc.density_gas(700 * u.mmHg, 5 * u.g / u.mol, 270 * u.K), answer
        )
        answer = 0 * u.kg / u.m ** 3
        self.assertAlmostEqualQuantity(
            pc.density_gas(0 * u.atm, 28.97 * u.g / u.mol, 273 * u.K), answer
        )


class GeometryTest(QuantityTest):
    """Test the circular area and diameter functions."""

    def test_area_circle(self):
        """area_circle should should give known result with known input."""
        checks = (
            (1 * u.m, 0.7853981633974483 * u.m ** 2),
            (495.6 * u.m, 192908.99423885669 * u.m ** 2),
            (495.6 * u.m, 192908.99423885669 * u.m ** 2),
        )
        for i in checks:
            with self.subTest(i=i):
                self.assertAlmostEqualQuantity(pc.area_circle(i[0]), i[1])

    def test_area_circle_range(self):
        """area_circle should return errors with inputs <= 0."""
        checks = (0 * u.m, -3 * u.m)
        for i in checks:
            with self.subTest(i=i):
                self.assertRaises(ValueError, pc.area_circle, i)

    def test_diam_circle(self):
        """diam_circle should should give known result with known input."""
        checks = (
            (1 * u.m ** 2, 1.1283791670955126 * u.m),
            (0.1 * u.m ** 2, 0.3568248232305542 * u.m),
            (347 * u.m ** 2, 21.019374919894773 * u.m),
            (10000 * u.m ** 2, 112.83791670955126 * u.m),
        )
        for i in checks:
            with self.subTest(i=i):
                self.assertAlmostEqualQuantity(pc.diam_circle(i[0]), i[1])

    def test_diam_circle_range(self):
        """diam_circle should return errors with inputs <= 0."""
        checks = ((0 * u.m, ValueError), (-3 * u.m, ValueError))
        for i in checks:
            with self.subTest(i=i):
                self.assertRaises(i[1], pc.diam_circle, i[0])


class WaterPropertiesTest(QuantityTest):
    """Test the density and dynamic/kinematic viscosity functions."""

    def test_water_table(self):
        """The table density_water relies upon shouldn't need to be changed."""
        table = pc.WATER_DENSITY_TABLE
        checks = ((0, 273.15, 999.9), (4, 303.15, 995.7), (11, 373.15, 958.4))
        for i in checks:
            with self.subTest(i=i):
                self.assertAlmostEqual(table[0][i[0]], i[1])
                self.assertAlmostEqual(table[1][i[0]], i[2])

    def test_water_table_units(self):
        """The water density table should handle units properly."""
        table = pc.WATER_DENSITY_TABLE
        self.assertAlmostEqual(
            table[0][0], (0 * u.degC).to_base_units().magnitude
        )
        self.assertAlmostEqual(
            table[0][4], (30 * u.degC).to_base_units().magnitude
        )

    def test_density_water_true(self):
        """density_water should give known result with known input."""
        checks = (
            (273.15 * u.degK, 999.9 * u.kg / u.m ** 3),
            (300 * u.degK, 996.601907542082 * u.kg / u.m ** 3),
            (343.15 * u.degK, 977.8 * u.kg / u.m ** 3),
        )
        for i in checks:
            with self.subTest(i=i):
                self.assertAlmostEqualQuantity(pc.density_water(i[0]), i[1])

    def test_density_water_warning(self):
        checks = (
            lambda: pc.density_water(Temperature=1 * u.degK, temp=1 * u.degK),
            lambda: pc.density_water(),
        )
        for i in checks:
            with self.subTest(i=i):
                self.assertRaises(TypeError, i)

        self.assertWarns(UserWarning, lambda: pc.density_water(temp=1 * u.degK))

    def test_viscosity_dynamic(self):
        self.assertWarns(UserWarning, pc.viscosity_dynamic, 300 * u.degK)

    def test_viscosity_dynamic_water(self):
        """viscosity_dynamic_water should give known result with known input."""
        checks = (
            (300 * u.degK, 0.0008540578046518858 * u.kg / (u.m * u.s)),
            (372 * u.degK, 0.00028238440851243975 * u.kg / (u.m * u.s)),
            (274 * u.degK, 0.0017060470223965783 * u.kg / (u.m * u.s)),
            (26.85 * u.degC, 0.0008540578046518858 * u.kg / (u.m * u.s)),
        )
        for i in checks:
            with self.subTest(i=i):
                self.assertAlmostEqualQuantity(
                    pc.viscosity_dynamic_water(i[0]), i[1]
                )

    def test_viscosity_kinematic(self):
        self.assertWarns(UserWarning, pc.viscosity_kinematic, 300 * u.degK)

    def test_viscosity_kinematic_water(self):
        """viscosity_kinematic_water should give known results with known input."""
        checks = (
            (342 * u.degK, 4.1584506710898959e-07 * u.m ** 2 / u.s),
            (297 * u.degK, 9.1670473903811879e-07 * u.m ** 2 / u.s),
            (273.15 * u.degK, 1.7532330683680798e-06 * u.m ** 2 / u.s),
            (373.15 * u.degK, 2.9108883329847625e-07 * u.m ** 2 / u.s),
            (100 * u.degC, 2.9108883329847625e-07 * u.m ** 2 / u.s),
        )
        for i in checks:
            with self.subTest(i=i):
                self.assertAlmostEqualQuantity(
                    pc.viscosity_kinematic_water(i[0]), i[1]
                )
                self.assertAlmostEqualQuantity(
                    pc.viscosity_kinematic_water(i[0]),
                    (pc.viscosity_dynamic_water(i[0]) / pc.density_water(i[0])),
                )


class RadiusFuncsTest(QuantityTest):
    """Test the various radius-acquisition functions."""

    def test_radius_hydraulic(self):
        self.assertWarns(
            UserWarning, pc.radius_hydraulic, *(10 * u.m, 4 * u.m, False)
        )

    def test_radius_hydraulic_rect(self):
        """radius_hydraulic_rect should return known results with known input."""
        checks = (
            ([10 * u.m, 4 * u.m, False], 1.4285714285714286 * u.m),
            ([10 * u.m, 4 * u.m, True], 2.2222222222222223 * u.m),
        )
        for i in checks:
            with self.subTest(i=i):
                self.assertAlmostEqualQuantity(
                    pc.radius_hydraulic_rect(*i[0]), i[1]
                )

    def test_radius_hydraulic_range(self):
        """radius_hydraulic should raise errors when inputs are out of bounds."""
        checks = (
            ([0 * u.m, 4 * u.m, True], ValueError),
            ([-1 * u.m, 4 * u.m, True], ValueError),
            ([1 * u.m, 0 * u.m, True], ValueError),
            ([10 * u.m, -1 * u.m, True], ValueError),
            ([10 * u.m, 4 * u.m, 0 * u.m], TypeError),
            ([10 * u.m, 4 * u.m, 6 * u.m], TypeError),
        )
        for i in checks:
            with self.subTest(i=i):
                self.assertRaises(i[1], pc.radius_hydraulic_rect, *i[0])

    def test_radius_hydraulic_general(self):
        self.assertWarns(
            UserWarning, pc.radius_hydraulic_general, *(6 * u.m ** 2, 12 * u.m)
        )

    def test_radius_hydraulic_channel(self):
        """radius_hydraulic_channel should return known results with known input."""
        checks = (
            ([6 * u.m ** 2, 12 * u.m], 0.5 * u.m),
            ([70 * u.m ** 2, 0.4 * u.m], 175 * u.m),
            ([40000 * u.m ** 2, 7 * u.m], 5714.285714285715 * u.m),
        )
        for i in checks:
            with self.subTest(i=i):
                self.assertAlmostEqualQuantity(
                    pc.radius_hydraulic_channel(*i[0]), i[1]
                )

    def test_radius_hydraulic_channel_range(self):
        """radius_hydraulic_channel should not accept inputs of 0 or less."""
        checks = ([0 * u.m ** 2, 6 * u.m], [6 * u.m ** 2, 0 * u.m])
        for i in checks:
            with self.subTest(i=i):
                self.assertRaises(ValueError, pc.radius_hydraulic_channel, *i)


class ReynoldsNumsTest(QuantityTest):
    """Test the various Reynolds Number functions."""

    def test_re_pipe(self):
        """re_pipe should return known results with known input."""
        checks = (
            (
                (12 * u.m ** 3 / u.s, 6 * u.m, 0.01 * u.m ** 2 / u.s),
                254.64790894703253,
            ),
            (
                (12000 * u.L / u.s, 600 * u.cm, 0.000001 * u.ha / u.s),
                254.64790894703253,
            ),
            (
                (60 * u.m ** 3 / u.s, 1 * u.m, 1 * u.m ** 2 / u.s),
                76.39437268410977,
            ),
            (
                (1 * u.m ** 3 / u.s, 12 * u.m, 0.45 * u.m ** 2 / u.s),
                0.23578510087688198,
            ),
        )
        for i in checks:
            with self.subTest(i=i):
                self.assertAlmostEqualQuantity(
                    pc.re_pipe(*i[0]), i[1] * u.dimensionless
                )

    def test_re_pipe_range(self):
        """re_pipe should raise errors when inputs are out of bounds."""
        checks = (
            (0 * u.m ** 3 / u.s, 4 * u.m, 0.5 * u.m ** 2 / u.s),
            (1 * u.m ** 3 / u.s, 0 * u.m, 0.4 * u.m ** 2 / u.s),
            (1 * u.m ** 3 / u.s, 1 * u.m, -0.1 * u.m ** 2 / u.s),
            (1 * u.m ** 3 / u.s, 1 * u.m, 0 * u.m ** 2 / u.s),
        )
        for i in checks:
            with self.subTest(i=i):
                self.assertRaises(ValueError, pc.re_pipe, *i)

    def test_re_rect(self):
        """re_rect should return known result with known input."""
        checks = (
            (
                (
                    10 * u.m ** 3 / u.s,
                    4 * u.m,
                    6 * u.m,
                    1 * u.m ** 2 / u.s,
                    True,
                ),
                2.5,
            ),
            (
                (
                    8 * u.m ** 3 / u.s,
                    10 * u.m,
                    4 * u.m,
                    0.6 * u.m ** 2 / u.s,
                    False,
                ),
                1.9047619047619049,
            ),
            (
                (10000 * u.L / u.s, 4 * u.m, 6 * u.m, 0.0001 * u.ha / u.s, True),
                2.5,
            ),
        )
        for i in checks:
            with self.subTest(i=i):
                self.assertAlmostEqualQuantity(
                    pc.re_rect(*i[0]), i[1] * u.dimensionless
                )

    def test_re_rect_range(self):
        """re_rect should raise errors when inputs are out of bounds."""
        checks = (
            (0 * u.m ** 3 / u.s, 1 * u.m, 1 * u.m, 1 * u.m ** 2 / u.s, False),
            (1 * u.m ** 3 / u.s, 1 * u.m, 1 * u.m, 0 * u.m ** 2 / u.s, False),
        )
        for i in checks:
            with self.subTest(i=i):
                self.assertRaises(ValueError, pc.re_rect, *i)

    def test_re_rect_warning(self):
        """re_rect should raise warnings when passed a deprecated parameter"""
        checks = (
            lambda: pc.re_rect(
                1 * u.m ** 3 / u.s, 1 * u.m, 1 * u.m, 1 * u.m ** 2 / u.s
            ),
            lambda: pc.re_rect(
                1 * u.m ** 3 / u.s,
                1 * u.m,
                1 * u.m,
                1 * u.m ** 2 / u.s,
                OpenChannel=False,
                openchannel=False,
            ),
        )
        for i in checks:
            with self.subTest(i=i):
                self.assertRaises(TypeError, i)

        self.assertWarns(
            UserWarning,
            lambda: pc.re_rect(
                1 * u.m ** 3 / u.s,
                1 * u.m,
                1 * u.m,
                1 * u.m ** 2 / u.s,
                openchannel=False,
            ),
        )

    def test_re_general(self):
        self.assertWarns(
            UserWarning,
            pc.re_general,
            *(1 * u.m / u.s, 2 * u.m ** 2, 3 * u.m, 0.4 * u.m ** 2 / u.s)
        )

    def test_re_channel(self):
        """re_channel should return known values with known input."""
        checks = (
            (
                [1 * u.m / u.s, 2 * u.m ** 2, 3 * u.m, 0.4 * u.m ** 2 / u.s],
                6.666666666666666,
            ),
            (
                [17 * u.m / u.s, 6 * u.m ** 2, 42 * u.m, 1 * u.m ** 2 / u.s],
                9.714285714285714,
            ),
            ([0 * u.m / u.s, 1 * u.m ** 2, 2 * u.m, 0.3 * u.m ** 2 / u.s], 0),
        )
        for i in checks:
            with self.subTest(i=i):
                self.assertAlmostEqualQuantity(
                    pc.re_channel(*i[0]), i[1] * u.dimensionless
                )

    def test_re_channel_range(self):
        """re_channel should raise errors when inputs are out of bounds."""
        checks = (
            (-1 * u.m / u.s, 2 * u.m ** 2, 3 * u.m, 0.4 * u.m ** 2 / u.s),
            (1 * u.m / u.s, 2 * u.m ** 2, 3 * u.m, 0 * u.m ** 2 / u.s),
        )
        for i in checks:
            with self.subTest(i=i):
                self.assertRaises(ValueError, pc.re_channel, *i)


class FrictionFuncsTest(QuantityTest):
    """Test the friction functions."""

    def test_fric(self):
        self.assertWarns(
            UserWarning,
            pc.fric,
            *(100 * u.m ** 3 / u.s, 2 * u.m, 0.001 * u.m ** 2 / u.s, 1 * u.m)
        )

    def test_fric_pipe(self):
        """fric_pipe should return known results with known input."""
        checks = (
            (
                [100 * u.m ** 3 / u.s, 2 * u.m, 0.001 * u.m ** 2 / u.s, 1 * u.m],
                0.33154589118654193,
            ),
            (
                [100 * u.m ** 3 / u.s, 2 * u.m, 0.1 * u.m ** 2 / u.s, 1 * u.m],
                0.10053096491487337,
            ),
            (
                [100 * u.m ** 3 / u.s, 2 * u.m, 0.001 * u.m ** 2 / u.s, 0 * u.m],
                0.019675384283293733,
            ),
            (
                [
                    46 * u.m ** 3 / u.s,
                    9 * u.m,
                    0.001 * u.m ** 2 / u.s,
                    0.03 * u.m,
                ],
                0.039382681891291252,
            ),
            (
                [
                    55 * u.m ** 3 / u.s,
                    0.4 * u.m,
                    0.5 * u.m ** 2 / u.s,
                    0.0001 * u.m,
                ],
                0.18278357257249706,
            ),
        )
        for i in checks:
            with self.subTest(i=i):
                self.assertAlmostEqualQuantity(
                    pc.fric_pipe(*i[0]), i[1] * u.dimensionless
                )

    def test_fric_range(self):
        """fric_pipe should raise an error if 0 <= Roughness is not true."""
        checks = (
            [1 * u.m ** 3 / u.s, 2 * u.m, 0.1 * u.m ** 2 / u.s, -0.1 * u.m],
        )
        for i in checks:
            with self.subTest(i=i):
                self.assertRaises(ValueError, pc.fric_pipe, *i)

    def test_fric_rect(self):
        """fric_rect should return known results with known inputs."""
        checks = (
            (
                [
                    60 * u.m ** 3 / u.s,
                    0.7 * u.m,
                    1 * u.m,
                    0.6 * u.m ** 2 / u.s,
                    0.001 * u.m,
                    True,
                ],
                0.432,
            ),
            (
                [
                    60 * u.m ** 3 / u.s,
                    0.7 * u.m,
                    1 * u.m,
                    0.6 * u.m ** 2 / u.s,
                    0.001 * u.m,
                    False,
                ],
                0.544,
            ),
            (
                [
                    120 * u.m ** 3 / u.s,
                    1 * u.m,
                    0.04 * u.m,
                    0.125 * u.m ** 2 / u.s,
                    0.6 * u.m,
                    True,
                ],
                150.90859874356411,
            ),
            (
                [
                    120 * u.m ** 3 / u.s,
                    1 * u.m,
                    0.04 * u.m,
                    0.125 * u.m ** 2 / u.s,
                    0.6 * u.m,
                    False,
                ],
                0.034666666666666665,
            ),
            (
                [
                    120 * u.m ** 3 / u.s,
                    1 * u.m,
                    0.04 * u.m,
                    0.125 * u.m ** 2 / u.s,
                    0 * u.m,
                    False,
                ],
                0.034666666666666665,
            ),
            (
                [
                    120 * u.m ** 3 / u.s,
                    1 * u.m,
                    0.04 * u.m,
                    0.125 * u.m ** 2 / u.s,
                    0 * u.m,
                    True,
                ],
                0.042098136441473824,
            ),
        )
        for i in checks:
            with self.subTest(i=i):
                self.assertAlmostEqualQuantity(
                    pc.fric_rect(*i[0]), i[1] * u.dimensionless
                )

    def test_fric_rect_range(self):
        """fric_rect should raise an error if 0 <= Roughness not true."""
        checks = (
            [
                1 * u.m ** 3 / u.s,
                1 * u.m,
                1 * u.m,
                1 * u.m ** 2 / u.s,
                -1.1 * u.m,
                True,
            ],
        )
        for i in checks:
            with self.subTest(i=i):
                self.assertRaises(ValueError, pc.fric_rect, *i)

    def test_fric_rect_warning(self):
        """fric_rect should raise warnings when passed deprecated parameters"""
        error_checks = (
            lambda: pc.fric_rect(
                1 * u.m ** 3 / u.s,
                1 * u.m,
                1 * u.m,
                1 * u.m ** 2 / u.s,
                Roughness=1 * u.m,
                PipeRough=1 * u.m,
                OpenChannel=True,
            ),
            lambda: pc.fric_rect(
                1 * u.m ** 3 / u.s,
                1 * u.m,
                1 * u.m,
                1 * u.m ** 2 / u.s,
                1 * u.m,
                OpenChannel=True,
                openchannel=True,
            ),
        )
        for i in error_checks:
            with self.subTest(i=i):
                self.assertRaises(TypeError, i)

        warning_checks = (
            lambda: pc.fric_rect(
                1 * u.m ** 3 / u.s,
                1 * u.m,
                1 * u.m,
                1 * u.m ** 2 / u.s,
                PipeRough=1 * u.m,
                OpenChannel=True,
            ),
            lambda: pc.fric_rect(
                1 * u.m ** 3 / u.s,
                1 * u.m,
                1 * u.m,
                1 * u.m ** 2 / u.s,
                PipeRough=1 * u.m,
                openchannel=True,
            ),
            lambda: pc.fric_rect(
                1 * u.m ** 3 / u.s,
                1 * u.m,
                1 * u.m,
                1 * u.m ** 2 / u.s,
                1 * u.m,
                openchannel=True,
            ),
        )
        for i in warning_checks:
            with self.subTest(i=i):
                self.assertWarns(UserWarning, i)

    def test_fric_general(self):
        self.assertWarns(
            UserWarning,
            pc.fric_general,
            *(
                9 * u.m ** 2,
                0.67 * u.m,
                3 * u.m / u.s,
                0.987 * u.m ** 2 / u.s,
                0.86 * u.m,
            )
        )

    def test_fric_channel(self):
        """fric_channel should return known results with known inputs."""
        checks = (
            (
                [
                    9 * u.m ** 2,
                    0.67 * u.m,
                    3 * u.m / u.s,
                    0.987 * u.m ** 2 / u.s,
                    0.86 * u.m,
                ],
                0.3918755555555556,
            ),
            (
                [
                    1 * u.m ** 2,
                    1 * u.m,
                    1 * u.m / u.s,
                    1 * u.m ** 2 / u.s,
                    1 * u.m,
                ],
                16,
            ),
            (
                [
                    120 * u.m ** 2,
                    0.6 * u.m,
                    12 * u.m / u.s,
                    0.3 * u.m ** 2 / u.s,
                    0.002 * u.m,
                ],
                0.023024557179148988,
            ),
        )
        for i in checks:
            with self.subTest(i=i):
                self.assertAlmostEqualQuantity(
                    pc.fric_channel(*i[0]), i[1] * u.dimensionless
                )

    def test_fric_channel_range(self):
        """fric_channel should raise an error if 0 <= Roughness is not true."""
        checks = (
            (
                1 * u.m ** 2,
                1 * u.m,
                1 * u.m / u.s,
                1 * u.m ** 2 / u.s,
                -0.0001 * u.m,
            ),
        )
        for i in checks:
            with self.subTest(i=i):
                self.assertRaises(ValueError, pc.fric_channel, *i)


class HeadlossFuncsTest(QuantityTest):
    """Test the headloss functions."""

    def test_headloss_fric(self):
        self.assertWarns(
            UserWarning,
            pc.headloss_fric,
            *(
                100 * u.m ** 3 / u.s,
                2 * u.m,
                4 * u.m,
                0.001 * u.m ** 2 / u.s,
                1 * u.m,
            )
        )

    def test_headloss_major_pipe(self):
        """headloss_major_pipe should return known results with known inputs."""
        checks = (
            (
                [
                    100 * u.m ** 3 / u.s,
                    2 * u.m,
                    4 * u.m,
                    0.001 * u.m ** 2 / u.s,
                    1 * u.m,
                ],
                34.2549414191127 * u.m,
            ),
            (
                [
                    100 * u.m ** 3 / u.s,
                    2 * u.m,
                    4 * u.m,
                    0.1 * u.m ** 2 / u.s,
                    1 * u.m,
                ],
                10.386744054168654 * u.m,
            ),
            (
                [
                    100 * u.m ** 3 / u.s,
                    2 * u.m,
                    4 * u.m,
                    0.001 * u.m ** 2 / u.s,
                    0 * u.m,
                ],
                2.032838149828097 * u.m,
            ),
            (
                [
                    46 * u.m ** 3 / u.s,
                    9 * u.m,
                    12 * u.m,
                    0.001 * u.m ** 2 / u.s,
                    0.03 * u.m,
                ],
                0.001399778168304583 * u.m,
            ),
            (
                [
                    55 * u.m ** 3 / u.s,
                    0.4 * u.m,
                    2 * u.m,
                    0.5 * u.m ** 2 / u.s,
                    0.0001 * u.m,
                ],
                8926.108171551185 * u.m,
            ),
        )
        for i in checks:
            with self.subTest(i=i):
                self.assertAlmostEqualQuantity(
                    pc.headloss_major_pipe(*i[0]), i[1]
                )

    def test_headloss_major_pipe_range(self):
        """headloss_major_pipe should raise an error if Length <= 0."""
        checks = (
            [1 * u.m ** 3 / u.s, 1 * u.m, 0 * u.m, 1 * u.m ** 2 / u.s, 1 * u.m],
            [1 * u.m ** 3 / u.s, 1 * u.m, -1 * u.m, 1 * u.m ** 2 / u.s, 1 * u.m],
        )
        for i in checks:
            with self.subTest(i=i):
                self.assertRaises(ValueError, pc.headloss_major_pipe, *i)

    def test_headloss_exp(self):
        self.assertWarns(
            UserWarning,
            pc.headloss_exp,
            *(60 * u.m ** 3 / u.s, 0.9 * u.m, 0.067)
        )

    def test_headloss_minor_pipe(self):
        """headloss_minor_pipe should return known results with known input."""
        checks = (
            ([60 * u.m ** 3 / u.s, 0.9 * u.m, 0.067], 30.386230766265214 * u.m),
            (
                [60 * u.m ** 3 / u.s, 0.9 * u.m, 0.067 * u.dimensionless],
                30.386230766265214 * u.m,
            ),
        )
        for i in checks:
            with self.subTest(i=i):
                self.assertAlmostEqualQuantity(
                    pc.headloss_minor_pipe(*i[0]), i[1]
                )

    def test_headloss_minor_pipe_range(self):
        """headloss_minor_pipe should raise errors when inputs are out of bounds."""
        checks = (
            [0 * u.m ** 3 / u.s, 1 * u.m, 1],
            [1 * u.m ** 3 / u.s, 0 * u.m, 1],
            [1 * u.m ** 3 / u.s, 1 * u.m, -1],
        )
        for i in checks:
            with self.subTest(i=i):
                self.assertRaises(ValueError, pc.headloss_minor_pipe, *i)

    def test_headloss(self):
        self.assertWarns(
            UserWarning,
            pc.headloss,
            *(
                100 * u.m ** 3 / u.s,
                2 * u.m,
                4 * u.m,
                0.001 * u.m ** 2 / u.s,
                1 * u.m,
                2,
            )
        )

    def test_headloss_pipe(self):
        """headloss_pipe should return known results with known inputs."""
        checks = (
            (
                [
                    100 * u.m ** 3 / u.s,
                    2 * u.m,
                    4 * u.m,
                    0.001 * u.m ** 2 / u.s,
                    1 * u.m,
                    2,
                ],
                137.57379509731857 * u.m,
            ),
            (
                [
                    100 * u.m ** 3 / u.s,
                    2 * u.m,
                    4 * u.m,
                    0.1 * u.m ** 2 / u.s,
                    1 * u.m,
                    0.4,
                ],
                31.05051478980984 * u.m,
            ),
            (
                [
                    100 * u.m ** 3 / u.s,
                    2 * u.m,
                    4 * u.m,
                    0.001 * u.m ** 2 / u.s,
                    0 * u.m,
                    1.2,
                ],
                64.024150356751633 * u.m,
            ),
            (
                [
                    46 * u.m ** 3 / u.s,
                    9 * u.m,
                    12 * u.m,
                    0.001 * u.m ** 2 / u.s,
                    0.03 * u.m,
                    4,
                ],
                0.10802874052554703 * u.m,
            ),
            (
                [
                    55 * u.m ** 3 / u.s,
                    0.4 * u.m,
                    2 * u.m,
                    0.5 * u.m ** 2 / u.s,
                    0.0001 * u.m,
                    0.12,
                ],
                10098.131417963332 * u.m,
            ),
        )
        for i in checks:
            with self.subTest(i=i):
                self.assertAlmostEqualQuantity(pc.headloss_pipe(*i[0]), i[1])

    def test_headloss_fric_rect(self):
        self.assertWarns(
            UserWarning,
            pc.headloss_fric_rect,
            *(
                0.06 * u.m ** 3 / u.s,
                3 * u.m,
                0.2 * u.m,
                4 * u.m,
                0.5 * u.m ** 2 / u.s,
                0.006 * u.m,
                True,
            )
        )

    def test_headloss_major_rect(self):
        """headloss_major_rect should return known result with known inputs."""
        checks = (
            (
                [
                    0.06 * u.m ** 3 / u.s,
                    3 * u.m,
                    0.2 * u.m,
                    4 * u.m,
                    0.5 * u.m ** 2 / u.s,
                    0.006 * u.m,
                    True,
                ],
                1.3097688246694272 * u.m,
            ),
            (
                [
                    0.06 * u.m ** 3 / u.s,
                    3 * u.m,
                    0.2 * u.m,
                    4 * u.m,
                    0.5 * u.m ** 2 / u.s,
                    0.006 * u.m,
                    False,
                ],
                4.640841787063992 * u.m,
            ),
        )
        for i in checks:
            with self.subTest(i=i):
                self.assertAlmostEqualQuantity(
                    pc.headloss_major_rect(*i[0]), i[1]
                )

    def test_headloss_major_rect_range(self):
        """headloss_major_rect should raise an error when Length <=0."""
        checks = (
            (
                1 * u.m ** 3 / u.s,
                1 * u.m,
                1 * u.m,
                0 * u.m,
                1 * u.m ** 2 / u.s,
                1 * u.m,
                1,
            ),
            (
                1 * u.m ** 3 / u.s,
                1 * u.m,
                1 * u.m,
                -1 * u.m,
                1 * u.m ** 2 / u.s,
                1 * u.m,
                1,
            ),
        )
        for i in checks:
            with self.subTest(i=i):
                self.assertRaises(ValueError, pc.headloss_major_rect, *i)

    def test_headloss_exp_rect(self):
        self.assertWarns(
            UserWarning,
            pc.headloss_exp_rect,
            *(0.06 * u.m ** 3 / u.s, 2 * u.m, 0.004 * u.m, 1)
        )

    def test_headloss_minor_rect(self):
        """headloss_minor_rect should return known result for known input."""
        checks = (
            [0.06 * u.m ** 3 / u.s, 2 * u.m, 0.004 * u.m, 1],
            2.8679518490004234 * u.m,
        )
        self.assertAlmostEqualQuantity(
            pc.headloss_minor_rect(*checks[0]), checks[1]
        )

    def test_headloss_minor_rect_range(self):
        """headloss_minor_rect should raise errors when inputs are out of bounds."""
        checks = (
            (0 * u.m ** 3 / u.s, 1 * u.m, 1 * u.m, 1),
            (1 * u.m ** 3 / u.s, 0 * u.m, 1 * u.m, 1),
            (1 * u.m ** 3 / u.s, 1 * u.m, 0 * u.m, 1),
            (1 * u.m ** 3 / u.s, 1 * u.m, 1 * u.m, -1),
        )
        for i in checks:
            with self.subTest(i=i):
                self.assertRaises(ValueError, pc.headloss_minor_rect, *i)

    def test_headloss_rect(self):
        """headloss_rect should return known result for known inputs."""
        checks = (
            (
                [
                    0.06 * u.m ** 3 / u.s,
                    3 * u.m,
                    0.2 * u.m,
                    4 * u.m,
                    1 * u.dimensionless,
                    0.5 * u.m ** 2 / u.s,
                    0.006 * u.m,
                    True,
                ],
                1.3102786827759163 * u.m,
            ),
            (
                [
                    0.06 * u.m ** 3 / u.s,
                    3 * u.m,
                    0.2 * u.m,
                    4 * u.m,
                    1,
                    0.5 * u.m ** 2 / u.s,
                    0.006 * u.m,
                    False,
                ],
                4.641351645170481 * u.m,
            ),
        )
        for i in checks:
            with self.subTest(i=i):
                self.assertAlmostEqualQuantity(pc.headloss_rect(*i[0]), i[1])

    def test_headloss_rect_warning(self):
        """headloss_rect should raise warnings when passed deprecated parameters"""
        error_checks = (
            lambda: pc.headloss_rect(
                1 * u.m ** 3 / u.s,
                1 * u.m,
                1 * u.m,
                4 * u.m,
                1 * u.dimensionless,
                1 * u.m ** 2 / u.s,
                Roughness=1 * u.m,
                PipeRough=1 * u.m,
                OpenChannel=True,
            ),
            lambda: pc.headloss_rect(
                1 * u.m ** 3 / u.s,
                1 * u.m,
                1 * u.m,
                4 * u.m,
                1 * u.dimensionless,
                1 * u.m ** 2 / u.s,
                1 * u.m,
                OpenChannel=True,
                openchannel=True,
            ),
        )
        for i in error_checks:
            with self.subTest(i=i):
                self.assertRaises(TypeError, i)

        warning_checks = (
            lambda: pc.headloss_rect(
                1 * u.m ** 3 / u.s,
                1 * u.m,
                1 * u.m,
                4 * u.m,
                1 * u.dimensionless,
                1 * u.m ** 2 / u.s,
                PipeRough=1 * u.m,
                OpenChannel=True,
            ),
            lambda: pc.headloss_rect(
                1 * u.m ** 3 / u.s,
                1 * u.m,
                1 * u.m,
                4 * u.m,
                1 * u.dimensionless,
                1 * u.m ** 2 / u.s,
                PipeRough=1 * u.m,
                openchannel=True,
            ),
            lambda: pc.headloss_rect(
                1 * u.m ** 3 / u.s,
                1 * u.m,
                1 * u.m,
                4 * u.m,
                1 * u.dimensionless,
                1 * u.m ** 2 / u.s,
                1 * u.m,
                openchannel=True,
            ),
        )
        for i in warning_checks:
            with self.subTest(i=i):
                self.assertWarns(UserWarning, i)

    def test_headloss_fric_general(self):
        self.assertWarns(
            UserWarning,
            pc.headloss_fric_general,
            *(
                1 * u.m ** 2,
                1 * u.m,
                1 * u.m / u.s,
                1 * u.m,
                1 * u.m ** 2 / u.s,
                1 * u.m,
            )
        )

    def test_headloss_major_channel(self):
        """headloss_major_channel should return known result for known inputs."""
        checks = (
            (
                [
                    1 * u.m ** 2,
                    1 * u.m,
                    1 * u.m / u.s,
                    1 * u.m,
                    1 * u.m ** 2 / u.s,
                    1 * u.m,
                ],
                0.20394324259558566 * u.m,
            ),
            (
                [
                    25 * u.m ** 2,
                    4 * u.m,
                    0.6 * u.m / u.s,
                    2 * u.m,
                    1 * u.m ** 2 / u.s,
                    1 * u.m,
                ],
                0.006265136412536391 * u.m,
            ),
        )
        for i in checks:
            with self.subTest(i=i):
                self.assertAlmostEqualQuantity(
                    pc.headloss_major_channel(*i[0]), i[1]
                )

    def test_headloss_major_channel_range(self):
        """headloss_major_channel should raise an error when Length <= 0."""
        checks = (
            [
                1 * u.m ** 2,
                1 * u.m,
                1 * u.m / u.s,
                0 * u.m,
                1 * u.m ** 2 / u.s,
                1 * u.m,
            ],
            [
                15 * u.m ** 2,
                1 * u.m,
                1 * u.m / u.s,
                -1 * u.m,
                1 * u.m ** 2 / u.s,
                1 * u.m,
            ],
        )
        for i in checks:
            with self.subTest(i=i):
                self.assertRaises(ValueError, pc.headloss_major_channel, *i)

    def test_headloss_exp_general(self):
        self.assertWarns(
            UserWarning, pc.headloss_exp_general, *(0.06 * u.m / u.s, 0.02)
        )

    def test_headloss_minor_channel(self):
        """headloss_minor_channel should return known result for known input."""
        self.assertAlmostEqualQuantity(
            pc.headloss_minor_channel(0.06 * u.m / u.s, 0.02),
            3.670978366720542e-06 * u.m,
        )

    def test_headloss_minor_channel_range(self):
        """headloss_minor_channel should raise errors if inputs are out of bounds."""
        checks = ((0 * u.m / u.s, 1), (1 * u.m / u.s, -1 * u.dimensionless))
        for i in checks:
            with self.subTest(i=i):
                self.assertRaises(ValueError, pc.headloss_minor_channel, *i)

    def test_headloss_gen(self):
        self.assertWarns(
            UserWarning,
            pc.headloss_gen,
            *(
                36 * u.m ** 2,
                0.1 * u.m / u.s,
                4 * u.m,
                6 * u.m,
                0.02,
                0.86 * u.m ** 2 / u.s,
                0.0045 * u.m,
            )
        )

    def test_headloss_channel(self):
        """headloss_channel should return known value for known inputs."""
        checks = (
            (
                [
                    36 * u.m ** 2,
                    0.1 * u.m / u.s,
                    4 * u.m,
                    6 * u.m,
                    0.02,
                    0.86 * u.m ** 2 / u.s,
                    0.0045 * u.m,
                ],
                0.0013093911519979546 * u.m,
            ),
            (
                [
                    49 * u.m ** 2,
                    2.4 * u.m / u.s,
                    12 * u.m,
                    3 * u.m,
                    2 * u.dimensionless,
                    4 * u.m ** 2 / u.s,
                    0.6 * u.m,
                ],
                0.9396236839032805 * u.m,
            ),
        )
        for i in checks:
            with self.subTest(i=i):
                self.assertAlmostEqualQuantity(pc.headloss_channel(*i[0]), i[1])

    def test_headloss_manifold(self):
        """headloss_manifold should return known value for known input."""
        checks = (
            (
                [
                    0.12 * u.m ** 3 / u.s,
                    0.4 * u.m,
                    6 * u.m,
                    0.8,
                    0.75 * u.m ** 2 / u.s,
                    0.0003 * u.m,
                    5,
                ],
                38.57715300752375 * u.m,
            ),
            (
                [
                    2 * u.m ** 3 / u.s,
                    6 * u.m,
                    40 * u.m,
                    5,
                    1.1 * u.m ** 2 / u.s,
                    0.04 * u.m,
                    6,
                ],
                0.11938889890999548 * u.m,
            ),
        )
        for i in checks:
            with self.subTest(i=i):
                self.assertAlmostEqualQuantity(pc.headloss_manifold(*i[0]), i[1])

    def test_headloss_manifold_range(self):
        """headloss_manifold should object if NumOutlets is not a positive int."""
        failChecks = (
            (
                1 * u.m ** 3 / u.s,
                1 * u.m,
                1 * u.m,
                1,
                1 * u.m ** 2 / u.s,
                1 * u.m,
                -1,
            ),
            (
                1 * u.m ** 3 / u.s,
                1 * u.m,
                1 * u.m,
                1,
                1 * u.m ** 2 / u.s,
                1 * u.m,
                0,
            ),
            (
                1 * u.m ** 3 / u.s,
                1 * u.m,
                1 * u.m,
                1,
                1 * u.m ** 2 / u.s,
                1 * u.m,
                0.1,
            ),
        )
        passchecks = (
            (
                1 * u.m ** 3 / u.s,
                1 * u.m,
                1 * u.m,
                1,
                1 * u.m ** 2 / u.s,
                1 * u.m,
                1.0,
            ),
            (
                1 * u.m ** 3 / u.s,
                1 * u.m,
                1 * u.m,
                1,
                1 * u.m ** 2 / u.s,
                1 * u.m,
                47,
            ),
        )
        for i in failChecks:
            with self.subTest(i=i):
                self.assertRaises(
                    (ValueError, TypeError), pc.headloss_manifold, *i
                )
        for i in passchecks:
            with self.subTest(i=i):
                pc.headloss_manifold(*i)

    def test_headloss_manifold_warning(self):
        """headloss_manifold should raise warnings when passed deprecated parameters"""
        error_checks = (
            lambda: pc.headloss_manifold(
                1 * u.m ** 3 / u.s,
                1 * u.m,
                1 * u.m,
                1,
                1 * u.m ** 2 / u.s,
                Roughness=1 * u.m,
                NumOutlets=1,
                PipeRough=1 * u.m,
            ),
            lambda: pc.headloss_manifold(
                1 * u.m ** 3 / u.s,
                1 * u.m,
                1 * u.m,
                1,
                1 * u.m ** 2 / u.s,
                NumOutlets=1,
            ),
            lambda: pc.headloss_manifold(
                1 * u.m ** 3 / u.s,
                1 * u.m,
                1 * u.m,
                1,
                1 * u.m ** 2 / u.s,
                Roughness=1 * u.m,
            ),
        )
        for i in error_checks:
            with self.subTest(i=i):
                self.assertRaises(TypeError, i)

        warning_checks = (
            lambda: pc.headloss_manifold(
                1 * u.m ** 3 / u.s,
                1 * u.m,
                1 * u.m,
                1,
                1 * u.m ** 2 / u.s,
                PipeRough=1 * u.m,
                NumOutlets=1,
            ),
        )

        for i in warning_checks:
            with self.subTest(i=i):
                self.assertWarns(UserWarning, i)

    def test_elbow_minor_loss(self):
        self.assertWarns(
            UserWarning,
            pc.elbow_minor_loss,
            *(0.1 * u.m ** 3 / u.s, 0.1 * u.m, 0.5)
        )

    def test_headloss_minor_elbow(self):
        checks = (
            ([0.1 * u.m ** 3 / u.s, 0.1 * u.m, 0.5], 4.132754147128235 * u.m),
            ([0.4 * u.m ** 3 / u.s, 0.3 * u.m, 0.2], 0.32653859927926804 * u.m),
        )
        for i in checks:
            with self.subTest(i=i):
                self.assertAlmostEqualQuantity(
                    pc.headloss_minor_elbow(*i[0]), i[1]
                )


class OrificeFuncsTest(QuantityTest):
    """Test the orifice functions."""

    def test_flow_orifice(self):
        """flow_orifice should return known result for known input."""
        checks = (
            ([0.4 * u.m, 2 * u.m, 0.46], 0.36204122788069698 * u.m ** 3 / u.s),
            ([2 * u.m, 0.04 * u.m, 0.2], 0.55652566805118475 * u.m ** 3 / u.s),
            ([7 * u.m, 0 * u.m, 1 * u.dimensionless], 0 * u.m ** 3 / u.s),
            ([1.4 * u.m, 0.1 * u.m, 0], 0 * u.m ** 3 / u.s),
        )
        for i in checks:
            with self.subTest(i=i):
                self.assertAlmostEqualQuantity(pc.flow_orifice(*i[0]), i[1])

    def test_flow_orifice_range(self):
        """flow_orifice should raise errors when inputs are out of bounds."""
        checks = (
            (0 * u.m, 1 * u.m, 1),
            (1 * u.m, 1 * u.m, 1.1),
            (1 * u.m, 1 * u.m, -1),
        )
        for i in checks:
            with self.subTest(i=i):
                self.assertRaises(ValueError, pc.flow_orifice, *i)

    def test_flow_orifice_vert(self):
        """flow_orifice_vert should return known values for known inputs."""
        checks = (
            ([1 * u.m, 3 * u.m, 0.4], 2.4077258053173911 * u.m ** 3 / u.s),
            ([0.3 * u.m, 4 * u.m, 0.67], 0.41946278400781861 * u.m ** 3 / u.s),
            ([2 * u.m, -4 * u.m, 0.2 * u.dimensionless], 0 * u.m ** 3 / u.s),
        )
        for i in checks:
            with self.subTest(i=i):
                self.assertAlmostEqualQuantity(pc.flow_orifice_vert(*i[0]), i[1])

    def test_flow_orifice_vert_range(self):
        """flow_orifice_vert should raise errors when inputs are out of bounds."""
        errorChecks = ((1 * u.m, 1 * u.m, -1), (1 * u.m, 1 * u.m, 2))
        errorlessChecks = (
            (1 * u.m, 1 * u.m, 1),
            (1 * u.m, 1 * u.m, 0),
            (1 * u.m, 1 * u.m, 0.5),
        )
        for i in errorChecks:
            with self.subTest(i=i):
                self.assertRaises(ValueError, pc.flow_orifice_vert, *i)
        for i in errorlessChecks:
            with self.subTest(i=i):
                pc.flow_orifice_vert(*i)

    def test_head_orifice(self):
        """head_orifice should return known value for known inputs."""
        checks = (
            ([1 * u.m, 1, 1 * u.m ** 3 / u.s], 0.08265508294256473 * u.m),
            ([1.2 * u.m, 0.1, 0.12 * u.m ** 3 / u.s], 0.05739936315455882 * u.m),
            (
                [2 * u.m, 0.5 * u.dimensionless, 0.04 * u.m ** 3 / u.s],
                3.3062033177025895e-05 * u.m,
            ),
        )
        for i in checks:
            with self.subTest(i=i):
                self.assertAlmostEqualQuantity(pc.head_orifice(*i[0]), i[1])

    def test_head_orifice_range(self):
        """head_orifice should raise errors when passed invalid inputs."""
        failChecks = (
            (0 * u.m, 1, 1 * u.m ** 3 / u.s),
            (1 * u.m, 1, 0 * u.m ** 3 / u.s),
            (1 * u.m, -1, 1 * u.m ** 3 / u.s),
            (1 * u.m, 2, 1 * u.m ** 3 / u.s),
        )
        for i in failChecks:
            with self.subTest(i=i):
                self.assertRaises(ValueError, pc.head_orifice, *i)
        self.assertRaises(
            ZeroDivisionError, pc.head_orifice, *(1 * u.m, 0, 1 * u.m ** 3 / u.s)
        )

    def test_area_orifice(self):
        """area_orifice should return known value for known inputs."""
        checks = (
            (
                [3 * u.m, 0.4, 0.06 * u.m ** 3 / u.s],
                0.019554886342464974 * u.m ** 2,
            ),
            (
                [2 * u.m, 0.1, 0.1 * u.m ** 3 / u.s],
                0.15966497839052934 * u.m ** 2,
            ),
            (
                [0.5 * u.m, 0.02 * u.dimensionless, 3 * u.m ** 3 / u.s],
                47.899493517158803 * u.m ** 2,
            ),
        )
        for i in checks:
            with self.subTest(i=i):
                self.assertAlmostEqualQuantity(pc.area_orifice(*i[0]), i[1])

    def test_area_orifice_range(self):
        """area_orifice should raise errors when inputs are out of bounds."""
        failChecks = (
            (0 * u.m, 1, 1 * u.m ** 3 / u.s),
            (1 * u.m, 1, 0 * u.m ** 3 / u.s),
            (1 * u.m, -1, 1 * u.m ** 3 / u.s),
            (1 * u.m, 2, 1 * u.m ** 3 / u.s),
            (1 * u.m, 0, 1 * u.m ** 3 / u.s),
        )
        for i in failChecks:
            with self.subTest(i=i):
                self.assertRaises(ValueError, pc.area_orifice, *i)

    def test_num_orifices(self):
        """num_orifices should return known value for known inputs."""
        checks = (
            (
                [0.12 * u.m ** 3 / u.s, 0.04, 0.05 * u.m, 2 * u.m],
                1 * u.dimensionless,
            ),
            (
                [6 * u.m ** 3 / u.s, 0.8, 0.08 * u.m, 1.2 * u.m],
                6 * u.dimensionless,
            ),
        )
        for i in checks:
            with self.subTest(i=i):
                self.assertAlmostEqualQuantity(pc.num_orifices(*i[0]), i[1])


class FlowFuncsTest(QuantityTest):
    """Test the flow functions."""

    def test_flow_transition(self):
        """flow_transition should return known value for known inputs."""
        checks = (
            (
                [2 * u.m, 0.4 * u.m ** 2 / u.s],
                1319.4689145077132 * u.m ** 3 / u.s,
            ),
            (
                [0.8 * u.m, 1.1 * u.m ** 2 / u.s],
                1451.4158059584847 * u.m ** 3 / u.s,
            ),
        )
        for i in checks:
            with self.subTest(i=i):
                self.assertAlmostEqualQuantity(pc.flow_transition(*i[0]), i[1])

    def test_flow_transition_range(self):
        """flow_transition should not accept inputs <= 0."""
        checks = ((1 * u.m, 0 * u.m ** 2 / u.s), (0 * u.m, 1 * u.m ** 2 / u.s))
        for i in checks:
            with self.subTest(i=i):
                self.assertRaises(ValueError, pc.flow_transition, *i)

    def test_flow_hagen(self):
        """flow_hagen should return known value for known inputs."""
        checks = (
            (
                [1 * u.m, 0.4 * u.m, 5.21 * u.m, 0.6 * u.m ** 2 / u.s],
                0.03079864403023667 * u.m ** 3 / u.s,
            ),
            (
                [0.05 * u.m, 0.0006 * u.m, 0.3 * u.m, 1.1 * u.m ** 2 / u.s],
                2.7351295806397676e-09 * u.m ** 3 / u.s,
            ),
        )
        for i in checks:
            with self.subTest(i=i):
                self.assertAlmostEqualQuantity(pc.flow_hagen(*i[0]), i[1])

    def test_flow_hagen_range(self):
        """flow_hagen should raise errors when inputs are out of bounds."""
        failChecks = (
            (0 * u.m, 1 * u.m, 1 * u.m, 1 * u.m ** 2 / u.s),
            (1 * u.m, -1 * u.m, 1 * u.m, 1 * u.m ** 2 / u.s),
            (1 * u.m, 1 * u.m, 0 * u.m, 1 * u.m ** 2 / u.s),
            (1 * u.m, 1 * u.m, 1 * u.m, 0 * u.m ** 2 / u.s),
        )
        for i in failChecks:
            with self.subTest(i=i):
                self.assertRaises(ValueError, pc.flow_hagen, *i)
        passChecks = (
            (1 * u.m, 1 * u.m, 1 * u.m, 1 * u.m ** 2 / u.s),
            (1 * u.m, 0 * u.m, 1 * u.m, 1 * u.m ** 2 / u.s),
        )
        for i in passChecks:
            with self.subTest(i=i):
                pc.flow_hagen(*i)

    def test_flow_hagen_warning(self):
        """flow_hagen should raise warnings when passed deprecated parameters"""
        error_checks = (
            lambda: pc.flow_hagen(
                1 * u.m,
                HeadLossMajor=1 * u.m,
                Length=1 * u.m,
                Nu=1 * u.m ** 2 / u.s,
                HeadLossFric=1 * u.m,
            ),
            lambda: pc.flow_hagen(
                1 * u.m, Length=1 * u.m, Nu=1 * u.m ** 2 / u.s
            ),
            lambda: pc.flow_hagen(
                1 * u.m, HeadLossMajor=1 * u.m, Nu=1 * u.m ** 2 / u.s
            ),
            lambda: pc.flow_hagen(
                1 * u.m, HeadLossMajor=1 * u.m, Length=1 * u.m
            ),
        )
        for i in error_checks:
            with self.subTest(i=i):
                self.assertRaises(TypeError, i)

        warning_checks = (
            lambda: pc.flow_hagen(
                1 * u.m,
                HeadLossFric=1 * u.m,
                Length=1 * u.m,
                Nu=1 * u.m ** 2 / u.s,
            ),
        )
        for i in warning_checks:
            with self.subTest(i=i):
                self.assertWarns(UserWarning, i)

    def test_flow_swamee(self):
        """flow_swamee should return known value for known inputs."""
        checks = (
            (
                [2 * u.m, 0.04 * u.m, 3 * u.m, 0.1 * u.m ** 2 / u.s, 0.37 * u.m],
                2.9565931732010045 * u.m ** 3 / u.s,
            ),
        )
        for i in checks:
            with self.subTest(i=i):
                self.assertAlmostEqualQuantity(pc.flow_swamee(*i[0]), i[1])

    def test_flow_swamee_range(self):
        """flow_swamee should raise errors when inputs are out of bounds."""
        failChecks = (
            (0 * u.m, 1 * u.m, 1 * u.m, 1 * u.m ** 2 / u.s, 1 * u.m),
            (1 * u.m, 0 * u.m, 1 * u.m, 1 * u.m ** 2 / u.s, 1 * u.m),
            (1 * u.m, 1 * u.m, 0 * u.m, 1 * u.m ** 2 / u.s, 1 * u.m),
            (1 * u.m, 1 * u.m, 1 * u.m, 0 * u.m ** 2 / u.s, 1 * u.m),
            (1 * u.m, 1 * u.m, 1 * u.m, 1 * u.m ** 2 / u.s, -0.1 * u.m),
            (1 * u.m, 1 * u.m, 1 * u.m, 1 * u.m ** 2 / u.s, -2 * u.m),
        )
        for i in failChecks:
            with self.subTest(i=i):
                self.assertRaises(ValueError, pc.flow_swamee, *i)
        passChecks = (
            (1 * u.m, 1 * u.m, 1 * u.m, 1 * u.m ** 2 / u.s, 1 * u.m),
            (1 * u.m, 1 * u.m, 1 * u.m, 1 * u.m ** 2 / u.s, 0 * u.m),
        )
        for i in passChecks:
            with self.subTest(i=i):
                pc.flow_swamee(*i)

    def test_flow_swamee_warning(self):
        """flow_swamee should raise warnings when passed deprecated parameters"""
        error_checks = (
            lambda: pc.flow_swamee(
                1 * u.m,
                HeadLossMajor=1 * u.m,
                Length=1 * u.m,
                Nu=1 * u.m ** 2 / u.s,
                Roughness=1 * u.m,
                HeadLossFric=1 * u.m,
            ),
            lambda: pc.flow_swamee(
                1 * u.m, Length=1 * u.m, Nu=1 * u.m ** 2 / u.s, Roughness=1 * u.m
            ),
            lambda: pc.flow_swamee(
                1 * u.m,
                HeadLossMajor=1 * u.m,
                Nu=1 * u.m ** 2 / u.s,
                Roughness=1 * u.m,
            ),
            lambda: pc.flow_swamee(
                1 * u.m, HeadLossMajor=1 * u.m, Length=1 * u.m, Roughness=1 * u.m
            ),
            lambda: pc.flow_swamee(
                1 * u.m,
                HeadLossMajor=1 * u.m,
                Length=1 * u.m,
                Nu=1 * u.m ** 2 / u.s,
                Roughness=1 * u.m,
                PipeRough=1 * u.m,
            ),
            lambda: pc.flow_swamee(
                1 * u.m,
                HeadLossMajor=1 * u.m,
                Length=1 * u.m,
                Nu=1 * u.m ** 2 / u.s,
            ),
        )
        for i in error_checks:
            with self.subTest(i=i):
                self.assertRaises(TypeError, i)

        warning_checks = (
            lambda: pc.flow_swamee(
                1 * u.m,
                HeadLossFric=1 * u.m,
                Length=1 * u.m,
                Nu=1 * u.m ** 2 / u.s,
                Roughness=1 * u.m,
            ),
            lambda: pc.flow_swamee(
                1 * u.m,
                HeadLossMajor=1 * u.m,
                Length=1 * u.m,
                Nu=1 * u.m ** 2 / u.s,
                PipeRough=1 * u.m,
            ),
        )
        for i in warning_checks:
            with self.subTest(i=i):
                self.assertWarns(UserWarning, i)

    def test_flow_pipemajor(self):
        self.assertWarns(
            UserWarning,
            pc.flow_pipemajor,
            *(1 * u.m, 0.97 * u.m, 0.5 * u.m, 0.025 * u.m ** 2 / u.s, 0.06 * u.m)
        )

    def test_flow_major_pipe(self):
        """flow_major_pipe should return known result for known inputs."""
        checks = (
            (
                [
                    1 * u.m,
                    0.97 * u.m,
                    0.5 * u.m,
                    0.025 * u.m ** 2 / u.s,
                    0.06 * u.m,
                ],
                18.677652880272845 * u.m ** 3 / u.s,
            ),
            (
                [
                    2 * u.m,
                    0.62 * u.m,
                    0.5 * u.m,
                    0.036 * u.m ** 2 / u.s,
                    0.23 * u.m,
                ],
                62.457206502701297 * u.m ** 3 / u.s,
            ),
        )
        for i in checks:
            with self.subTest(i=i):
                self.assertAlmostEqualQuantity(pc.flow_major_pipe(*i[0]), i[1])

    def test_flow_pipeminor(self):
        self.assertWarns(
            UserWarning, pc.flow_pipeminor, *(1 * u.m, 0.125 * u.m, 3)
        )

    def test_flow_minor_pipe(self):
        """flow_minor_pipe should return known results for known input."""
        self.assertAlmostEqualQuantity(
            pc.flow_minor_pipe(1 * u.m, 0.125 * u.m, 3),
            0.71000203931611083 * u.m ** 3 / u.s,
        )

    def test_flow_minor_pipe_range(self):
        """flow_minor_pipe should raise errors when inputs are out of bounds."""
        failChecks = (
            (1 * u.m, -1 * u.m, 1),
            (1 * u.m, 1 * u.m, 0 * u.dimensionless),
        )
        for i in failChecks:
            with self.subTest(i=i):
                self.assertRaises(ValueError, pc.flow_minor_pipe, *i)
        passChecks = ((1 * u.m, 1 * u.m, 1), (1 * u.m, 0 * u.m, 1))
        for i in passChecks:
            with self.subTest(i=i):
                pc.flow_minor_pipe(*i)

    def test_flow_pipe(self):
        """flow_pipe should return known value for known inputs."""
        checks = (
            (
                [
                    0.25 * u.m,
                    0.4 * u.m,
                    2 * u.m,
                    0.58 * u.m ** 2 / u.s,
                    0.029 * u.m,
                    0,
                ],
                0.000324207170118938 * u.m ** 3 / u.s,
            ),
            (
                [
                    0.25 * u.m,
                    0.4 * u.m,
                    2 * u.m,
                    0.58 * u.m ** 2 / u.s,
                    0.029 * u.m,
                    0.35 * u.dimensionless,
                ],
                0.000324206539183988 * u.m ** 3 / u.s,
            ),
        )
        for i in checks:
            with self.subTest(i=i):
                self.assertAlmostEqualQuantity(pc.flow_pipe(*i[0]), i[1])

    def test_flow_pipe_warning(self):
        """flow_pipe should raise warnings when passed deprecated parameters"""
        error_checks = (
            lambda: pc.flow_pipe(
                1 * u.m,
                1 * u.m,
                1 * u.m,
                1 * u.m ** 2 / u.s,
                Roughness=1 * u.m,
                KMinor=1,
                PipeRough=1 * u.m,
            ),
            lambda: pc.flow_pipe(
                1 * u.m, 1 * u.m, 1 * u.m, 1 * u.m ** 2 / u.s, KMinor=1
            ),
            lambda: pc.flow_pipe(
                1 * u.m, 1 * u.m, 1 * u.m, 1 * u.m ** 2 / u.s, Roughness=1 * u.m
            ),
        )
        for i in error_checks:
            with self.subTest(i=i):
                self.assertRaises(TypeError, i)

        warning_checks = (
            lambda: pc.flow_pipe(
                1 * u.m,
                1 * u.m,
                1 * u.m,
                1 * u.m ** 2 / u.s,
                PipeRough=1 * u.m,
                KMinor=1,
            ),
        )
        for i in warning_checks:
            with self.subTest(i=i):
                self.assertWarns(UserWarning, i)


class DiamFuncsTest(QuantityTest):
    """Test the diameter functions."""

    def test_diam_hagen(self):
        """diam_hagen should return known value for known inputs."""
        self.assertAlmostEqualQuantity(
            pc.diam_hagen(
                0.006 * u.m ** 3 / u.s,
                0.00025 * u.m,
                0.75 * u.m,
                0.0004 * u.m ** 2 / u.s,
            ),
            0.4158799465199102 * u.m,
        )

    def test_diam_hagen_range(self):
        """diam_hagen should raise errors when inputs are out of bounds."""
        failChecks = (
            (0 * u.m ** 3 / u.s, 1 * u.m, 1 * u.m, 1 * u.m ** 2 / u.s),
            (1 * u.m ** 3 / u.s, 0 * u.m, 1 * u.m, 1 * u.m ** 2 / u.s),
            (1 * u.m ** 3 / u.s, 1 * u.m, 0 * u.m, 1 * u.m ** 2 / u.s),
            (1 * u.m ** 3 / u.s, 1 * u.m, 1 * u.m, 0 * u.m ** 2 / u.s),
        )
        for i in failChecks:
            with self.subTest(i=i):
                self.assertRaises(ValueError, pc.diam_hagen, *i)

    def test_diam_hagen_warning(self):
        """flow_hagen should raise warnings when passed deprecated parameters"""
        error_checks = (
            lambda: pc.diam_hagen(
                1 * u.m ** 3 / u.s,
                HeadLossMajor=1 * u.m,
                Length=1 * u.m,
                Nu=1 * u.m ** 2 / u.s,
                HeadLossFric=1 * u.m,
            ),
            lambda: pc.diam_hagen(
                1 * u.m ** 3 / u.s, Length=1 * u.m, Nu=1 * u.m ** 2 / u.s
            ),
            lambda: pc.diam_hagen(
                1 * u.m ** 3 / u.s, HeadLossMajor=1 * u.m, Nu=1 * u.m ** 2 / u.s
            ),
            lambda: pc.diam_hagen(
                1 * u.m ** 3 / u.s, HeadLossMajor=1 * u.m, Length=1 * u.m
            ),
        )
        for i in error_checks:
            with self.subTest(i=i):
                self.assertRaises(TypeError, i)

        warning_checks = (
            lambda: pc.diam_hagen(
                1 * u.m ** 3 / u.s,
                HeadLossFric=1 * u.m,
                Length=1 * u.m,
                Nu=1 * u.m ** 2 / u.s,
            ),
        )
        for i in warning_checks:
            with self.subTest(i=i):
                self.assertWarns(UserWarning, i)

    def test_diam_swamee(self):
        """diam_swamee should return known value for known input."""
        self.assertAlmostEqualQuantity(
            pc.diam_swamee(
                0.06 * u.m ** 3 / u.s,
                1.2 * u.m,
                7 * u.m,
                0.2 * u.m ** 2 / u.s,
                0.0004 * u.m,
            ),
            0.19286307314945772 * u.m,
        )

    def test_diam_swamee_range(self):
        """diam_swamee should raise errors if inputs are out of bounds."""
        failChecks = (
            (0 * u.m ** 3 / u.s, 1 * u.m, 1 * u.m, 1 * u.m ** 2 / u.s, 1 * u.m),
            (1 * u.m ** 3 / u.s, 0 * u.m, 1 * u.m, 1 * u.m ** 2 / u.s, 1 * u.m),
            (1 * u.m ** 3 / u.s, 1 * u.m, 0 * u.m, 1 * u.m ** 2 / u.s, 1 * u.m),
            (1 * u.m ** 3 / u.s, 1 * u.m, 1 * u.m, 0 * u.m ** 2 / u.s, 1 * u.m),
            (1 * u.m ** 3 / u.s, 1 * u.m, 1 * u.m, 1 * u.m ** 2 / u.s, -2 * u.m),
            (1 * u.m ** 3 / u.s, 1 * u.m, 1 * u.m, 1 * u.m ** 2 / u.s, -1 * u.m),
        )
        for i in failChecks:
            with self.subTest(i=i):
                self.assertRaises(ValueError, pc.diam_swamee, *i)
        passChecks = (
            (1 * u.m ** 3 / u.s, 1 * u.m, 1 * u.m, 1 * u.m ** 2 / u.s, 1 * u.m),
            (1 * u.m ** 3 / u.s, 1 * u.m, 1 * u.m, 1 * u.m ** 2 / u.s, 0 * u.m),
        )
        for i in passChecks:
            with self.subTest(i=i):
                pc.diam_swamee(*i)

    def test_diam_swamee_warning(self):
        """diam_swamee should raise warnings when passed deprecated parameters"""
        error_checks = (
            lambda: pc.diam_swamee(
                1 * u.m ** 3 / u.s,
                HeadLossMajor=1 * u.m,
                Length=1 * u.m,
                Nu=1 * u.m ** 2 / u.s,
                Roughness=1 * u.m,
                HeadLossFric=1 * u.m,
            ),
            lambda: pc.diam_swamee(
                1 * u.m ** 3 / u.s,
                Length=1 * u.m,
                Nu=1 * u.m ** 2 / u.s,
                Roughness=1 * u.m,
            ),
            lambda: pc.diam_swamee(
                1 * u.m ** 3 / u.s,
                HeadLossMajor=1 * u.m,
                Nu=1 * u.m ** 2 / u.s,
                Roughness=1 * u.m,
            ),
            lambda: pc.diam_swamee(
                1 * u.m ** 3 / u.s,
                HeadLossMajor=1 * u.m,
                Length=1 * u.m,
                Roughness=1 * u.m,
            ),
            lambda: pc.diam_swamee(
                1 * u.m ** 3 / u.s,
                HeadLossMajor=1 * u.m,
                Length=1 * u.m,
                Nu=1 * u.m ** 2 / u.s,
                Roughness=1 * u.m,
                PipeRough=1 * u.m,
            ),
            lambda: pc.diam_swamee(
                1 * u.m ** 3 / u.s,
                HeadLossMajor=1 * u.m,
                Length=1 * u.m,
                Nu=1 * u.m ** 2 / u.s,
            ),
        )
        for i in error_checks:
            with self.subTest(i=i):
                self.assertRaises(TypeError, i)

        warning_checks = (
            lambda: pc.diam_swamee(
                1 * u.m ** 3 / u.s,
                HeadLossFric=1 * u.m,
                Length=1 * u.m,
                Nu=1 * u.m ** 2 / u.s,
                Roughness=1 * u.m,
            ),
            lambda: pc.diam_swamee(
                1 * u.m ** 3 / u.s,
                HeadLossMajor=1 * u.m,
                Length=1 * u.m,
                Nu=1 * u.m ** 2 / u.s,
                PipeRough=1 * u.m,
            ),
        )
        for i in warning_checks:
            with self.subTest(i=i):
                self.assertWarns(UserWarning, i)

    def test_diam_pipemajor(self):
        self.assertWarns(
            UserWarning,
            pc.diam_pipemajor,
            *(
                0.005 * u.m ** 3 / u.s,
                0.03 * u.m,
                1.6 * u.m,
                0.53 * u.m ** 2 / u.s,
                0.002 * u.m,
            )
        )

    def test_diam_major_pipe(self):
        """diam_major_pipe should return known value for known inputs."""
        checks = (
            (
                [
                    0.005 * u.m ** 3 / u.s,
                    0.03 * u.m,
                    1.6 * u.m,
                    0.53 * u.m ** 2 / u.s,
                    0.002 * u.m,
                ],
                0.8753787620849313 * u.m,
            ),
            (
                [
                    1 * u.m ** 3 / u.s,
                    2 * u.m,
                    0.03 * u.m,
                    0.004 * u.m ** 2 / u.s,
                    0.005 * u.m,
                ],
                0.14865504303291951 * u.m,
            ),
        )
        for i in checks:
            with self.subTest(i=i):
                self.assertAlmostEqualQuantity(pc.diam_major_pipe(*i[0]), i[1])

    def test_diam_pipeminor(self):
        self.assertWarns(
            UserWarning,
            pc.diam_pipeminor,
            *(0.008 * u.m ** 3 / u.s, 0.012 * u.m, 0.93)
        )

    def test_diam_minor_pipe(self):
        """diam_minor_pipe should return known value for known inputs."""
        checks = (
            (
                [0.008 * u.m ** 3 / u.s, 0.012 * u.m, 0.93],
                0.14229440061589257 * u.m,
            ),
            (
                [0.015 * u.m ** 3 / u.s, 0.3 * u.m, 0.472 * u.dimensionless],
                0.073547549463488848 * u.m,
            ),
        )
        for i in checks:
            with self.subTest(i=i):
                self.assertAlmostEqualQuantity(pc.diam_minor_pipe(*i[0]), i[1])

    def test_diam_minor_pipe_range(self):
        """diam_minor_pipe should raise errors when inputs are out of bounds."""
        failChecks = (
            (0 * u.m ** 3 / u.s, 1 * u.m, 1),
            (1 * u.m ** 3 / u.s, 0 * u.m, 1),
            (1 * u.m ** 3 / u.s, 1 * u.m, -1 * u.dimensionless),
        )
        for i in failChecks:
            with self.subTest(i=i):
                self.assertRaises(ValueError, pc.diam_minor_pipe, *i)
        passChecks = (
            (1 * u.m ** 3 / u.s, 1 * u.m, 1),
            (1 * u.m ** 3 / u.s, 1 * u.m, 0),
        )
        for i in passChecks:
            with self.subTest(i=i):
                pc.diam_minor_pipe(*i)

    def test_diam_pipe(self):
        """diam_pipe should return known value for known inputs."""
        checks = (
            (
                [
                    0.007 * u.m ** 3 / u.s,
                    0.04 * u.m,
                    0.75 * u.m,
                    0.16 * u.m ** 2 / u.s,
                    0.0079 * u.m,
                    0,
                ],
                0.5434876490369928 * u.m,
            ),
            (
                [
                    0.007 * u.m ** 3 / u.s,
                    0.04 * u.m,
                    0.75 * u.m,
                    0.16 * u.m ** 2 / u.s,
                    0.0079 * u.m,
                    0.8 * u.dimensionless,
                ],
                0.5436137491479152 * u.m,
            ),
        )
        for i in checks:
            with self.subTest(i=i):
                self.assertAlmostEqualQuantity(pc.diam_pipe(*i[0]), i[1])


class WeirFuncsTest(QuantityTest):
    """Test the weir functions."""

    def test_width_rect_weir(self):
        self.assertWarns(
            UserWarning, pc.width_rect_weir, *(0.005 * u.m ** 3 / u.s, 0.2 * u.m)
        )

    def test_width_weir_rect(self):
        """width_weir_rect should return known value for known inputs."""
        self.assertAlmostEqualQuantity(
            pc.width_weir_rect(0.005 * u.m ** 3 / u.s, 0.2 * u.m),
            0.03005386871 * u.m,
        )

    def test_width_weir_rect_range(self):
        """width_weir_rect should raise errors when inputs are out of bounds."""
        checks = ((0 * u.m ** 3 / u.s, 1 * u.m), (1 * u.m ** 3 / u.s, 0 * u.m))
        for i in checks:
            with self.subTest(i=i):
                self.assertRaises(ValueError, pc.width_weir_rect, *i)

    def test_headloss_weir(self):
        self.assertWarns(
            UserWarning, pc.headloss_weir, *(0.005 * u.m ** 3 / u.s, 1 * u.m)
        )

    def test_headloss_weir_rect(self):
        """headloss_rect_weir should return known value for known inputs."""
        self.assertAlmostEqualQuantity(
            pc.headloss_weir_rect(0.005 * u.m ** 3 / u.s, 1 * u.m),
            0.01933289619 * u.m,
        )

    def test_headloss_weir_rect_range(self):
        """headloss_weir_rect should raise errors when inputs are out of bounds."""
        checks = ((0 * u.m ** 3 / u.s, 1 * u.m), (1 * u.m ** 3 / u.s, 0 * u.m))
        for i in checks:
            with self.subTest(i=i):
                self.assertRaises(ValueError, pc.headloss_weir_rect, *i)

    def test_flow_rect_weir(self):
        self.assertWarns(UserWarning, pc.flow_rect_weir, *(2 * u.m, 1 * u.m))

    def test_flow_weir_rect(self):
        """flow_weir_rect should return known value for known inputs."""
        self.assertAlmostEqualQuantity(
            pc.flow_weir_rect(2 * u.m, 1 * u.m), 5.2610159627 * u.m ** 3 / u.s
        )

    def test_flow_weir_rect_range(self):
        """flow_weir_rect should raise errors when inputs are out of bounds."""
        checks = ((0 * u.m, 1 * u.m), (1 * u.m, 0 * u.m))
        for i in checks:
            with self.subTest(i=i):
                self.assertRaises(ValueError, pc.flow_weir_rect, *i)


class PorousMediaFuncsTest(QuantityTest):
    def test_headloss_kozeny(self):
        """headloss_kozeny should raise an error when the user tries to use the function."""
        with self.assertRaises(DeprecatedFunctionError):
            pc.headloss_kozeny(
                1 * u.m, 1.4 * u.m, 0.5 * u.m / u.s, 0.625, 0.8 * u.m ** 2 / u.s
            )
        # self.assertRaises(DeprecatedFunctionError, pc.headloss_kozeny(1 * u.m, 1.4 * u.m, 0.5 * u.m/u.s, 0.625, 0.8 * u.m**2/u.s))

    # def test_headloss_kozeny(self):
    #     """headloss_kozeny should return known value for known input."""
    #     self.assertAlmostEqualQuantity(pc.headloss_kozeny(1 * u.m, 1.4 * u.m, 0.5 * u.m/u.s, 0.625, 0.8 * u.m**2/u.s),
    #                                    2.1576362645214617 * u.m)

    # def test_headloss_kozeny_range(self):
    #     """headloss_kozeny should raise errors when inputs are out of bounds."""
    #     checks = ((0 * u.m, 1 * u.m, 1 * u.m/u.s, 1, 1 * u.m**2/u.s),
    #               (1 * u.m, 0 * u.m, 1 * u.m/u.s, 1, 1 * u.m**2/u.s),
    #               (1 * u.m, 1 * u.m, 0 * u.m/u.s, 1, 1 * u.m**2/u.s),
    #               (1 * u.m, 1 * u.m, 1 * u.m/u.s, 1, 0 * u.m**2/u.s),
    #               (1 * u.m, 1 * u.m, 1 * u.m/u.s, -1, 1 * u.m**2/u.s),
    #               (1 * u.m, 1 * u.m, 1 * u.m/u.s, 2, 1 * u.m**2/u.s))
    #     for i in checks:
    #         with self.subTest(i=i):
    #             self.assertRaises(ValueError, pc.headloss_kozeny, *i)
    def test_re_ergun(self):
        self.assertAlmostEqualQuantity(
            pc.re_ergun(0.1 * u.m / u.s, 10 ** -3 * u.m, 298 * u.degK, 0.2),
            139.49692604 * u.dimensionless,
        )

    def test_re_ergun_range(self):
        checks = (
            (0 * u.m / u.s, 1 * u.m, 1 * u.degK, 0.5),
            (1 * u.m / u.s, 0 * u.m, 1 * u.degK, 0.5),
            (1 * u.m / u.s, 1 * u.m, -1 * u.degK, 0.5 * u.dimensionless),
            (1 * u.m / u.s, 1 * u.m, 1 * u.degK, 1 * u.dimensionless),
        )
        for i in checks:
            with self.subTest(i=i):
                self.assertRaises(ValueError, pc.re_ergun, *i)

    def test_fric_ergun(self):
        self.assertAlmostEqualQuantity(
            pc.fric_ergun(0.1 * u.m / u.s, 10 ** -3 * u.m, 298 * u.degK, 0.2),
            5.6505850237 * u.dimensionless,
        )

    def test_headloss_ergun(self):
        self.assertAlmostEqualQuantity(
            pc.headloss_ergun(
                0.1 * u.m / u.s, 10 ** -3 * u.m, 298 * u.degK, 0.2, 4 * u.m
            ),
            1152.39863230 * u.m,
        )

    def test_g_cs_ergun(self):
        self.assertAlmostEqualQuantity(
            pc.g_cs_ergun(0.1 * u.m / u.s, 10 ** -3 * u.m, 298 * u.degK, 0.2),
            39704.892422 * u.Hz,
            5,
        )


class MiscPhysFuncsTest(QuantityTest):
    """Test the miscellaneous physchem functions."""

    def test_height_water_critical(self):
        """height_water_critical should return known value for known inputs."""
        self.assertAlmostEqualQuantity(
            pc.height_water_critical(0.006 * u.m ** 3 / u.s, 1.2 * u.m),
            0.013660704939951886 * u.m,
        )

    def test_height_water_critical_range(self):
        """height_water_critical should raise errors when inputs are out of bounds."""
        checks = ((0 * u.m ** 3 / u.s, 1 * u.m), (1 * u.m ** 3 / u.s, 0 * u.m))
        for i in checks:
            with self.subTest(i=i):
                self.assertRaises(ValueError, pc.height_water_critical, *i)

    def test_vel_horizontal(self):
        """vel_horizontal should return known value for known inputs."""
        self.assertAlmostEqualQuantity(
            pc.vel_horizontal(0.03 * u.m), 0.5424016039799292 * u.m / u.s
        )

    def test_vel_horizontal_range(self):
        """vel_horizontzal should raise an errors when input is <= 0."""
        self.assertRaises(ValueError, pc.vel_horizontal, 0 * u.m)

    def test_pipe_ID(self):
        """pipe_ID should return known value for known input"""
        self.assertAlmostEqualQuantity(
            pc.pipe_ID(0.006 * u.m ** 3 / u.s, 1.2 * u.m),
            0.039682379412712764 * u.m,
        )


if __name__ == "__main__":
    unittest.main()
