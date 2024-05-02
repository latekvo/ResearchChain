from fastapi import FastAPI
from webui.router import completion_routes, crawl_routes, url_routes

app = FastAPI()

app.include_router(completion_routes.router)
app.include_router(crawl_routes.router)
app.include_router(url_routes.router)
