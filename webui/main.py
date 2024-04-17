from fastapi import FastAPI
# from router.completion_routes import router as completion_router
from webui.router import completion_routes, crawl_routes, url_routes
# from core.databases.db_url_pool import db_add_url, db_get_not_downloaded, db_get_not_embedded, db_set_url_downloaded, db_set_url_rubbish, db_is_url_present

app = FastAPI()

app.include_router(completion_routes.router)
app.include_router(crawl_routes.router)
app.include_router(url_routes.router)