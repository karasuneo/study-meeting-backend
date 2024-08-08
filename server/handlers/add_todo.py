from fastapi import APIRouter, HTTPException
from models.connection import DBConnection
from models.todo import Todo, TodoModel
from pydantic import BaseModel


class AddTodoRequest(BaseModel):
    title: str


class AddTodoResponse(BaseModel):
    id: str
    title: str
    isCompleted: bool


router = APIRouter()


@router.post("/todo", response_model=AddTodoResponse, status_code=201)
async def add_todo(request: AddTodoRequest):
    """
    ## TODO を追加する
    """
    try:
        conn = DBConnection.connect()

        todo = Todo(
            title=request.title,
        )

        add_todo_result = TodoModel.save(conn, todo)

        return AddTodoResponse(
            id=add_todo_result.id,
            title=add_todo_result.title,
            isCompleted=add_todo_result.is_completed,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
