from pydantic import BaseModel


class judgementType(BaseModel):
    judgement: bool = True
    marks: int
    pos: None | int = None
