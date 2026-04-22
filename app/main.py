from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.openapi.docs import get_swagger_ui_html
from app.routers.auth.googleAuthHandeller import router as AuthRouter
from app.routers.user.user_info import router as UserRouter
from app.routers.pay.payment import router as PaymentRouter
from app.middilwares.cors import cors_middleware
from app.database.connection import pingMongoDB_1
from app.routers.event.event import router as EventRouter
from app.routers.root.root import router as AdminRouter
from app.routers.judge.judgement import router as JudgeRouter
from app.utils.authhandeller import authenticate

from dotenv import load_dotenv
from os import getenv

load_dotenv()

app = FastAPI(
    title="Innovatearena",
    version=getenv("VERSION") if getenv("VERSION") else "Pikachu",
    # docs_url=None,
    # redoc_url=None,
    # openapi_url=None,
)

cors_middleware(app)

app.include_router(JudgeRouter)
app.include_router(EventRouter)
app.include_router(AuthRouter)
app.include_router(UserRouter)
app.include_router(PaymentRouter)
app.include_router(AdminRouter)


@app.get("/")
def root():
    return RedirectResponse("/docs")


# @app.get("/docs", include_in_schema=False)
# def protected_docs(user: str = Depends(authenticate)):
#     return get_swagger_ui_html(openapi_url="/openapi.json", title="Secure Docs")


@app.get("/health")
def health():
    data = {"api": "UP"}
    data["DB_1"] = pingMongoDB_1()
    return JSONResponse(data)
