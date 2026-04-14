from pydantic import BaseModel


class judgementType(BaseModel):
    judgement: bool = True
    marks: int | float
    pos: None | int = None
