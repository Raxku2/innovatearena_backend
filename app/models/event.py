from pydantic import BaseModel


class eventDataType(BaseModel):
    regOpen: str | None = None
    regClose: str | None = None
    eventDate: str | None = None
    teamSize: str | None = None


class eventOrganizers(BaseModel):
    name: str
    role: str
    email: str

class scheduleDataType(BaseModel):
    title: str | None = None
    time: str | None = None
    description: str | None = None

class rulesDataType(BaseModel):
    title:str
    description:str


