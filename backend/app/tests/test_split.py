import pytest
from app.engines.curtain_math import fabric_meters, split_panels


def test_ratio_floor_split():
    # 5 幅、左侧占比 0.4 -> floor(2.0)=2，右侧余 3
    assert split_panels(5, 0.4) == (2, 3)


def test_ratio_default_half():
    r = fabric_meters(3.0, 2.6, 2.0, 0.10, 0.15, 1.4)
    assert r["panels"] == 5
    assert (r["left_panels"], r["right_panels"]) == (2, 3)
    # 总 meters 仍按总 panels × cut_height，不随分幅改变
    assert r["meters"] == 14.25


def test_ratio_independent_of_split():
    base = fabric_meters(3.0, 2.6, 2.0, 0.10, 0.15, 1.4, 0.5)
    skew = fabric_meters(3.0, 2.6, 2.0, 0.10, 0.15, 1.4, 0.3)
    assert base["meters"] == skew["meters"]
    assert skew["left_panels"] == 1
    assert skew["right_panels"] == 4


def test_ratio_boundaries():
    assert split_panels(4, 0.0) == (0, 4)
    assert split_panels(4, 1.0) == (4, 0)


@pytest.mark.parametrize("bad", [-0.01, 1.01, float("nan"), float("inf")])
def test_ratio_out_of_range(bad):
    with pytest.raises(ValueError):
        split_panels(4, bad)
    with pytest.raises(ValueError):
        fabric_meters(1.0, 2.0, 1.0, 0.0, 0.0, 1.4, bad)


def test_zero_total_panels_fails():
    with pytest.raises(ValueError):
        split_panels(0, 0.5)
