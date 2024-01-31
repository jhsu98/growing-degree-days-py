import pytest
from gddPy.gdd import GDD

def test_hourlyUtilization():
    gdd = GDD()

    with pytest.raises(ValueError):
        gdd.calcHourlyUtilization()

def test_hourlyUtilization_threshold_low():
    gdd = GDD({'threshold_low': 15})

    with pytest.raises(ValueError):
        gdd.calcHourlyUtilization()

def test_hourlyUtilization_temperatures():
    gdd = GDD({'hourly_temps': [10,22,44,58,60]})

    with pytest.raises(ValueError):
        gdd.calcHourlyUtilization()

def test_hourlyUtilization_valid():
    gdd = GDD({'threshold_low': 15, 'hourly_temps': [10,22,44,58,60]})
    assert gdd.calcHourlyUtilization() == 24.8

def test_hourlyUtilization_noCutoff():
    gdd = GDD()
    gdd.threshold_low = 34
    gdd.hourly_temps = [32,36,51,60,74,75,70,66,63,61]

    assert gdd.calcHourlyUtilization() == 25

def test_hourlyUtilization_minCutoff():
    gdd = GDD()
    gdd.threshold_low = 34
    gdd.hourly_temps = [32,36,51,60,74,75,70,66,63,61]
    gdd.min_temp_cutoff = 40
    gdd.max_temp_cutoff = 66

    assert gdd.calcHourlyUtilization(cutoff_min_temp=True) == 26

def test_hourlyUtilization_maxCutoff():
    gdd = GDD()
    gdd.threshold_low = 34
    gdd.hourly_temps = [32,36,51,60,74,75,70,66,63,61]
    gdd.min_temp_cutoff = 40
    gdd.max_temp_cutoff = 66

    assert gdd.calcHourlyUtilization(cutoff_max_temp=True) == 22.9

def test_hourlyUtilization_minAndMaxCutoff():
    gdd = GDD()
    gdd.threshold_low = 34
    gdd.hourly_temps = [32,36,51,60,74,75,70,66,63,61]
    gdd.min_temp_cutoff = 40
    gdd.max_temp_cutoff = 66

    assert gdd.calcHourlyUtilization(cutoff_min_temp=True, cutoff_max_temp=True) == 23.9