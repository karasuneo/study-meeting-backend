from fastapi import APIRouter
from models.connection import DBConnection
from models.todo import TodoModel

router = APIRouter()


@router.delete("/todo/{todo_id}", status_code=204)
async def complete_todo(todo_id: str):
    """
    ## TODO を削除する
    """
    conn = DBConnection.connect()
    TodoModel.delete(conn, todo_id)

    return None
