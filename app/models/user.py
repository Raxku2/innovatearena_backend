from pydantic import BaseModel


class userInfo(BaseModel):
    name: str | None = None
    dept: str | None = None
    batch: str | None = None
    phone: str | None = None
    reg_status: bool | None = None


class partnerInfo(BaseModel):
    name: str | None = None
    email: str | None = None


class partnerInfoUpdate(partnerInfo):
    team_id: str | None = None


class adminSetter(BaseModel):
    target: str
    param: str


class projectSubmit(BaseModel):
    project_title: str
    deployment: str
    repo: str
