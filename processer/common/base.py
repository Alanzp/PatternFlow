from abc import ABCMeta, abstractmethod
from .parameter import Parameter
from typing import Dict


class Base(metaclass=ABCMeta):
    def __init__(self) -> None:
        self.params: Dict[str:Parameter] = {}
        pass

    def outputStr(self) -> str:
        string_params = ["{},{}".format(k, v.getCurrent()) for k, v in self.params.items()]
        outputStr = ";".join(string_params)
        return outputStr

    @abstractmethod
    def process(self, inputImage_BGR):
        pass
