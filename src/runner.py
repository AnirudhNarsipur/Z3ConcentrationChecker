from operator import index
import sys
import argparse

from ask_parser import get_all_plans
from concentration_constants import ConcentrationConstants
from model_ab import ABModel
from concentration_plans import ABPlan, ErrorPlan, ScBPlan
from model_scb import ScBModel
from dfparser import DFParser
import pandas as pd

def main(declaration_file : str,course_spec_file : str,pathway_spec_fl : str,concentration_constants_fl : str):
    str_plans = get_all_plans(declaration_file)
    parser = DFParser(course_spec_file,pathway_spec_fl)
    concentration_constants = ConcentrationConstants(concentration_constants_fl)
    res_dict  = {}
    res = None
    for (student_info,plan) in str_plans:
        # try:
        if isinstance(plan,ABPlan):
            model  = ABModel(plan,parser,concentration_constants)
            res = model.get_result()
        elif isinstance(plan,ScBPlan):
            model = ScBModel(plan,parser,concentration_constants)
            res = model.get_result()
        elif isinstance(plan,ErrorPlan):
            res = plan.error_message
        # print(f"For Student {student_info} result : {res}")
        student_res_dict = student_info.__dict__
        student_res_dict["Result"] = str(res)
            
        # except Exception as e:
        #     student_res_dict = student_info.__dict__
        #     student_res_dict["Result"] = f"Error running model: {e}" 
        if res_dict == {}:
                res_dict = {key: [val] for (key,val) in student_res_dict.items()}
        else:
                for key in res_dict:
                    res_dict[key].append(student_res_dict[key])
    print(res_dict)
    df =  pd.DataFrame(res_dict)
    df.to_csv("results.csv")
    return df


# coursespec_file = "course_specs/2021/course_spec.csv"
# pathwayspec_file = "course_specs/2021/pathway_spec.csv"
# concentration_constants_fl = "course_specs/2021/concentration_constants.json"
# declaration_file = "examples/sample_declarations/1T1F.json"
# parser= DFParser(coursespec_file,pathwayspec_file)
# res = main(declaration_file,coursespec_file,pathwayspec_file,concentration_constants_fl)

if __name__ == "__main__":
    #Parse arguments and pass them to main
    parser = argparse.ArgumentParser()
    parser.add_argument("--declaration_file", help="Path to declaration file")
    parser.add_argument("--course_spec_file", help="Path to course spec file",default="course_specs/2021/course_spec.csv")
    parser.add_argument("--pathway_spec_file", help="Path to pathway spec file",default="course_specs/2021/pathway_spec.csv"  )
    parser.add_argument("--concentration_constants_file", help="Path to concentration constants file",default="course_specs/2021/concentration_constants.json")
    args = parser.parse_args()
    main(args.declaration_file,args.course_spec_file,args.pathway_spec_file,args.concentration_constants_file)