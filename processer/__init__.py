import os
import inspect
import sys

from sqlalchemy import true
from .common.base import Base
from .common.parameter import Parameter

__all__ = []


def isProcessClass(cls: object) -> bool:
    if issubclass(cls, Base) and Base != cls and Parameter != cls:
        return true


sys.path.append(os.path.dirname(__file__))
for module in os.listdir(os.path.dirname(__file__)):
    if module == '__init__.py' or module[-3:] != '.py':
        continue
    myModule = __import__(module[:-3], locals(), globals())
    classes = inspect.getmembers(myModule, inspect.isclass)

    __all__.extend(
        [myClss[1] for myClss in classes if isProcessClass(myClss[1])])
