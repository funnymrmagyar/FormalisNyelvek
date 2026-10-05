# problems almodul – automatikusan importálja az összes Problems-leszármazottat,
# hogy a __main__.py egységesen tudja kezelni őket.

from .problem import Problems
from .sum import SumProblem
from .dfa import DFAProblem
