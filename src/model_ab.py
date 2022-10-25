from __future__ import annotations
from dataclasses import dataclass
from importlib.resources import path
from z3 import *
import re
from model_abstract import AbstractModel
from concentration_plans import Plan,ABPlan,ScBPlan
from dfparser import  DFParser
import random 
from plan_vars import ABPlanVars, PathwayVars,PlanVars
from concentration_constants import ConcentrationConstants

class ABModel(AbstractModel):
    def __init__(self,plan : ABPlan,parser : DFParser,concentration_constants : ConcentrationConstants) -> None:
        super().__init__(plan,parser,concentration_constants)
       
      
        self.vars = ABPlanVars.get_ab_plan_vars(plan,parser.map.num_courses)
        mapping = parser.map
        #Variable Bounds
        for var in self.vars.courses:
            self.s.add(0 <= var,var <= parser.map.num_courses)
        #Variables Equal to Plan Change approved
        self.set_equal(self.vars.calc_prereq,mapping.course_ints(plan.calc_prereq),"Calc courses are approved")
        self.set_equal(self.vars.intro,mapping.course_ints(plan.intro),"Intro courses are approved")
        self.set_equal(self.vars.intermediate,mapping.course_ints(plan.intermediate),"intermediate courses are approved")
        self.set_equal(self.vars.pathway1.courses ,mapping.course_ints(plan.pathway1.courses),"pathway courses are approved")
        self.set_equal(self.vars.electives,mapping.course_ints(plan.electives),"Elective courses are approved")

    def create_model(self,vars: PlanVars):
      
        parser = self.parser
        mp = self.parser.map
        self.add_common_requirements()
        self.add(Distinct(vars.courses),"Courses are distinct")

    
        #Pathway Reqs 
        self.satisfies_pathway(vars,vars.pathway1)

        #AB Reqs
        self.add(len(vars.courses) >= self.concentration_constants.NumberOfCoursesAB , f"At least {self.concentration_constants.NumberOfCoursesAB} courses in AB Plan")

        self.add(len(vars.pathway1) != 0,"At least 1 pathway in AB Plan")

        self.add(self.intersection(vars.courses,parser.arts_courses) <= self.concentration_constants.NumberOfArtsSocialCoursesAB,f"{self.concentration_constants.NumberOfArtsSocialCoursesAB} or fewer Arts/Social Science courses in AB Plan")

        self.add(len(vars.intermediate) >= self.concentration_constants.NumberOfArtsSocialCoursesAB,f"At least {self.concentration_constants.NumberOfIntermediateCoursesAB} intermediate courses in AB Plan")

        #At least 1 course from 2 intermediate categories
        systemscourses = self.intersection(vars.intermediate,parser.intermediate_systems_courses)

        mathcourses = self.intersection(vars.intermediate,parser.intermediate_math_courses)

        foundationscourses = self.intersection(vars.intermediate,parser.intermediate_foundations_courses)


        self.add(Or(
            And(systemscourses >= 1,mathcourses >= 1),
            And(systemscourses >= 1,foundationscourses >= 1),
            And(mathcourses >= 1 , foundationscourses >= 1)
        ),"Courses from 2 of 3 intermediate course categories for a AB Plan")