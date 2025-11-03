from src.settings import settings
from sqlalchemy import create_engine, text
from pydantic import BaseModel


class User(BaseModel):
    name: str
    email: str


class Database:
    def __init__(
        self,
        driver=settings.database_driver,
        host=settings.database_host,
        name=settings.database_name,
        password=settings.database_password,
        port=settings.database_port,
        username=settings.database_username,
    ):
        self.engine = create_engine(
            f"{driver}://{username}:{password}@{host}:{port}/{name}"
        )

    def create_user(self, name: str, email: str) -> str:
        with self.engine.begin() as connection:
            statement = text(
                """
                INSERT INTO users
                (name, email)
                VALUES (:name, :email)
                RETURNING id;
                """
            )
            result = connection.execute(
                statement=statement, parameters={"name": name, "email": email}
            )
            user_id = result.scalar_one()

            return str(user_id)

    def get_user(self, user_id: int) -> User | None:
        with self.engine.begin() as connection:
            statement = text(
                """
                SELECT name, email
                FROM users
                WHERE id = :id;
                """
            )
            result = connection.execute(statement=statement, parameters={"id": user_id})
            result_first = result.fetchone()

            if not result_first:
                return None

            user = User(name=result_first[0], email=result_first[1])

            return user

    def delete_user(self, id: int):
        with self.engine.begin() as connection:
            statement = text(
                """
                DELETE FROM users
                WHERE id = :id
                RETURNING id;
                """
            )
            result = connection.execute(statement, {"id": id})
            deleted_id = result.scalar_one_or_none()

            return deleted_id is not None

    def update(self, id: int, name: str, email: str):
        with self.engine.begin() as connection:
            statement = text(
                """
                UPDATE users
                SET name = :name, email = :email
                WHERE id = :id
                RETURNING id;
                """
            )
            result = connection.execute(statement, {"id": id, "name": name, "email": email})
            updated_id = result.scalar_one_or_none()

            return updated_id is not None


if __name__ == "__main__":
    breakpoint()
