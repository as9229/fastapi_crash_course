from db import new_session, TaskORM

from sqlalchemy import select

from schemas import STaskAdd, STask


class TaskRepository:

    @classmethod
    async def add_one(cls, data: STaskAdd):
        async with new_session() as session:
            task_dict = data.model_dump()
            task = TaskORM(**task_dict)
            session.add(task)
            await session.flush()
            await session.commit()
            return task.id

    @classmethod
    async def get_all(cls) -> list[STask]:
        async with new_session() as session:
            query = select(TaskORM)
            result = await session.execute(query)
            tasks_orm_obj = result.scalars().all()
            tasks_schemas = [STask.model_validate(obj) for obj in tasks_orm_obj]
            return tasks_schemas
