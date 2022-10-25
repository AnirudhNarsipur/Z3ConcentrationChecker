from __future__ import annotations
from dataclasses import dataclass
from importlib.resources import path
from z3 import *
import re
from concentration_plans import Plan,ABPlan,ScBPlan
from dfparser import  DFParser
import random
from model_result import FAILED, PASSED, Result 
from plan_vars import ABPlanVars, PathwayVars,PlanVars
from abc import ABC, abstractmethod
from concentration_constants import ConcentrationConstants


#TODO : some constraints are actually just boolean vals being added to the model
#this will probably cause a problem for synthesis
class AbstractModel(ABC):

    def __init__(self,plan : Plan,parser : DFParser,concentration_constants : ConcentrationConstants) -> None:
        self.parser = parser
        self.s = Solver()
        self.plan  = plan
        self.concentration_constants = concentration_constants
        return None

    def set_equal(self,ls : set[ArithRef],cs : list[int],txt : str):
            ls = list(ls)
            for i in range(len(ls)):
                self.add(ls[i] == cs[i],f"{i+1} {txt}")

    def var_inset(self,v : ArithRef,ls : set[int]):
        """
        Check if variable  is in set of course ints

        Args:
            v (ArithRef): _description_
            ls (list[int]): _description_

        Returns:
            _type_: _description_
        """
        return Or([v == elem for elem in ls])
   
    def vars_inset(self,vars : set[ArithRef],courses : set[int]):
        return And([self.var_inset(v,courses) for v in vars])

    def course_inset(self,course:int,vars :set[ArithRef]):
        return Or([course == var for var in vars])

    def var_in_varset(self,var : ArithRef,vars : set[ArithRef]):
        return Or([var == var for var in vars])


    def lscourse_inset(self,courses : set[int],vars:set[ArithRef]):
        return And([self.course_inset(c,vars) for c in courses])

    def intersection(self,vars : set[ArithRef],courses : Iterable[int]):
        intersect_vars = []
        for var in vars:
            intersect = Bool(f"intersection_{var}_{str(courses)})_{random.randint(1,1000)}")
            var_match = self.var_inset(var,courses)
            self.s.add(If(
              var_match == True,
               intersect == True,
                intersect == False
                ))
            intersect_vars.append(intersect)
        
        return Sum(intersect_vars)

    
    def add(self,constraint,txt : str):
        if isinstance(constraint,bool):
            var = Bool(f"assertconstant_{random.randint(1,10000)}")
            self.s.add(var == True)
            self.s.assert_and_track(var == constraint,txt)
        else:
            self.s.assert_and_track(constraint == True,txt)

    def unsat_core(self):
        return [" ".join(str(s).split()[1:]) for s in self.s.unsat_core()]

    def satisfies_pathway(self,vars : PlanVars,pathwayvars : PathwayVars):
        pathreqs = self.parser.get_pathway(pathwayvars.pathwayname)
        #Intermediate Reqs
        for catg in pathreqs.intermediate:
            self.add(
                self.intersection(vars.courses,catg) >= 1,
                f"Pathway intermediate course Requirement {catg} ")
        #Core Reqs
        self.add(len(pathwayvars) >= 2,f"At least 2 courses in pathway {pathwayvars.pathwayname}")
        self.add(self.intersection(pathwayvars.courses,pathreqs.core) >= 1,"At least 1 pathway course is a core course")
        self.add(self.intersection(pathwayvars.courses,pathreqs.core+pathreqs.grad+pathreqs.related) == len(pathwayvars),"All pathway courses are core/grad/related")

   
    def add_common_requirements(self):
        self.add_calculus_prereq_requirements()
        self.add_intro_course_requirements()
        self.add_elective_requirements()

    def get_result(self) -> Result:
        if self.s.check() == unsat:
            return FAILED(list(self.unsat_core()))
        else:
            return PASSED()


        
       
    def add_intro_course_requirements(self):
        mp = self.parser.map
        #intro req 
        self.add(len(vars.intro) >= 2,"at least 2 intro courses")
        self.add(
            Or(
                self.course_inset(mp["CSCI0190"],vars.intro),
                self.course_inset(mp["CSCI0160"],vars.intro),
                self.course_inset(mp["CSCI0180"],vars.intro),
                self.course_inset(mp["CSCI0200"],vars.intro),
                # CSCI 113?

            )
        ,"intro reqs")
        
    def add_calculus_prereq_requirements(self):
        # Calc prereq
        self.add(
            Or(
                self.intersection(vars.courses,self.parser.map.course_ints(["MATH0100","MATH0170","MATH0190"])) > 0,
                self.lscourse_inset(self.parser.calc_courses,vars.courses)
            )
       ,"calc requisite" )

    def add_elective_requirements(self):
        #Elective Requirements
        self.add(self.vars_inset(vars.electives,self.parser.electives),"Electives are approved")

        self.add(self.intersection(vars.electives,self.parser.intermediate_courses) <= 1,"No more than 1 intermediate course is a elective")

        pathreq  = self.parser.get_pathway(vars.pathway1.pathwayname)
        pathwaycourses = pathreq.core + pathreq.related + pathreq.grad
        self.add(self.intersection(vars.electives,pathwaycourses) != len(vars.electives),"At least 1 elective course is not in the pathways")
