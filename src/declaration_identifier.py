from __future__ import annotations
from dataclasses import dataclass

from typing import Optional

@dataclass
class DeclarationIdentifier:
    degree_short : str
    conc_code : str 
    track_code : Optional[str]
    term_id : int 

    def _partial_equal_to_declaration(self,other : DeclarationIdentifier) -> bool:
        return self.degree_short == other.degree_short and self.conc_code == other.conc_code and self.track_code == other.track_code and self.term_id >= other.term_id
    
    @classmethod
    def get_identifier(cls,dct : dict) -> DeclarationIdentifier:
        if dct["term_id"] is None:
            dct["term_id"] = 0
        return cls(dct["degree_short"],dct["conc_code"],dct["track_code"],int(dct["term_id"]))

    def get_most_similar(self,decls : dict) -> dict:
        best_candidate = None
        for dec in decls:
            dec_id = DeclarationIdentifier.get_identifier(dec)
            if best_candidate is None and self._partial_equal_to_declaration(dec_id):
                best_candidate = dec
            elif self._partial_equal_to_declaration(dec_id) and dec_id.term_id >= int(best_candidate["term_id"]):
                best_candidate = dec
        if best_candidate is None:
            raise ValueError("no suitable declaration")
        else:
            return best_candidate