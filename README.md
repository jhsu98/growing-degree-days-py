# gddPy

## Description

This Python library is intended for agriculture professionals interested in calculating growing degree days (GDD). GDD is also known as heat units or thermal units.

## Installation and Initial Usage

To begin using the library, install it using one of the following commands based on your system and package management strategy:

```bash
pip install gddPy
pip3 install gddPy
poetry add gddPy
```

Next, here's a quick example of using the library:

```python
from gddPy import GDD

gdd = GDD()
gdd.min_temp = 34
gdd.max_temp = 60
gdd.threshold_low = 40

heat_units = gdd.calcDailyAverage() # should calculate to 7
```

## Detailed Description

The library supports the following properties:

| Property        | Description                      |
| :-------------- | :------------------------------- |
| min_temp        | low temperature for the day      |
| max_temp        | high temperature for the day     |
| threshold_low   | base threshold to begin accruing |
| min_temp_cutoff | optional limit for min_temp      |
| max_temp_cutoff | optional limit for max_temp      |

Each property may be set when creating a new GDD() instance as a dictionary property

```python
params = {
    "min_temp": 34,
    "max_temp": 60,
    "threshold_low": 40
}

gdd = GDD(params)
```

The following calculation methods are supported, each with a description of the formula

### DailyAverage

The Daily Average method is the simplest approach to calculate GDD. The formula takes the average temperature for the day and subtracts the lower threshold from it[^1].

$\text{GDD} = \frac{T_{\text{max}} + T_{\text{min}}}{2} - TH_{\text{low}}$

### Baskerville-Emin

The Baskerville-Emin method is a more complex approach to calculate GDD that is preferable in regions with larger temperature fluctuations[^2].

$\text{GDD} = \frac{w \cdot \sqrt{1 - \left(\theta\right)^2} - (TH_{\text{low}} - T_{\text{avg}}) \cdot \arccos\left(\theta\right)}{\pi}$

where...

- $w =$ Half of the Daily Temperature Range
- $T_{\text{avg}} =$ Average Temperature
- $TH_{\text{low}} =$ Lower Threshold
- $\theta = \frac{TH_{\text{low}} - T_{\text{avg}}}{w}$

### Hourly Utilization

The Hourly Utilization method is a more precise approach to calculate GDD that requires hourly temperature readings to determine the thermal accumulation for each hour individually.

$\text{GDD} = \frac{\sum_{h=1}^{24} \max\left( T_{h} - TH_{\text{low}}, 0 \right)}{24}$

Although the formula above assumes a whole day (24 hours) this library is able to calculate partial days by providing less than 24 temperature values to `hourly_temps`

```python
gdd = GDD()
gdd.threshold_low = 34
gdd.hourly_temps = [32,36,51,60,74,75,70,66,63,61]

heat_units = gdd.calcHourlyUtilization()
```

[^1]: https://mrcc.purdue.edu/gismaps/gddinfo
[^2]: https://www.canr.msu.edu/uploads/files/Research_Center/NW_Mich_Hort/General/CalculationBaskervilleEminGDD.pdf

### Using min_temp_cutoff and max_temp_cutoff

To use `min_temp_cutoff` and/or `max_temp_cutoff`, pass a dictionary to any calculation method setting flags to `True`.

```python
temperature_data = {
    "min_temp": 34,
    "max_temp": 60,
    "min_temp_cutoff": 35,
    "max_temp_cutoff": 55,
    "threshold_low": 40
}

gdd = GDD(temp_data)

params = {
    "cutoff_min_temp": True,
    "cutoff_max_temp": True
}

heat_units = gdd.calcDailyAverage(params) # equals 5

```

## Changelog

- v1.0.3 | January 30, 2024: Added `calcHourlyUtilization()` method, which requires `threshold_low` and `hourly_temps` to be set. Added two properties `min_temp_cutoff` and `max_temp_cutoff` that can be used with any of the calculation methods by passing `use_min_cutoff = True` or `use_max_cutoff = True`
