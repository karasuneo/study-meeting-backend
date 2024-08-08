from fastapi import APIRouter, HTTPException
from models.connection import DBConnection
from models.todo import TodoModel
from pydantic import BaseModel


class CompleteTodoResponse(BaseModel):
    id: str
    title: str
    isComplete: bool


router = APIRouter()


@router.put(
    "/todo/complete/{todo_id}", response_model=CompleteTodoResponse, status_code=201
)
async def complete_todo(todo_id: str):
    """
    ## TODO を完了する
    """
    try:
        conn = DBConnection.connect()

        complete_todo_result = TodoModel.update_true(conn, todo_id)

        return CompleteTodoResponse(
            id=complete_todo_result.id,
            title=complete_todo_result.title,
            isComplete=complete_todo_result.is_completed,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
