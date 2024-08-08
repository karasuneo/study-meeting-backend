from typing import List

from fastapi import APIRouter, HTTPException
from models.connection import DBConnection
from models.todo import TodoModel
from pydantic import BaseModel


class GetAllTodo(BaseModel):
    id: str
    title: str
    isCompleted: bool


class GetAllTodoResponse(BaseModel):
    todos: List[GetAllTodo]


router = APIRouter()


@router.get("/todo", response_model=GetAllTodoResponse, status_code=200)
async def get_todo():
    """
    ## TODO を取得する
    """
    try:
        conn = DBConnection.connect()

        complete_todo_result = TodoModel.get(conn)

        get_todo_result = [
            GetAllTodo(
                id=todo.id,
                title=todo.title,
                isCompleted=todo.is_completed,
            )
            for todo in complete_todo_result
        ]

        return GetAllTodoResponse(
            todos=get_todo_result,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
