from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class CourseMap:
    map : dict[str,int]

    def __getitem__(self,indices):
        if isinstance(indices,tuple):
            raise ValueError("oops")
        else:
            if indices in self.map:
                return self.map[indices]
            else:
                return -1
    @property
    def num_courses(self):
        return len(self.map)
   
    def course_ints(self,ls : Iterable[str]):
       return [self[i] for i in ls]