from fastapi import APIRouter
from core.databases.db_url_pool import db_add_url, db_get_not_downloaded, db_get_not_embedded, db_is_url_present, db_set_url_downloaded, db_set_url_embedded, db_set_url_rubbish
from webui.models.url_pool import UrlCreator, Downloaded, Embedded
from typing import Union

router = APIRouter()

@router.post('/url')
def add_url(url: UrlCreator):
    result = db_add_url(url.url, url.prompt, url.parent_uuid)
    return {
        "url_object": result
    }

@router.get('/url/downloaded')
def get_not_downloaded():
    result = db_get_not_downloaded()
    return {
        "result": result
    }

@router.get('/url/embedded')
def get_not_embedded(
    model: Union[str, None] = None
):
    result = db_get_not_embedded(model)
    return {
        "result": result
    }
        
    
@router.get('/url/present')
def get_present_urls(
    url: Union[str, None] = None
):
    result = db_is_url_present(url)
    return {
        "url": result
    }

@router.put('/url/embedded')
def set_embedded_url(body: Embedded):
    db_set_url_embedded(body.url_id, body.embeddeding_model)

@router.put('/url/downloaded')
def set_downloaded_url(body: Downloaded):
    db_set_url_downloaded(body.url_id, body.text)

@router.put('/url/rubbish/{url_id}')
def set_url_rubbish(url_id: str):
    db_set_url_rubbish(url_id)

#TODO: fix the type error with union type 