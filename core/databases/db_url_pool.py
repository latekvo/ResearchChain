from sqlalchemy import (
    String,
    Boolean,
    Integer,
    select,
    update,
    ForeignKey,
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
    url: Mapped[str] = mapped_column(String())
    text: Mapped[str] = mapped_column(String())

    # tracking data
    parent_uuid: Mapped[str] = mapped_column(String())
    task_uuid: Mapped[str] = mapped_column(String())
    prompt: Mapped[str] = mapped_column(String())

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
    session = Session(engine)

    query = select(UrlObject).where(
        UrlObject.is_downloaded.is_(False) and UrlObject.is_rubbish.is_(False)
    )

    results = list(session.scalars(query).all())

    return results


def db_get_not_embedded(model: str, amount: int = 100) -> list[UrlObject]:
    session = Session(engine)

    exclusion_query = select(UrlObject).where(
        UrlEmbedding.document_uuid.is_(UrlObject.uuid)
        and UrlEmbedding.embedder_name.is_(model)
    )

    query = select(UrlObject).where(
        UrlObject.is_downloaded.is_(True) and UrlObject.is_rubbish.is_(False)
    )

    # todo: this particular function requires rigorous testing,
    #       as this is not common usage
    query.except_(exclusion_query)

    results = list(session.scalars(query).all())

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
    session = Session(engine)

    session.execute(
        update(UrlObject)
        .where(UrlObject.uuid.is_(url_id))
        .values(is_downloaded=True, text=text)
    )

    session.commit()


def db_set_url_rubbish(url_id: str):
    session = Session(engine)

    session.execute(
        update(UrlObject).where(UrlObject.uuid.is_(url_id)).values(is_rubbish=True)
    )

    session.commit()


def db_is_url_present(url: str):
    session = Session(engine)

    query = select(UrlObject).where(UrlObject.url.is_(url))
    result = session.scalar(query)

    if result is None:
        return False

    return True
