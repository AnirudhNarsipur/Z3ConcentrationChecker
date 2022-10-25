from __future__ import annotations
import json
from traceback import print_exc, print_exception
from typing import Tuple
from declaration_identifier import DeclarationIdentifier
from concentration_plans import ErrorPlan, Plan,ABPlan,ScBPlan
from pathway import Pathway
from degree_type import DegreeType
from student_info import StudentInfo




SCB_COURSE_CATEGORIES = ["Calculus Prerequisite","Introductory Courses","Intermediate Courses","Additional Courses","Capstone Course","Pathways"]
AB_COURSE_CATEGORIES = ["Calculus Prerequisite","Introductory Courses","Intermediate Courses","Additional Courses","Pathways"]
REQIDKEY = "requirement_uuid"



def get_category_dict(declr : dict,category : str) -> dict:
    """Get the Json dict of a category (Intermediate,pathways etc)

    Args:
        declr (dict): Dictionary representing declaration (json)

    Returns:
        dict: _description_
    """
    for catg in declr["requirements"]:
        if catg["title"] == category:
            return catg
    raise Exception(f"Could not find category {category}")

def get_all_uuids(decl_catg : dict):
    """Recursively get all uuids found in dict

    Args:
        dct (dict): _description_
    """
    ids = []
    if REQIDKEY in decl_catg:
        ids.append(decl_catg[REQIDKEY])
    for key in decl_catg:
        if isinstance(decl_catg[key],dict):
            ids += decl_catg[key] # very sus what is this ?
        elif isinstance(decl_catg[key],list):
            for item in decl_catg[key]:
                ids += get_all_uuids(item)
    return ids

def parse_pathways_dict(declr : dict):
    pathways_dict = get_category_dict(declr,"Pathways")
    groups_dict = pathways_dict["requirement_definitions"][0]["requirement_definitions"]
    pathway_uuid = {}
    for group in groups_dict:
        pathway_uuid[group["title"]] = get_all_uuids(group)
    return pathway_uuid
def get_course_code(item : dict):
    return  item["subject_code"] + item["course_number"]

def match_to_pathways(declr : dict , items : list):
    pathway_uuid = parse_pathways_dict(declr)
    pathway_courses = {key : [] for key in pathway_uuid.keys()}
    for item in items:
        for pathway_name in pathway_uuid:
            if item[REQIDKEY] in pathway_uuid[pathway_name]:
                pathway_courses[pathway_name].append(get_course_code(item))
                break
    res =  {key : set(pathway_courses[key]) for key in pathway_courses if len(pathway_courses[key]) != 0}
    assert len(res) != 0
    return res


def seperate_students(ls : list[dict]):
    banner_ids = set()
    for item in ls:
        banner_ids.add(item["banner_id"])
    students = []
    for bannerid in banner_ids:
        students.append(
            [item for item in ls if item["banner_id"] == bannerid]
        )
    return students

def create_plan(student_items : list[dict],defn : dict) -> Plan:
    if len(student_items) == 0:
        raise ValueError("Cannot create plan from empty list")
    else:
        degree_type = DegreeType.ScB if defn["degree_short"] == DegreeType.ScB.value else DegreeType.AB
        categories = SCB_COURSE_CATEGORIES if degree_type == DegreeType.ScB else AB_COURSE_CATEGORIES
        plan_dict = {i : set() for i in categories}
        for category in plan_dict:
            if category == "Pathways":
                plan_dict[category] = match_to_pathways(defn,student_items)
            else:
                catg_dict = get_category_dict(defn,category)
                catg_ids = get_all_uuids(catg_dict)
                matching_items = [item for item in student_items if item[REQIDKEY] in catg_ids]
                matching_items = [item["subject_code"] + item["course_number"] for item in matching_items]
                plan_dict[category] = set(matching_items)
        if degree_type == DegreeType.ScB:
            return ScBPlan.from_dict(plan_dict)
        else:
            return ABPlan.from_dict(plan_dict)

def remove_intermediate_overlap(plan : Plan) -> Plan:
    if isinstance(plan,ABPlan):
        return ABPlan(
            calc_prereq=plan.calc_prereq,
            intro=plan.intro,
            intermediate=plan.intermediate,
            pathway1=Pathway(name = plan.pathway1.name,courses=plan.pathway1.courses - plan.intermediate),
            electives=plan.electives
        )
    elif isinstance(plan,ScBPlan):
        return ScBPlan(
            calc_prereq=plan.calc_prereq,
            intro=plan.intro,
            intermediate=plan.intermediate,
            pathway1=Pathway(name = plan.pathway1.name,courses=plan.pathway1.courses - plan.intermediate),
            electives=plan.electives,
            pathway2= Pathway(name = plan.pathway2.name,courses=plan.pathway2.courses - plan.intermediate),
            capstone=plan.capstone
        )
    else:
        raise ValueError("Did not recieve a plan")

    
def get_all_plans(fl) -> list[Tuple[StudentInfo,Plan]]:
    file_dict = json.loads(open(fl).read())
    decls  = file_dict["program_definitions"]
    students = seperate_students(file_dict['plan_items'])
    plans =[]
    for student in students:
        studentinfo = StudentInfo(name=student[0]["display_name"],
        student_email=student[0]["email"],
        banner_id=student[0]["banner_id"],
        advisor_name=student[0]["advisor_name"],
        advisor_email=student[0]["advisor_email"])
        
        try:
            decl_ident = DeclarationIdentifier.get_identifier(student[0])
            if decl_ident.conc_code != "COMP":
                raise Exception("Cannot handle plans other than CS ScB or CS AB")
            student_decl = decl_ident.get_most_similar(decls)
            plan =  create_plan(student,student_decl)
            plan = remove_intermediate_overlap(plan)
            plans.append((studentinfo,plan))
        except Exception as ex:
            # print_exc()
            plans.append((studentinfo,ErrorPlan(str(ex))))
    return plans