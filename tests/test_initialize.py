import pytest
from gddPy.gdd import GDD

def test_empty_init():
    try:
        gdd = GDD()
    except Exception as e:
        assert False, f"test_empty_init raised an exception {e}"

def test_empty_init_params():
    try:
        gdd = GDD({})
    except Exception as e:
        assert False, f"test_empty_init_params raised an exception {e}"

def test_init_params():
    try:
        gdd = GDD({'min_temperature': 1, 'max_temperature': 2, 'threshold_low': 3})
    except Exception as e:
        assert False, f"test_init_params raised an exception {e}"

def test_init_params_min_temperature():
    try:
        gdd = GDD({'min_temperature': 1})
        assert gdd.min_temperature == 1
    except Exception as e:
        assert False, f"test_init_params_min_temperature raised an exception {e}"

    with pytest.raises(TypeError):
        gdd = GDD({'min_temperature': '1'})
    
    with pytest.raises(TypeError):
        gdd = GDD({'min_temperature': None})

def test_init_params_max_temperature():
    try:
        gdd = GDD({'max_temperature': 2})
        assert gdd.max_temperature == 2
    except Exception as e:
        assert False, f"test_init_params_max_temperature raised an exception {e}"

    with pytest.raises(TypeError):
        gdd = GDD({'max_temperature': '2'})
    
    with pytest.raises(TypeError):
        gdd = GDD({'max_temperature': None})

def test_init_params_threshold_low():
    try:
        gdd = GDD({'threshold_low': 3})
        assert gdd.threshold_low == 3
    except Exception as e:
        assert False, f"test_init_params_threshold_low raised an exception {e}"

    with pytest.raises(TypeError):
        gdd = GDD({'threshold_low': '3'})
    
    with pytest.raises(TypeError):
        gdd = GDD({'threshold_low': None})

