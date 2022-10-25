class Course:
    def __init__(self,coursecode : str) -> None:
        if not re.match(r"[A-Z]{3,4}[0-9]{4,}[A-Z]?",coursecode):
            raise InvalidCourseCode(f"Recieved invalid course code {coursecode}")
        self.coursecode = coursecode
        self.numericcode = int(re.search(r"[0-9]{3,4}",coursecode).group(0))
        self.department = re.search(r"[A-Z]{3,4}",coursecode).group(0)
    
    def __eq__(self, other: object) -> bool:
        return isinstance(other,Course) and self.coursecode == other.coursecode
    
    def __repr__(self) -> str:
        return self.coursecode  
    def __hash__(self) -> int:
        return hash(self.coursecode)
    @classmethod
    def from_item(cls,item : dict) -> Course:
        return Course(item["subject_code"] + item["course_number"])

 decls_ids = [DeclarationIdentifier.get_identifier(i) for i in decls]
        candidate_decls = [i for i in decls_ids if self._partial_equal_to_declaration(i)]