from typing import Literal, Optional

from sqlalchemy import (
    String,
    Boolean,
    Integer,
    update,
    select,
    ForeignKey,
    insert,
)
from sqlalchemy.orm import Mapped, mapped_column, Session, relationship

from core.databases import defaults
from core.databases.db_base import Base, engine
from core.tools import utils
from core.tools.utils import gen_unix_time, page_to_range


class EmbeddingProgression(Base):
    __tablename__ = "embedding_progressions"

    uuid: Mapped[str] = mapped_column(primary_key=True)

    crawl_uuid: Mapped[str] = mapped_column(ForeignKey("crawl_tasks.uuid"))

    embedder_name: Mapped[str] = mapped_column(String())
    embedding_amount: Mapped[int] = mapped_column(Integer(), default=0)
    timestamp: Mapped[int] = mapped_column(Integer())  # time added UNIX SECONDS


class CrawlTask(Base):
    __tablename__ = "crawl_tasks"

    uuid: Mapped[str] = mapped_column(primary_key=True)
    prompt: Mapped[str] = mapped_column(String())
    mode: Mapped[str] = mapped_column(String(12))
    timestamp: Mapped[int] = mapped_column(Integer())  # time added UNIX SECONDS

    executing: Mapped[bool] = mapped_column(Boolean())
    execution_date: Mapped[int] = mapped_column(Integer())  # time started completion

    completed: Mapped[bool] = mapped_column(Boolean())
    completion_date: Mapped[int] = mapped_column(Integer())  # time completed

    embedding_progression: Mapped[list["EmbeddingProgression"]] = relationship()
    base_amount_scheduled: Mapped[int] = mapped_column(Integer())
    required_by_uuid: Mapped[Optional[str]] = mapped_column(
        ForeignKey("completion_tasks.uuid"), nullable=True
    )


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
            required_by_uuid=None,
            embedding_progression=[],
        )

        session.add(crawl_task)
        session.commit()

    return new_uuid


def db_get_crawl_tasks_by_page(
    page: int, per_page: int = defaults.ITEMS_PER_PAGE
) -> list[CrawlTask]:
    with Session(engine) as session:
        session.expire_on_commit = False

        start, stop = page_to_range(page, per_page)
        query = select(CrawlTask).slice(start, stop)
        results = list(session.scalars(query))
        session.expunge_all()

        return results


def db_get_crawl_task_by_uuid(uuid: int) -> CrawlTask:
    with Session(engine) as session:
        session.expire_on_commit = False

        query = select(CrawlTask).where(CrawlTask.uuid == uuid)
        result = session.scalars(query).one()
        session.expunge_all()

        return result


def db_set_crawl_executing(uuid: str):
    with Session(engine) as session:
        session.execute(
            update(CrawlTask)
            .where(CrawlTask.uuid == uuid)
            .values(executing=True, execution_date=gen_unix_time())
        )

        session.commit()


def db_set_crawl_completed(uuid: str):
    with Session(engine) as session:
        session.execute(
            update(CrawlTask)
            .where(CrawlTask.uuid == uuid)
            .values(completed=True, completion_date=gen_unix_time())
        )

        session.commit()


# fixme cont. and this function should only return n of inComp and nonExec tasks, for workers
def db_get_incomplete_crawl_task():
    with Session(engine) as session:
        session.expire_on_commit = False

        query = (
            select(CrawlTask)
            .where(CrawlTask.completed == False)
            .where(CrawlTask.executing == False)
            .limit(1)
        )

        crawl_task = session.scalars(query).one_or_none()

        if crawl_task is not None:
            db_set_crawl_executing(crawl_task.uuid)

        session.expunge_all()

        return crawl_task


def db_is_task_completed(uuid: str):
    with Session(engine) as session:
        query = select(CrawlTask).where(CrawlTask.uuid == uuid)
        crawl_task = session.scalars(query).one()
        crawl_state = crawl_task.completed

        return crawl_state


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
    with Session(engine) as session:
        query = select(CrawlTask).where(CrawlTask.uuid == uuid)
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
    with Session(engine) as session:
        query = (
            select(EmbeddingProgression)
            .where(EmbeddingProgression.crawl_uuid == uuid)
            .where(EmbeddingProgression.embedder_name == model_name)
        )

        embedding_progression = session.scalars(query).one_or_none()

        # no prior progression records found, add them
        if embedding_progression is None:
            session.execute(
                insert(EmbeddingProgression).values(
                    uuid=utils.gen_uuid(),
                    crawl_uuid=uuid,
                    embedder_name=model_name,
                    embedding_amount=1,
                    timestamp=utils.gen_unix_time(),
                )
            )

            session.commit()
            return

        current_count = embedding_progression.embedding_amount
        new_count = current_count + 1

        session.execute(
            update(EmbeddingProgression)
            .where(EmbeddingProgression.crawl_uuid == uuid)
            .where(EmbeddingProgression.embedder_name == model_name)
            .values(embedding_amount=new_count)
        )

        session.commit()
