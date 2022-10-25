from dataclasses import dataclass
from typing import Iterable
from z3 import ArithRef

@dataclass(frozen=True)        
class PathwayReq:
    name : str
    core : list[int]
    intermediate : list[list[int]]
    grad : list[int]
    related : list[int]
