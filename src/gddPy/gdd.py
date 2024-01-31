import numbers
import numpy as np


class GDD:
    """GDD class"""

    __min_temp = None
    __max_temp = None
    __min_temp_cutoff = None
    __max_temp_cutoff = None
    __threshold_low = None
    __hourly_temps = None

    def __init__(self, params: dict = None):
        if params:
            if not isinstance(params, dict):
                raise TypeError("params must be a dictionary")
            if "min_temp" in params:
                self.min_temp = params.get("min_temp")
            if "max_temp" in params:
                self.max_temp = params.get("max_temp")
            if "min_temp_cutoff" in params:
                self.min_temp_cutoff = params.get("min_temp_cutoff")
            if "max_temp_cutoff" in params:
                self.max_temp_cutoff = params.get("max_temp_cutoff")
            if "threshold_low" in params:
                self.threshold_low = params.get("threshold_low")
            if "hourly_temps" in params:
                self.hourly_temps = params.get("hourly_temps")

    def set_min_temp(self, min_temp: float) -> None:
        if not isinstance(min_temp, numbers.Number):
            raise TypeError("min_temp must be a number")
        if (
            self.__max_temp is not None
            and min_temp > self.__max_temp
        ):
            raise ValueError("min_temp must be less than max_temp")
        self.__min_temp = min_temp

    def set_max_temp(self, max_temp: float) -> None:
        if not isinstance(max_temp, numbers.Number):
            raise TypeError("max_temp must be a number")
        if (
            self.__min_temp is not None
            and max_temp < self.__min_temp
        ):
            raise ValueError("max_temp must be greater than min_temp")
        self.__max_temp = max_temp

    def set_min_temp_cutoff(self, min_temp_cutoff: float) -> None:
        if not isinstance(min_temp_cutoff, numbers.Number):
            raise TypeError("min_temp_cutoff must be a number")
        self.__min_temp_cutoff = min_temp_cutoff

    def set_max_temp_cutoff(self, max_temp_cutoff: float) -> None:
        if not isinstance(max_temp_cutoff, numbers.Number):
            raise TypeError("max_temp_cutoff must be a number")
        self.__max_temp_cutoff = max_temp_cutoff

    def set_threshold_low(self, threshold_low: float) -> None:
        if not isinstance(threshold_low, numbers.Number):
            raise TypeError("threshold_low must be a number")
        self.__threshold_low = threshold_low

    def set_hourly_temps(self, hourly_temps: list) -> None:
        if not isinstance(hourly_temps, list):
            raise TypeError("hourly_temps must be a list")
        if not hourly_temps:
            raise ValueError("hourly_temps must not be empty")
        if not all(isinstance(x, numbers.Number) for x in hourly_temps):
            raise TypeError("hourly_temps must be a list of numbers")
        if len(hourly_temps) > 24:
            raise ValueError("hourly_temps cannot contain 24 more than values")

        self.__hourly_temps = hourly_temps

    def get_min_temp(self) -> numbers.Number:
        return self.__min_temp

    def get_max_temp(self) -> numbers.Number:
        return self.__max_temp

    def get_min_temp_cutoff(self) -> numbers.Number:
        return self.__min_temp_cutoff

    def get_max_temp_cutoff(self) -> numbers.Number:
        return self.__max_temp_cutoff

    def get_threshold_low(self) -> numbers.Number:
        return self.__threshold_low

    def get_hourly_temps(self) -> list:
        return self.__hourly_temps

    min_temp = property(get_min_temp, set_min_temp)
    max_temp = property(get_max_temp, set_max_temp)
    min_temp_cutoff = property(
        get_min_temp_cutoff, set_min_temp_cutoff
    )
    max_temp_cutoff = property(
        get_max_temp_cutoff, set_max_temp_cutoff
    )
    threshold_low = property(get_threshold_low, set_threshold_low)
    hourly_temps = property(get_hourly_temps, set_hourly_temps)

    def __dailyAverage(low: float, high: float, base: float) -> numbers.Number:
        return max(0, ((high + low) / 2) - base)

    def calcDailyAverage(
        self, cutoff_min_temp=False, cutoff_max_temp=False
    ):
        if self.min_temp is None or self.max_temp is None:
            raise ValueError("min_temp and max_temp must be set")

        if self.__threshold_low is None:
            raise ValueError("threshold_low must be set")

        if cutoff_min_temp and self.min_temp_cutoff is None:
            raise ValueError("min_temp_cutoff must be set")

        if cutoff_max_temp and self.max_temp_cutoff is None:
            raise ValueError("max_temp_cutoff must be set")

        min_temp = (
            max(self.min_temp, self.min_temp_cutoff)
            if cutoff_min_temp
            else self.min_temp
        )
        max_temp = (
            min(self.max_temp, self.max_temp_cutoff)
            if cutoff_max_temp
            else self.max_temp
        )
        base = self.threshold_low

        gdd = GDD.__dailyAverage(min_temp, max_temp, base)
        return gdd

    def calcBaskervilleEmin(
        self, cutoff_min_temp=False, cutoff_max_temp=False
    ) -> numbers.Number:
        if self.min_temp is None or self.max_temp is None:
            raise ValueError("min_temp and max_temp must be set")

        if self.threshold_low is None:
            raise ValueError("threshold_low must be set")

        if cutoff_min_temp and self.min_temp_cutoff is None:
            raise ValueError("min_temp_cutoff must be set")

        if cutoff_max_temp and self.max_temp_cutoff is None:
            raise ValueError("max_temp_cutoff must be set")

        min_temp = (
            max(self.min_temp, self.min_temp_cutoff)
            if cutoff_min_temp
            else self.min_temp
        )

        max_temp = (
            min(self.max_temp, self.max_temp_cutoff)
            if cutoff_max_temp
            else self.max_temp
        )

        base = self.threshold_low

        if max_temp < base:
            return 0
        elif min_temp >= base:
            return GDD.__dailyAverage(min, max, base)
        else:
            avg = (min_temp + max_temp) / 2
            w = (max_temp - min_temp) / 2
            theta = np.arcsin((base - avg) / w)

            gdd = (w * np.cos(theta) - (base - avg) * (np.pi / 2 - theta)) / np.pi
            return gdd

    def calcHourlyUtilization(
        self, cutoff_min_temp=False, cutoff_max_temp=False
    ) -> numbers.Number:
        print(f"cutoff_min_temp: {cutoff_min_temp}")
        print(f"cutoff_max_temp: {cutoff_max_temp}")
        if self.threshold_low is None:
            raise ValueError("threshold_low must be set")

        if self.hourly_temps is None:
            raise ValueError("hourly_temps must be set")

        if cutoff_min_temp and self.min_temp_cutoff is None:
            raise ValueError("min_temp_cutoff must be set")

        if cutoff_max_temp and self.max_temp_cutoff is None:
            raise ValueError("max_temp_cutoff must be set")

        ht = self.hourly_temps
        base = self.threshold_low

        if cutoff_min_temp or cutoff_max_temp:
            for i in range(len(ht)):
                if cutoff_min_temp and self.min_temp_cutoff and ht[i] < self.min_temp_cutoff:
                    ht[i] = self.min_temp_cutoff
                    
                if cutoff_max_temp and self.max_temp_cutoff and ht[i] > self.max_temp_cutoff:
                    ht[i] = self.max_temp_cutoff

        gdd = 0

        for h in ht:
            gdd += max(0, h - base)

        return gdd / len(ht)
