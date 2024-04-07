# this file provides a simple internal API for UIs to interact with the entire system
from core.tools import utils


def add_crawl_task():
    task_uuid = utils.gen_uuid()
    return task_uuid


def add_summarize_task():
    task_uuid = utils.gen_uuid()
    return task_uuid


def get_crawls(page=0, results_per_page=20):
    return []


def get_summaries(page=0, results_per_page=20):
    return []
