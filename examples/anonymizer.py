# This script anonymizes program exports JSONs downloaded from ASK.
# It can handle JSON exports with one or many students. It replaces
# each student name, id, email and each advisor name/email value. Students
# get a temp ID number that is used to generate their name, id, and email.
# All advisors are set to Josiah Carberry.

# The file path name is currently hardcoded to the one in Kathi's directory.
# Change the os.chdir command in the first line of the anonymize function
# to use a different working directory. 

# The file currently hardcodes the file to run on.

import json
import os

# The temp ID generator
next_name_num = 0
def get_next_name_num():
    global next_name_num
    next_name_num = next_name_num + 1
    return next_name_num

def anonymize(filename):
  # os.chdir("/Users/kathi/Documents/r/brown/project-cs-advising/examples/raw-json")
  fp = open(filename)
  data = json.load(fp)
  fp.close()
  masks = {}
  plans = data["plan_items"]
  for item in plans:
      item_tag = get_next_name_num()
      if not(item["display_name"] in masks):
          masks[item["display_name"]] = "Student " + str(item_tag)
      if not(item["banner_id"] in masks):
          masks[item["banner_id"]] = "B" + str(10000000 + item_tag)
      if not(item["email"] in masks):
          masks[item["email"]] = "s" + str(item_tag) + "@brown.edu"
      if not(item["advisor_name"] in masks):
          masks[item["advisor_name"]] = "Josiah Carberry"
      if not(item["advisor_email"] in masks):
          masks[item["advisor_email"]] = "carberry@brown.edu"
  # print(masks)
  for key, value in masks.items():
      subst_str = "sed -i '' 's/" + key + "/" + value + "/g' " + filename 
      os.system(subst_str)

def main():
    args = os.sys.argv[1:]
    print(args[0])
    #anonymize(args[0])

# anonymize("program_export_mixed-status.json")
