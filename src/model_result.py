

from dataclasses import dataclass

from abc import ABC

class Result(ABC):
    pass

class PASSED(Result):
    def __str__(self) -> str:
        return "PASSED"
    def __repr__(self) -> str:
        return "PASSED"

@dataclass(frozen=True)
class FAILED(Result):
    unsat_core : list[str]

    def __str__(self) -> str:
        return "FAILED: " + " ".join(self.unsat_core)