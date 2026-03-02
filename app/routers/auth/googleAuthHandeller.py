from fastapi import APIRouter, status, Response
from fastapi.responses import JSONResponse
from app.utils.authhandeller import handle_success
from app.database.auth import viewUser, createUser
from bson import ObjectId

router = APIRouter(prefix="/auth", tags=["Google Auth"])


@router.get("/{token}")
def authTokenVerify(token: str):
    try:
        tokenData = handle_success(token)

        if not tokenData:
            return Response(status_code=status.HTTP_401_UNAUTHORIZED)

        userData = viewUser(useremail=tokenData.get("email"))

        if not userData:
            new_team_id = ObjectId()
            user_id = createUser(
                username=tokenData.get("name"),
                useremail=tokenData.get("email"),
                userdp=tokenData.get("picture"),
                team_id=new_team_id,
            )
        else:
            return JSONResponse(userData)

        if not user_id:
            return Response(status_code=status.HTTP_406_NOT_ACCEPTABLE)

        return JSONResponse(
            {
                "_id": user_id,
                "name": tokenData.get("name"),
                "email": tokenData.get("email"),
                "dp": tokenData.get("picture"),
                "type": "user",
                "team_id": str(new_team_id),
            },
            status_code=status.HTTP_201_CREATED,
        )

    except Exception as err:
        print(err)
        raise Exception(err)
