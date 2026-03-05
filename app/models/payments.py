from pydantic import BaseModel


class orderCreateNotes(BaseModel):
    user_id: str
    team_id: str
    username: str

class orderVerifyModel(orderCreateNotes):
    order_id: str
    payment_id: str
    signature: str
