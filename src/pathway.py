from dataclasses import dataclass

@dataclass(frozen=True)
class Pathway:
    courses : set[str]
    name : str

    def __len__(self):
        return len(self.courses)