from __future__ import annotations
from z3 import *
import re
from model_abstract import AbstractModel
from concentration_plans import ScBPlan
from dfparser import  DFParser
from plan_vars import  ScBPlanVars
from concentration_constants import ConcentrationConstants

class ScBModel(AbstractModel):
    def __init__(self,plan : ScBPlan,parser : DFParser,concentration_constants : ConcentrationConstants) -> None:
        super().__init__(plan,parser,concentration_constants)
       
      
        self.vars = ScBPlanVars.get_scb_plan_vars(plan,parser.map.num_courses)
        mapping = parser.map
        #Variable Bounds
        for var in self.vars.courses:
            self.s.add(0 <= var,var <= parser.map.num_courses)
        #Variables Equal to Plan Change approved
        self.set_equal(self.vars.calc_prereq,mapping.course_ints(plan.calc_prereq),"Calc courses are approved")
        self.set_equal(self.vars.intro,mapping.course_ints(plan.intro),"Intro courses are approved")
        self.set_equal(self.vars.intermediate,mapping.course_ints(plan.intermediate),"intermediate courses are approved")
        self.set_equal(self.vars.pathway1.courses ,mapping.course_ints(plan.pathway1.courses),"pathway 1 courses are approved")
        self.set_equal(self.vars.pathway2.courses ,mapping.course_ints(plan.pathway2.courses),"pathway 2 courses are approved")
        self.set_equal(self.vars.electives,mapping.course_ints(plan.electives),"Elective courses are approved")
        
        self.add(len(plan.capstone) == 1,"Single Capstone Course")
        self.add(self.vars.capstone == mapping[list(plan.capstone)[0]],"Capstone courses are approved")


    def create_model(self,vars: ScBPlanVars):
        parser = self.parser
        mp = self.parser.map
        
        #Courses are all distinct TODO : Capstone need not be distinct!
        # self.add(Distinct(vars.courses),"Courses are distinct")
        self.add_common_requirements()
        
        allcourses = set.union(*[vars.calc_prereq,vars.intro,vars.intermediate,vars.pathway1.courses,vars.pathway2.courses,vars.electives])
        self.add(Distinct(allcourses),"No course is double counted")


        #Pathway Reqs 
        self.satisfies_pathway(vars,vars.pathway1)
        self.satisfies_pathway(vars,vars.pathway2)

        #Scb Reqs
        self.add(len(allcourses) >= self.concentration_constants.NumberOfCoursesScB , "At least 15 courses in ScB Plan")

        self.add(And(len(vars.pathway1.courses) != 0,len(vars.pathway2.courses) != 0),"At least 2 pathways in ScB Plan")

        self.add(self.intersection(vars.courses,parser.arts_courses) <= self.concentration_constants.NumberOfArtsSocialCoursesScB,"4 or fewer Arts/Social Science courses in ScB Plan")

        self.add(len(vars.intermediate) >= self.concentration_constants.NumberOfArtsSocialCoursesScB,"At least 5 courses in ScB Plan")

        #At least 1 course from each intermediate category
        systemscourses = self.intersection(vars.intermediate,parser.intermediate_systems_courses)

        mathcourses = self.intersection(vars.intermediate,parser.intermediate_math_courses)

        foundationscourses = self.intersection(vars.intermediate,parser.intermediate_foundations_courses)


        self.add(And(
            systemscourses >= 1,mathcourses >= 1,foundationscourses >= 1)
        ,"Courses from all 3 intermediate categories for a Scb")

        #no intersection between pathway courses
        self.add(self.intersection(vars.pathway1.courses,vars.pathway2.courses),"No intersection between courses used for pathways")

        #Capstone course exists , is capstonable and is part of a pathway

        self.add(vars.capstone is not None,"ScB plan has 1 capstone course")

        self.add(self.var_inset(vars.capstone,parser.capstonable_course),"Capstone course is capstonable")

        self.add(self.var_in_varset(vars.capstone,vars.pathway1.courses.union(vars.pathway2.courses)),"Capstone course is part of pathway")



