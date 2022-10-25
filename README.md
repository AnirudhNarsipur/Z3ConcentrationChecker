# Setup 

Run : ``` pip install -r requirements.txt  ```
The complete spec used is located in course_specs/2021

A sample commnand is :

````
python3.9 src/runner.py --declaration_file "examples/sample_declarations/program_export_mixed-status.json"   --course_spec_file "course_specs/2021/course_spec.csv"  --pathway_spec_file "course_specs/2021/pathway_spec.csv"  --concentration_constants_file  "course_specs/2021/concentration_constants.json"
```
You can also use the default spec arguments above and just specify the declaration:
````
python3.9 src/runner.py --declaration_file "examples/sample_declarations/program_export_mixed-status.json"
```

The results will generated in a results.csv file in the project directory.
## Contributors
* Anirudh Narsipur