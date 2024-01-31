import pytest
from gddPy.gdd import GDD

def test_baskervilleEmin():
    gdd = GDD()

    gdd.min_temp = 34
    gdd.max_temp = 60
    gdd.threshold_low = 50

    assert round(gdd.calcBaskervilleEmin(), 3) == 2.749