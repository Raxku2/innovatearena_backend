from fastapi import FastAPI
from fastapi.responses import JSONResponse, RedirectResponse
from app.routers.auth.googleAuthHandeller import router as AuthRouter
from app.routers.user.user_info import router as UserRouter
from app.routers.pay.payment import router as PaymentRouter
from app.middilwares.cors import cors_middleware
from app.database.connection import pingMongoDB_1
from app.routers.event.event import router as EventRouter

app = FastAPI(title="Innivatearena", version="pichu")

cors_middleware(app)

app.include_router(EventRouter)
app.include_router(AuthRouter)
app.include_router(UserRouter)
app.include_router(PaymentRouter)


@app.get("/")
def root():
    return RedirectResponse("/docs")
    # return "ok"


@app.get("/health")
def health():
    data = {"api": "UP"}
    data["DB_1"] = pingMongoDB_1()
    return JSONResponse(data)
