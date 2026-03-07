from fastapi import APIRouter, status, Response, HTTPException
from fastapi.responses import JSONResponse
from bson import ObjectId
from app.database.user import showUserInfo
from app.utils.razorpay import orderCreator, orderValidator, load_order_info
from app.models.payments import orderCreateNotes, orderVerifyModel
from app.database.payments import (
    mark_sucessful_payment,
    create_payment_token,
    read_payment_token,
)


router = APIRouter(prefix="/pay", tags=["Razorpay"])


@router.post("/order/{user_id}")
def create_order(user_id: str, payload: orderCreateNotes):
    notes = payload.dict(exclude_unset=True, exclude_none=True)

    if not notes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Notes cannot be empty"
        )

    try:
        # Assuming showUserInfo is defined elsewhere
        user_data = showUserInfo(user_id)

        if not user_data:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
            )

        del user_data

        order = orderCreator(notes=notes)

        if not order:
            raise HTTPException(
                status_code=status.HTTP_417_EXPECTATION_FAILED,
                detail="Failed to create order",
            )

        return JSONResponse(content=order, status_code=status.HTTP_201_CREATED)

    except HTTPException:
        raise  # Let FastAPI handle known HTTP exceptions
    except Exception as err:
        print(f"Order creation error: {err}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@router.post("/verify")
def verify_order(payload: orderVerifyModel):
    try:
        # 1. Validate the signature
        is_valid = orderValidator(data=payload)

        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid payment signature",
            )

        # 2. Mark payment successful in your database
        # Assuming mark_sucessful_payment is defined elsewhere
        mark_status = mark_sucessful_payment(data=payload)

        if not mark_status:
            # 🔹 FIX: Changed from 100_CONTINUE to 500. If the DB fails after a user pays, it's a critical server error.
            print(f"CRITICAL: DB update failed for order {payload.order_id}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Payment captured but database update failed",
            )

        # 🔹 FIX: Return a dictionary so the frontend `result.success` check passes!
        return JSONResponse(content={"success": True}, status_code=status.HTTP_200_OK)

    except HTTPException:
        raise
    except Exception as err:
        print(f"Verification error: {err}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during verification",
        )


@router.post("/token/{user_id}")
def post_token(user_id: str):
    try:
        token = create_payment_token(user_id)

        if not token:
            return Response(status_code=status.HTTP_406_NOT_ACCEPTABLE)

        return JSONResponse(token, status_code=status.HTTP_201_CREATED)

    except Exception as err:
        raise Exception(f"{err} : error on order route")


@router.get("/token/{token_id}")
def get_token(token_id: str):
    try:

        token_data = read_payment_token(token_id)

        if not token_data:
            return Response(status_code=status.HTTP_401_UNAUTHORIZED)

        return JSONResponse(token_data, status_code=status.HTTP_200_OK)

    except Exception as err:
        raise Exception(f"{err} : error on order route")


@router.get("/invoice/{user_id}")
def get_invoice(team_id: str, pay_id: str):
    try:
        invoice_info = load_order_info(payment_id=pay_id, team_id=team_id)
        if not invoice_info:
            return Response(status_code=status.HTTP_404_NOT_FOUND)
        return JSONResponse(content=invoice_info)
    except Exception as err:
        return Response(status_code=status.HTTP_406_NOT_ACCEPTABLE)
