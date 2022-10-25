import pandas as pd
import re 
from coursemap import CourseMap
from pathwayreq import PathwayReq

class DFParser:

    def __init__(self,course_spec_file : str,pathway_spec_file : str) -> None:
        self.df = pd.read_csv(course_spec_file)
        self.pf = pd.read_csv(pathway_spec_file)
        self.all_courses = self.df["Course"].tolist()
        course_int = {self.all_courses[i]: i for i in range(len(self.all_courses))}
        self.map =  CourseMap(course_int)
        self.pathwayreqs = self.create_pathways()

    def create_pathways(self) -> list[PathwayReq]:
        pf = self.pf
        pathways = []
        for index in range(len(self.pf)):
            officialname = str(pf.iloc[index]["OfficialPathwayName"])
            reqcolname = str(pf.iloc[index]["Pathways"])
            core = self.get_col(reqcolname,"c")
            related = self.get_col(reqcolname,"r")
            grad = self.get_col(reqcolname,"g")
            intermediate = self.parse_intermediate(str(pf.iloc[index]["IntermediateCategories"]))
            pathways.append(
                PathwayReq(
                    name=officialname,
                    core=core,
                    intermediate=intermediate,
                    grad=grad,
                    related=related
                )
            )
        return pathways

    def get_pathway(self,name) -> PathwayReq:
        return list(filter(lambda p : p.name == name,self.pathwayreqs))[0]
    def parse_intermediate(self,reqs : str) -> list[list[int]]:
        req_catgs = reqs.split("|")
        indiv = [[i.replace(" ","") for i in elem.split(";")] for elem in req_catgs]
        res =[]
        for elem in indiv:
            tmp = []
            for indiv in elem:
                if indiv in self.pf["CategorySymbol"].tolist(): 
                    symb_col = str(self.pf[self.pf["CategorySymbol"] == indiv]["CategoryColumn"].tolist()[0])
                    tmp += self.get_col(symb_col)
                else:
                    tmp.append(self.map[indiv])
            res.append(tmp)
        return res

    def get_coursecode(self,course : str) -> int:
        return  int(re.search(r"[0-9]{3,4}",course).group(0))

    def get_coursedept(self,course:str) -> str:
        return re.search(r"[A-Z]{3,4}",course).group(0)

    def get_col(self,col : str,filter : str = "t") -> list[int]: 
        course_strs = self.df[self.df[col] == filter]["Course"].tolist()
        return [self.map[course] for course in course_strs]
    @property
    def calc_courses(self) -> list[int]:
        return self.get_col("Calculus")
    @property
    def outside_elective(self) -> list[int]:
        return self.get_col("OutsideElective")
    
    @property
    def arts_courses(self) -> list[int]:
        return self.get_col("ArtsCourses")
    
    @property
    def intermediate_foundations_courses(self) -> list[int]:
        return self.get_col("Foundations")
    
    @property
    def intermediate_systems_courses(self) -> list[int]:
        return self.get_col("Systems")
    
    @property
    def intermediate_math_courses(self) -> list[int]:
        catgs = ["LinearAlgebra","ProbabilityStatistics"	,"Calculus"	]
        courses = [self.get_col(catg) for catg in catgs]
        res = []
        for ls in courses:
            res += ls
        return res


    @property
    def intermediate_courses(self) -> list[int]:
        catgs = ["LinearAlgebra","ProbabilityStatistics","Calculus"	,"Foundations"	,"Systems"]
        courses = [self.get_col(catg) for catg in catgs]
        res = []
        for ls in courses:
            res += ls
        return res
    @property
    def thousand_level_cs(self) -> list[int]:
        cscourses = filter(lambda c : self.get_coursedept(c) == "CSCI",self.all_courses)
        thousandcs = filter(lambda c : self.get_coursecode(c) > 1_000,cscourses)
        return self.map.course_ints(list(thousandcs))
    @property
    def electives(self) -> list[int]:
        outsideelectives = self.get_col("OutsideElective")
        thousandcs = self.thousand_level_cs
        return thousandcs + outsideelectives

    @property
    def capstonable_course(self) -> list[int]:
        return self.get_col("Capstone")