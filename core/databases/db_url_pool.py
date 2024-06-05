from sqlalchemy import (
    String,
    Boolean,
    Integer,
    create_engine,
    select,
    update,
    ForeignKey,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session, relationship

from core.tools import utils

engine = create_engine("sqlite://", echo=True)


class UrlEmbedding(DeclarativeBase):
    __tablename__ = "url_embeddings"

    uuid: Mapped[str] = mapped_column(primary_key=True)

    document_uuid: Mapped[str] = mapped_column(ForeignKey("url_pool.uuid"))

    embedder_name: Mapped[str] = mapped_column(String())
    timestamp: Mapped[int] = mapped_column(Integer())  # time added UNIX SECONDS


class UrlObject(DeclarativeBase):
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

    # todo: using this type of list may cause issues, test this!
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


def db_get_not_embedded(model: str) -> list[UrlObject]:
    session = Session(engine)

    # fixme: this requires embedded_by to be a relation, not a list

    # query = select(UrlObject).where(UrlObject.embedded_by.has())
    # results = list(session.scalars(query).all())

    return []


def db_set_url_embedded(url_id: str, embedding_model: str):
    session = Session(engine)

    query = select(UrlObject).where(UrlObject.uuid.is_(url_id))
    result = session.scalar(query)

    embedded_by = result.embedded_by
    embedded_by.append(embedding_model)

    # fixme: embedded_by...
    # db.update({"embedded_by": embedded_by}, query.uuid == url_id)


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
