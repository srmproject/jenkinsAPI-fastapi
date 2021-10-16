from fastapi import FastAPI
from app.api.jenkins import router as jenkinsrouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.core.exceptions import jenkins as jenkinsexception


app = FastAPI()
app.include_router(jenkinsrouter)

origins = [
    "http://localhost",
    "http://localhost:8080"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/healthcheck")
async def healthcheck():
    return {"message": "pingpong"}


@app.exception_handler(jenkinsexception.FailConnection)
async def validation_exception_handler(request, exc):
    '''jenkins 서버 연결실패 오류 핸들러'''
    return JSONResponse(
        status_code=500,
        content=jsonable_encoder({"error": "jekins서버 연결실패"})
    )
