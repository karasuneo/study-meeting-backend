from fastapi import APIRouter, HTTPException
from models.connection import DBConnection
from models.todo import TodoModel
from pydantic import BaseModel


class CompleteTodoRequest(BaseModel):
    id: str


class CompleteTodoResponse(BaseModel):
    id: str
    title: str
    is_completed: bool


router = APIRouter()


@router.put("/todo/complete", response_model=CompleteTodoResponse, status_code=201)
async def complete_todo(request: CompleteTodoRequest):
    """
    ## TODO を完了する
    """
    try:
        conn = DBConnection.connect()

        complete_todo_result = TodoModel.update_true(conn, request.id)

        return CompleteTodoResponse(
            id=complete_todo_result.id,
            title=complete_todo_result.title,
            is_completed=complete_todo_result.is_completed,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
