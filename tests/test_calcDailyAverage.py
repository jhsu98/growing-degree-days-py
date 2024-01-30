import pytest
from gddPy.gdd import GDD

def test_baskervilleEmin():
    gdd = GDD()

    gdd.min_temperature = 34
    gdd.max_temperature = 60
    gdd.threshold_low = 40

    assert gdd.calcDailyAverage() == 7