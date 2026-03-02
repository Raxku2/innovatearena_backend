from fastapi import FastAPI
from fastapi.responses import JSONResponse, RedirectResponse
from app.routers.auth.googleAuthHandeller import router as AuthRouter
from app.routers.user.user_info import router as UserRouter
from app.routers.pay.payment import router as PaymentRouter
from app.middilwares.cors import cors_middleware


app = FastAPI(title="Innivatearena", version="pichu")

cors_middleware(app)


app.include_router(AuthRouter)
app.include_router(UserRouter)
app.include_router(PaymentRouter)


@app.get("/")
def root():
    # return RedirectResponse("/docs")
    return "ok"
