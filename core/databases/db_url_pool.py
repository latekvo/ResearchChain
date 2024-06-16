from typing import Optional

from sqlalchemy import (
    String,
    Boolean,
    Integer,
    select,
    update,
    ForeignKey,
    TEXT,
)
from sqlalchemy.orm import Mapped, mapped_column, Session, relationship

from core.databases.db_base import Base, engine
from core.tools import utils


class UrlEmbedding(Base):
    __tablename__ = "url_embeddings"

    uuid: Mapped[str] = mapped_column(primary_key=True)

    document_uuid: Mapped[str] = mapped_column(ForeignKey("url_pool.uuid"))

    embedder_name: Mapped[str] = mapped_column(String())
    timestamp: Mapped[int] = mapped_column(Integer())  # time added UNIX SECONDS


class UrlObject(Base):
    __tablename__ = "url_pool"

    # base data
    uuid: Mapped[str] = mapped_column(primary_key=True)
    url: Mapped[str] = mapped_column(TEXT())
    text: Mapped[str] = mapped_column(TEXT(), nullable=True)

    # tracking data
    parent_uuid: Mapped[Optional["UrlObject"]] = mapped_column(
        ForeignKey("url_pool.uuid"), nullable=True
    )
    task_uuid: Mapped[str] = mapped_column(String(), nullable=True)
    prompt: Mapped[str] = mapped_column(TEXT())

    timestamp: Mapped[int] = mapped_column(Integer())  # time added UNIX SECONDS

    is_downloaded: Mapped[bool] = mapped_column(Boolean())
    is_rubbish: Mapped[bool] = mapped_column(Boolean())

    embedded_by: Mapped[list["UrlEmbedding"]] = relationship()


def db_add_url(url: str, prompt: str, parent_uuid: str = None, task_uuid: str = None):
    new_uuid = utils.gen_uuid()
    timestamp = utils.gen_unix_time()

    with Session(engine) as session:
        completion_task = UrlObject(
            uuid=new_uuid,
            parent_uuid=parent_uuid,
            task_uuid=task_uuid,
            prompt=prompt,
            url=url,
            text=None,
            is_downloaded=False,
            is_rubbish=False,
            embedded_by=[],
            timestamp=timestamp,
        )

        session.add(completion_task)
        session.commit()

    return new_uuid, completion_task


def db_get_not_downloaded() -> list:
    with Session(engine) as session:
        session.expire_on_commit = False

        query = (
            select(UrlObject)
            .where(UrlObject.is_downloaded.is_(False))
            .where(UrlObject.is_rubbish.is_(False))
        )

        results = list(session.scalars(query).all())
        session.expunge_all()

        return results


def db_get_not_embedded(model: str, amount: int = 100) -> list[UrlObject]:
    with Session(engine) as session:
        session.expire_on_commit = False

        exclusion_query = (
            select(UrlObject)
            .where(UrlEmbedding.document_uuid == UrlObject.uuid)
            .where(UrlEmbedding.embedder_name == model)
            .limit(amount)
        )

        query = (
            select(UrlObject)
            .where(UrlObject.is_downloaded.is_(True))
            .where(UrlObject.is_rubbish.is_(False))
        )

        # todo: this particular function requires rigorous testing,
        #       as this is not a well documented use case
        query.except_(exclusion_query)

        results = list(session.scalars(query).all())
        session.expunge_all()

        return results


def db_set_url_embedded(url_id: str, embedding_model: str):
    new_uuid = utils.gen_uuid()
    timestamp = utils.gen_unix_time()

    with Session(engine) as session:
        completion_task = UrlEmbedding(
            uuid=new_uuid,
            document_uuid=url_id,
            embedder_name=embedding_model,
            timestamp=timestamp,
        )

        session.add(completion_task)
        session.commit()

    return True


def db_set_url_downloaded(url_id: str, text: str):
    with Session(engine) as session:
        session.execute(
            update(UrlObject)
            .where(UrlObject.uuid == url_id)
            .values(is_downloaded=True, text=text)
        )

        session.commit()


def db_set_url_rubbish(url_id: str):
    with Session(engine) as session:
        session.execute(
            update(UrlObject).where(UrlObject.uuid == url_id).values(is_rubbish=True)
        )

        session.commit()


def db_is_url_present(url: str):
    with Session(engine) as session:
        query = select(UrlObject).where(UrlObject.url == url)
        result = session.scalar(query)

        if result is None:
            return False

        return True
