from __future__  import annotations
from dataclasses import dataclass
from pathway import Pathway

class Plan:
    pass

@dataclass(frozen=True)
class ScBPlan(Plan):
    calc_prereq : set[str]
    intro : set[str]
    intermediate : set[str]
    pathway1 : Pathway
    electives : set[str]
    pathway2 : Pathway
    capstone :  set[str]

    @classmethod
    def from_dict(cls,plan_dict : dict) -> ScBPlan:
        pathwaysls  =  []
        for key in plan_dict["Pathways"]:
            pathwaysls.append(Pathway(name=key,courses=plan_dict["Pathways"][key]))
        if len(pathwaysls) != 2:
            raise Exception("Given more than 2 pathways")
        if len(plan_dict["Capstone Course"]) < 1:
            raise Exception("No capstone course specified")
        return cls(
            intro = plan_dict["Introductory Courses"],
            calc_prereq=plan_dict["Calculus Prerequisite"],
            intermediate =plan_dict["Intermediate Courses"],
            pathway1 = pathwaysls[0],
            electives = plan_dict["Additional Courses"],
            pathway2 = pathwaysls[1],
            capstone = plan_dict["Capstone Course"])


@dataclass(frozen=True)
class ABPlan(Plan):
    calc_prereq : set[str]
    intro : set[str]
    intermediate : set[str]
    pathway1 : Pathway
    electives : set[str]

    @classmethod
    def from_dict(cls,plan_dict : dict) -> ABPlan:
        pathway = Pathway(name=list(plan_dict["Pathways"].keys())[0],courses=list(plan_dict["Pathways"].values())[0])
        return cls(
            intro = plan_dict["Introductory Courses"],
            calc_prereq=plan_dict["Calculus Prerequisite"],
            intermediate =plan_dict["Intermediate Courses"],
            pathway1 = pathway,
            electives = plan_dict["Additional Courses"]
        )

@dataclass(frozen=True)
class ErrorPlan(Plan):
    error_message : str
       
        


