from fastapi import APIRouter, status, Response, Request
from fastapi.responses import JSONResponse
from app.utils.authhandeller import handle_success
from bson import ObjectId
from app.models.user import userInfo, partnerInfo, partnerInfoUpdate, projectSubmit
from app.database.user import showUserInfo, updateUserInfo, mark_attendence, add_submits
from app.database.partner import (
    showPartner,
    createPartner,
    updatePartner,
    removePartner,
)


router = APIRouter(prefix="/user", tags=["User"])



@router.get("/partner/{partner_email}")
def get_partner_info(partner_email: str):
    try:
        res = showPartner(partner_email)

        if not res:
            return Response(status_code=status.HTTP_404_NOT_FOUND)

        return JSONResponse(res)
    except Exception as err:
        return Response(status_code=status.HTTP_417_EXPECTATION_FAILED)


@router.post("/partner/{user_id}")
def post_partner_info(user_id: str, payload: partnerInfo):
    try:
        res = createPartner(payload, user_id)

        if not res:
            return Response(status_code=status.HTTP_501_NOT_IMPLEMENTED)

        return Response(status_code=status.HTTP_201_CREATED)
    except Exception as err:
        print(err)
        return Response(status_code=status.HTTP_417_EXPECTATION_FAILED)


@router.put("/partner/{user_id}")
def put_partner_info(user_id: str):
    try:
        res = updatePartner(user_id)

        if not res:
            return Response(status_code=status.HTTP_304_NOT_MODIFIED)

        return Response(status_code=status.HTTP_200_OK)
    except Exception as err:
        return Response(status_code=status.HTTP_417_EXPECTATION_FAILED)


@router.delete("/partner/{user_id}")
def delete_partner_info(user_id: str):
    try:
        res = removePartner(user_id)

        if not res:
            return Response(status_code=status.HTTP_501_NOT_IMPLEMENTED)

        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except Exception as err:
        # print(err)
        return Response(status_code=status.HTTP_417_EXPECTATION_FAILED)


@router.put("/attendence/{team_id}")
def put_attendence(team_id: str, request: Request):
    try:
        res = mark_attendence(team_id=team_id, request=request)

        if res == False:
            return Response(status_code=status.HTTP_501_NOT_IMPLEMENTED)
        if res == None:
            return Response(status_code=status.HTTP_401_UNAUTHORIZED)

        return Response(status_code=status.HTTP_200_OK)
    except Exception as err:
        print(err)
        return Response(status_code=status.HTTP_417_EXPECTATION_FAILED)


@router.put("/project/{team_id}")
def put_project(team_id: str, request: Request, payload: projectSubmit):
    try:
        res = add_submits(team_id=team_id, request=request, data=payload)

        if res == False:
            return Response(status_code=status.HTTP_501_NOT_IMPLEMENTED)
        if res == None:
            return Response(status_code=status.HTTP_401_UNAUTHORIZED)

        return Response(status_code=status.HTTP_200_OK)
    except Exception as err:
        # print(err)
        return Response(status_code=status.HTTP_417_EXPECTATION_FAILED)


@router.get("/{user_id}")
def get_user_info(user_id: str):
    try:
        res = showUserInfo(user_id)

        if not res:
            return Response(status_code=status.HTTP_404_NOT_FOUND)

        return JSONResponse(res)
    except Exception as err:
        print(err)
        return Response(status_code=status.HTTP_417_EXPECTATION_FAILED)


@router.put("/{user_id}")
def put_user_info(user_id: str, payload: userInfo):
    try:
        res = updateUserInfo(user_id=user_id, data=payload)

        if not res:
            return Response(status_code=status.HTTP_304_NOT_MODIFIED)

        return JSONResponse(res)
    except Exception as err:
        return Response(status_code=status.HTTP_417_EXPECTATION_FAILED)
