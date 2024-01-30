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
gdd.min_temperature = 34
gdd.max_temperature = 60
gdd.threshold_low = 50

heat_units = gdd.calcDailyAverage() # should calculate to 7
```

## Detailed Description

The library supports the following properties:

| Property        | Description                      |
| :-------------- | :------------------------------- |
| min_temperature | low temperature for the day      |
| max_temperature | high temperature for the day     |
| threshold_low   | base threshold to begin accruing |

Each property may be set when creating a new GDD() instance as a dictionary property

```python
params = {
    "min_temperature": 34,
    "max_temperature": 60,
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

[^1]: https://mrcc.purdue.edu/gismaps/gddinfo
[^2]: https://www.canr.msu.edu/uploads/files/Research_Center/NW_Mich_Hort/General/CalculationBaskervilleEminGDD.pdf
