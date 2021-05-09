from aguaclara.design.ent_floc import EntTankFloc
from aguaclara.core.units import u
import aguaclara.core.utility as ut

import pytest

etf_20 = EntTankFloc(q=20.0 * u.L / u.s)
etf_60 = EntTankFloc(q=60.0 * u.L / u.s)


@pytest.mark.parametrize(
    "actual, expected",
    [
        (etf_20.ent.l, 42.14070667837542 * u.inch),
        (etf_60.ent.l, 42.64683865450655 * u.inch),
        (etf_20.ent.drain_pipe.id, 3.8048780487804876 * u.inch),
        (etf_60.ent.drain_pipe.id, 3.8048780487804876 * u.inch),
        (etf_20.floc.chan_w, 33.0 * u.cm),
        (etf_60.floc.chan_w, 97.0 * u.cm),
        (etf_20.floc.chan_n, 2),
        (etf_60.floc.chan_n, 2),
        (etf_20.floc.chan_w_min_gt, 32.02195253008654 * u.cm),
        (etf_60.floc.chan_w_min_gt, 96.24786648922903 * u.cm),
        (etf_20.ent.plate_l, 56 * u.cm),
        (etf_60.ent.plate_l, 58 * u.cm),
        (etf_20.ent.plate_n, 20),
        (etf_20.ent.plate_n, 20),
    ],
)
def test_etf(actual, expected):
    if type(actual) == u.Quantity and type(expected) == u.Quantity:
        assert actual.units == expected.units
        assert actual.magnitude == pytest.approx(expected.magnitude)
    else:
        assert actual == pytest.approx(expected)
