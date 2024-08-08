from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from handlers.add_todo import router as add_todo_router
from handlers.complete_todo import router as complete_todo_router
from handlers.delete_todo import router as delete_todo_router
from handlers.get_todo import router as get_todo_router
from handlers.un_complete_todo import router as un_complete_todo_router
from starlette.requests import Request

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(get_todo_router)
app.include_router(add_todo_router)
app.include_router(delete_todo_router)
app.include_router(complete_todo_router)
app.include_router(un_complete_todo_router)


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail},
    )
