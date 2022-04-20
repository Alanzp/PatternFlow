class Parameter:
    def __init__(
        self,
        min: int = 0,
        max: int = 100,
        current: int = 50,
    ) -> None:
        self._min = min
        self._max = max
        self.setCurrent(current)

    def getMin(self) -> int:
        return self._min

    def getMax(self) -> int:
        return self._max

    def getCurrent(self) -> int:
        return self._current

    def setCurrent(self, val: int) -> None:
        if self._min > val or self._max < val:
            raise Exception("Set param {} out of range".format(self._name))
        self._current = val
