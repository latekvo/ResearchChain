from typing import Literal

from sqlalchemy import String, Boolean, Integer, create_engine, update, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session

from core.tools import utils
from core.tools.utils import gen_unix_time

# we have to heartbeat our workers once we run out of tasks, websocks should suffice
engine = create_engine("sqlite://", echo=True)


class CrawlTask(DeclarativeBase):
    __tablename__ = "crawl_tasks"

    uuid: Mapped[str] = mapped_column(primary_key=True)
    prompt: Mapped[str] = mapped_column(String())
    mode: Mapped[str] = mapped_column(String(12))
    timestamp: Mapped[int] = mapped_column(Integer())  # time added UNIX SECONDS

    executing: Mapped[bool] = mapped_column(Boolean())
    execution_date: Mapped[int] = mapped_column(Integer())  # time started completion

    completed: Mapped[bool] = mapped_column(Boolean())
    completion_date: Mapped[int] = mapped_column(Integer())  # time completed

    # fixme! figure out embedding_progression (n to 1)
    embedding_progression: Mapped[dict] = mapped_column()  # {model_name: count}
    # todo: replace with dynamically adjusted value
    base_amount_scheduled: Mapped[int] = mapped_column(Integer())


def db_add_crawl_task(prompt: str, mode: Literal["news", "wiki", "docs"] = "wiki"):
    # todo: replace arguments with a single WebQuery
    new_uuid = utils.gen_uuid()
    timestamp = utils.gen_unix_time()

    with Session(engine) as session:
        crawl_task = CrawlTask(
            uuid=new_uuid,
            prompt=prompt,
            mode=mode,
            timestamp=timestamp,
            executing=False,
            execution_date=0,
            completed=False,
            completion_date=0,
            base_amount_scheduled=100,
            embedding_progression={},
        )

        session.add(crawl_task)
        session.commit()

    return new_uuid


def db_set_crawl_executing(uuid: str):
    session = Session(engine)

    session.execute(
        update(CrawlTask)
        .where(CrawlTask.uuid.is_(uuid))
        .values(executing=True, execution_date=gen_unix_time())
    )

    session.commit()


def db_set_crawl_completed(uuid: str):
    session = Session(engine)

    session.execute(
        update(CrawlTask)
        .where(CrawlTask.uuid.is_(uuid))
        .values(completed=True, completion_date=gen_unix_time())
    )

    session.commit()


# fixme: this function should return a list of all tasks for management purposes (see below)
def db_get_crawl_task():
    session = Session(engine)

    query = select(CrawlTask).where(CrawlTask.completed.is_(False))
    crawl_task = session.scalars(query).one()

    if crawl_task is not None:
        db_set_crawl_executing(crawl_task.uuid)

    return crawl_task


# fixme cont. and this function should only return n of inComp and nonExec tasks, for workers
def db_get_incomplete_crawl_task():
    session = Session(engine)

    query = select(CrawlTask).where(
        CrawlTask.completed.is_(False) and CrawlTask.executing.is_(False)
    )

    # fixme: potential exception here
    crawl_task = session.scalars(query).one()

    if crawl_task is not None:
        db_set_crawl_executing(crawl_task.uuid)

    return crawl_task


def db_is_task_completed(uuid: str):
    session = Session(engine)

    query = select(CrawlTask).where(CrawlTask.uuid.is_(uuid))
    crawl_task = session.scalars(query).one()

    return crawl_task.completed


def db_are_tasks_completed(uuid_list: list[str]):
    # fixme: instead of multiple individual calls, make one composite one
    #        for our current usage this is not necessary

    total_completeness = True

    for uuid in uuid_list:
        task_completeness = db_is_task_completed(uuid)
        if task_completeness is False:
            total_completeness = False
            break

    return total_completeness


def db_is_crawl_task_fully_embedded(uuid: str, model_name: str):
    session = Session(engine)

    query = select(CrawlTask).where(CrawlTask.uuid.is_(uuid))
    crawl_task = session.scalars(query).one()

    baseline_count = crawl_task.base_amount_scheduled
    current_count = crawl_task.embedding_progression[model_name]

    return current_count >= baseline_count


def db_are_crawl_tasks_fully_embedded(uuid_list: str, model_name: str):
    # todo: replace this naive approach with a one-query solution
    for uuid in uuid_list:
        if db_is_crawl_task_fully_embedded(uuid, model_name) is False:
            return False

    return True


def db_increment_task_embedding_progression(uuid: str, model_name: str):
    session = Session(engine)

    query = select(CrawlTask).where(CrawlTask.uuid.is_(uuid))
    crawl_task = session.scalars(query).one()

    current_progression = crawl_task.embedding_progression
    current_count = current_progression[model_name]

    if current_count is not None:
        current_count += 1
    else:
        current_count = 1

    current_progression[model_name] = current_count

    session.execute(
        update(CrawlTask)
        .where(CrawlTask.uuid.is_(crawl_task.uuid))
        .values(embedding_progression=current_progression)
    )

    session.commit()
