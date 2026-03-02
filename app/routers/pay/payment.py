from fastapi import APIRouter, status, Response
from fastapi.responses import JSONResponse
from bson import ObjectId
from app.database.user import showUserInfo
from app.utils.razorpay import orderCreator, orderValidator
from app.models.payments import orderCreateNotes, orderVerifyModel
from app.database.payments import mark_sucessful_payment

router = APIRouter(prefix="/pay", tags=["Razorpay"])


@router.post("/order/{user_id}")
def create_order(user_id: str, payload: orderCreateNotes):
    notes = payload.dict(exclude_unset=True, exclude_none=True)

    if not notes:
        return Response(status_code=status.HTTP_400_BAD_REQUEST)

    try:
        user_data = showUserInfo(user_id)

        if not user_data:
            return Response(status_code=status.HTTP_401_UNAUTHORIZED)

        del user_data

        order = orderCreator(notes=notes)

        if not order:
            return Response(status_code=status.HTTP_417_EXPECTATION_FAILED)

        return JSONResponse(order, status_code=status.HTTP_201_CREATED)

    except Exception as err:
        raise Exception(f"{err} : error on order route")


@router.post("/verify")
def verify_order(payload: orderVerifyModel):
    try:

        order = orderValidator(data=payload)

        if not order:
            return Response(status_code=status.HTTP_401_UNAUTHORIZED)

        mark_status = mark_sucessful_payment(data=payload)

        if not mark_status:
            return Response(status_code=status.HTTP_100_CONTINUE)

        return JSONResponse(order, status_code=status.HTTP_200_OK)

    except Exception as err:
        raise Exception(f"{err} : error on order route")
