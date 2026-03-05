from pydantic import BaseModel


class eventDataType(BaseModel):
    regOpen: str | None = None
    regClose: str | None = None
    eventDate: str | None = None
    teamSize: str | None = None


class eventOrganizers(BaseModel):
    name: str | None = None
    role: str | None = None
    dp: str | None = None


class scheduleDataType(BaseModel):
    title: str | None = None
    time: str | None = None


class rulesDataType(BaseModel):
    title: str
    description: str
