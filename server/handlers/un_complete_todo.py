from fastapi import APIRouter, HTTPException
from models.connection import DBConnection
from models.todo import TodoModel
from pydantic import BaseModel


class UnCompleteTodoRequest(BaseModel):
    id: str


class UnCompleteTodoResponse(BaseModel):
    id: str
    title: str
    is_completed: bool


router = APIRouter()


@router.put("/todo/uncomplete", response_model=UnCompleteTodoResponse, status_code=201)
async def un_complete_todo(request: UnCompleteTodoRequest):
    """
    ## TODO を未完了にする
    """
    try:
        conn = DBConnection.connect()

        complete_todo_result = TodoModel.update_false(conn, request.id)

        return UnCompleteTodoResponse(
            id=complete_todo_result.id,
            title=complete_todo_result.title,
            is_completed=complete_todo_result.is_completed,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
