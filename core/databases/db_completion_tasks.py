from typing import Optional
from sqlalchemy import String, TEXT, Integer, Boolean, select, update
from sqlalchemy.orm import Mapped, mapped_column, Session, relationship

from core.databases import defaults
from core.databases.db_base import Base, engine
from core.databases.db_crawl_tasks import CrawlTask
from core.tools import utils
from core.tools.utils import gen_unix_time, page_to_range


class CompletionTask(Base):
    __tablename__ = "completion_tasks"

    uuid: Mapped[str] = mapped_column(primary_key=True)
    prompt: Mapped[str] = mapped_column(TEXT())  # make sure postgres uses "TEXT" here
    mode: Mapped[str] = mapped_column(String(12))
    timestamp: Mapped[int] = mapped_column(Integer())  # time added
    completion_result: Mapped[str] = mapped_column(TEXT())  # "TEXT" type here as well
    executing: Mapped[bool] = mapped_column(Boolean())
    execution_date: Mapped[int] = mapped_column(Integer())  # time started completion

    completed: Mapped[bool] = mapped_column(Boolean())
    completion_date: Mapped[int] = mapped_column(Integer())  # time completed

    required_crawl_tasks: Mapped[list["CrawlTask"]] = relationship()


def db_add_completion_task(prompt, mode) -> str:
    new_uuid = utils.gen_uuid()
    timestamp = utils.gen_unix_time()

    with Session(engine) as session:
        completion_task = CompletionTask(
            uuid=new_uuid,
            prompt=prompt,
            mode=mode,
            timestamp=timestamp,
            executing=False,
            execution_date=0,
            completed=False,
            completion_result="N/A",
            completion_date=0,
            required_crawl_tasks=[],
        )

        session.add(completion_task)
        session.commit()

    return new_uuid


def db_get_completion_tasks_by_page(
    page: int, per_page: int = defaults.ITEMS_PER_PAGE
) -> list[CompletionTask]:
    with Session(engine) as session:
        session.expire_on_commit = False

        start, stop = page_to_range(page, per_page)
        query = select(CompletionTask).slice(start, stop)
        results = list(session.scalars(query))
        session.expunge_all()

        return results


def db_get_completion_task_by_uuid(uuid: int) -> CompletionTask:
    with Session(engine) as session:
        session.expire_on_commit = False

        query = select(CompletionTask).where(CompletionTask.uuid == uuid)
        result = session.scalars(query).one()
        session.expunge_all()
        return result


def db_set_completion_task_executing(uuid: str):
    with Session(engine) as session:
        session.execute(
            update(CompletionTask)
            .where(CompletionTask.uuid == uuid)
            .values(executing=True, execution_date=gen_unix_time())
        )

        session.commit()


def db_get_incomplete_completion_tasks(amount: int = 1):
    with Session(engine) as session:
        session.expire_on_commit = False

        query = (
            select(CompletionTask)
            # point of notice! is_ may need to be replaced with ==
            .where(CompletionTask.completed.is_(False))
            .where(CompletionTask.executing.is_(False))
            .limit(amount)
        )

        results = list(session.scalars(query).all())

        for task in results:
            db_set_completion_task_executing(task.uuid)

        session.expunge_all()

        return results


def db_release_executing_tasks(uuid_list: list[str]):
    with Session(engine) as session:
        session.execute(
            update(CompletionTask)
            .where(CompletionTask.uuid.in_(uuid_list))
            .values(executing=False, execution_date=0)
        )

        session.commit()


def db_required_crawl_tasks_for_uuid(uuid: str):
    # TODO!!!
    # currently summarizer pings the db with this command
    # instead we want it to ping the db for already crawl-ready summary tasks,
    # while not holding onto any non-ready tasks
    # More details: PR #47

    with Session(engine) as session:
        session.expire_on_commit = False

        query = select(CrawlTask).where(CrawlTask.required_by_uuid == uuid)

        results = list(session.scalars(query).all())

        session.expunge_all()

        return results


def db_update_completion_task_after_summarizing(summary: str, uuid: str):
    with Session(engine) as session:
        session.execute(
            update(CompletionTask)
            .where(CompletionTask.uuid == uuid)
            .values(
                completed=True,
                completion_result=summary,
                completion_date=gen_unix_time(),
            )
        )

        session.commit()
