import json
"""
    {
    "NumberOfArtsSocialCoursesAB" : 2,
    "NumberOfArtsSocialCoursesScB" : 4,
    "NumberOfIntermediateCoursesAB" : 3,
    "NumberOfIntermediateCoursesScB" : 5,
    "NumberOfCoursesAB" : 9,
    "NumberOfCoursesScB" : 15


}

    """

#Data class to store the above json

class ConcentrationConstants:

    def __init__(self,fl :str) -> None:
        """
        Args:
            fl (str): file location of json file
        """
        self.json_dict = json.load(open(fl))
        self.NumberOfArtsSocialCoursesAB = self.json_dict["NumberOfArtsSocialCoursesAB"]
        self.NumberOfArtsSocialCoursesScB = self.json_dict["NumberOfArtsSocialCoursesScB"]
        self.NumberOfIntermediateCoursesAB = self.json_dict["NumberOfIntermediateCoursesAB"]
        self.NumberOfIntermediateCoursesScB = self.json_dict["NumberOfIntermediateCoursesScB"]
        self.NumberOfCoursesAB = self.json_dict["NumberOfCoursesAB"]
        self.NumberOfCoursesScB = self.json_dict["NumberOfCoursesScB"]
        
