from __future__ import annotations
from dataclasses import dataclass
from z3 import ArithRef , Int
from concentration_plans import ABPlan, ScBPlan


@dataclass()
class PathwayVars:
    pathwayname : str
    courses : set[ArithRef]

    def __len__(self):
        return len(self.courses)


@dataclass()
class PlanVars:
    calc_prereq : set[ArithRef]
    intro : set[ArithRef]
    intermediate : set[ArithRef]
    pathway1 : PathwayVars
    electives :set[ArithRef]
    @property
    def courses(self) -> set[ArithRef]:
        res = set().union(*[self.calc_prereq , self.intro , self.intermediate , self.pathway1.courses , self.electives])
        return res

@dataclass()
class ABPlanVars(PlanVars):

    @classmethod
    def get_ab_plan_vars(cls,str_plan : ABPlan,num_courses : int) -> ABPlanVars:
        elems = {}
        for key in str_plan.__dict__ :
            if key == "pathway1":
                elems["pathway1"] = PathwayVars(str_plan.pathway1.name,
                   {Int(f"pathway_{elem}") for elem in range(len(str_plan.pathway1.courses))})
            else:
                elems[key] = {Int(f"{key}_{i}") for i in range(len(str_plan.__dict__[key]))}
        return cls(**elems)

@dataclass()
class ScBPlanVars(PlanVars):
    pathway2 : PathwayVars
    capstone : ArithRef
    @property
    def courses(self) -> set[ArithRef]:
        # not including capstone because that should be in the pathways 
        # Is this a problem ? no because the constraints are not affected
        res = set().union(*[self.calc_prereq , self.intro , self.intermediate , self.pathway1.courses , self.electives,self.pathway2.courses])
        return res
    @classmethod
    def get_scb_plan_vars(cls,str_plan : ScBPlan,num_courses : int) -> ScBPlanVars:
        elems = {}
        for key in str_plan.__dict__ :
            if key == "pathway1" :
                elems[key] = PathwayVars( str_plan.pathway1.name,{Int(f"{key}_{elem}") for elem in range(len(str_plan.pathway1.courses))})
            elif key == "pathway2":
                elems[key] = PathwayVars( str_plan.pathway2.name,{Int(f"{key}_{elem}") for elem in range(len(str_plan.pathway2.courses))})
            elif key == "capstone":
                elems[key] = Int("capstone_course")
            else:
                elems[key] = {Int(f"{key}_{i}") for i in range(len(str_plan.__dict__[key]))}
        return cls(**elems)
