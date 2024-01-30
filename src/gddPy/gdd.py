import numbers
import numpy as np


class GDD:
    """GDD class"""

    __min_temperature = None
    __max_temperature = None
    __threshold_low = None

    def __init__(self, params: dict = None):
        if params:
            if not isinstance(params, dict):
                raise TypeError("params must be a dictionary")
            if "min_temperature" in params:
                self.min_temperature = params.get("min_temperature")
            if "max_temperature" in params:
                self.max_temperature = params.get("max_temperature")
            if "threshold_low" in params:
                self.threshold_low = params.get("threshold_low")

    def set_min_temperature(self, min_temperature: float) -> None:
        if not isinstance(min_temperature, numbers.Number):
            raise TypeError("min_temperature must be a number")
        if (
            self.__max_temperature is not None
            and min_temperature > self.__max_temperature
        ):
            raise ValueError("min_temperature must be less than max_temperature")
        self.__min_temperature = min_temperature

    def set_max_temperature(self, max_temperature: float) -> None:
        if not isinstance(max_temperature, numbers.Number):
            raise TypeError("max_temperature must be a number")
        if (
            self.__min_temperature is not None
            and max_temperature < self.__min_temperature
        ):
            raise ValueError("max_temperature must be greater than min_temperature")
        self.__max_temperature = max_temperature

    def set_threshold_low(self, threshold_low: float) -> None:
        if not isinstance(threshold_low, numbers.Number):
            raise TypeError("threshold_low must be a number")
        self.__threshold_low = threshold_low

    def get_min_temperature(self) -> numbers.Number:
        return self.__min_temperature

    def get_max_temperature(self) -> numbers.Number:
        return self.__max_temperature

    def get_threshold_low(self) -> numbers.Number:
        return self.__threshold_low

    min_temperature = property(get_min_temperature, set_min_temperature)
    max_temperature = property(get_max_temperature, set_max_temperature)
    threshold_low = property(get_threshold_low, set_threshold_low)

    def __dailyAverage(low: float, high: float, base: float) -> numbers.Number:
        return max(0, ((high + low) / 2) - base)

    def calcDailyAverage(self):
        if self.min_temperature is None or self.max_temperature is None:
            raise ValueError("min_temperature and max_temperature must be set")

        if self.__threshold_low is None:
            raise ValueError("threshold_low must be set")

        gdd = GDD.__dailyAverage(
            self.min_temperature, self.max_temperature, self.threshold_low
        )
        return gdd

    def calcBaskervilleEmin(self) -> numbers.Number:
        if self.min_temperature is None or self.max_temperature is None:
            raise ValueError("min_temperature and max_temperature must be set")

        if self.threshold_low is None:
            raise ValueError("threshold_low must be set")

        min = self.min_temperature
        max = self.max_temperature
        base = self.threshold_low

        if max < base:
            return 0
        elif min >= base:
            return GDD.__dailyAverage(min, max, base)
        else:
            avg = (min + max) / 2
            w = (max - min) / 2
            theta = np.arcsin((base - avg) / w)

            gdd = (w * np.cos(theta) - (base - avg) * (np.pi / 2 - theta)) / np.pi
            return gdd
