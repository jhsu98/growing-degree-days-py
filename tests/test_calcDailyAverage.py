import pytest
from gddPy.gdd import GDD

def test_calcDailyAverage():
    gdd = GDD()

    gdd.min_temp = 34
    gdd.max_temp = 60
    gdd.min_temp_cutoff = 35
    gdd.max_temp_cutoff = 59
    gdd.threshold_low = 40

    assert gdd.calcDailyAverage() == 7
    assert gdd.calcDailyAverage(cutoff_min_temp=True) == 7.5
    assert gdd.calcDailyAverage(cutoff_max_temp=True) == 6.5
    assert gdd.calcDailyAverage(cutoff_min_temp=True, cutoff_max_temp=True) == 7