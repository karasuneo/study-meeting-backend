from dataclasses import dataclass
from typing import List, Optional

from psycopg2.extensions import connection
from ulid import ULID


@dataclass
class Todo:
    def __init__(
        self, title: str, id: Optional[str] = None, is_completed: bool = False
    ):
        self.id = id or str(ULID())
        self.title = title
        self.is_completed = is_completed


class TodoModel:
    @staticmethod
    def get(conn: connection) -> List[Todo]:
        with conn as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT id, title, is_completed FROM todos")
                result = cursor.fetchall()

                if result is None:
                    raise Exception("Failed to get todos")

                return [
                    Todo(
                        id=id,
                        title=title,
                        is_completed=is_completed,
                    )
                    for id, title, is_completed in result
                ]

    @staticmethod
    def save(conn: connection, todo: Todo) -> Todo:
        with conn as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO todos (id, title) VALUES (%s, %s) RETURNING id",
                    (
                        todo.id,
                        todo.title,
                    ),
                )
                result = cursor.fetchone()
                if result is None:
                    raise Exception("Failed to save todo")
                id = result[0]

                return Todo(
                    id=id,
                    title=todo.title,
                )

    @staticmethod
    def update_true(conn: connection, id: str) -> Todo:
        with conn as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "UPDATE todos SET is_completed = true WHERE id = %s RETURNING id, title, is_completed",
                    (id,),
                )
                result = cursor.fetchone()
                if result is None:
                    raise Exception("Failed to update todo")
                id, title, is_completed = result

                return Todo(
                    id=id,
                    title=title,
                    is_completed=is_completed,
                )

    @staticmethod
    def update_false(conn: connection, id: str) -> Todo:
        with conn as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "UPDATE todos SET is_completed = false WHERE id = %s RETURNING id, title, is_completed",
                    (id,),
                )
                result = cursor.fetchone()
                if result is None:
                    raise Exception("Failed to update todo")
                id, title, is_completed = result

                return Todo(
                    id=id,
                    title=title,
                    is_completed=is_completed,
                )

    @staticmethod
    def delete(conn: connection, id: str) -> None:
        with conn as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "DELETE FROM todos WHERE id = %s",
                    (id,),
                )
