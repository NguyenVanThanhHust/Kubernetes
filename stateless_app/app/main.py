import os, sys
from typing import Union

from fastapi import FastAPI

from celery import Task, shared_task
from celery.result import AsyncResult
from celery_task_queue import celery_app

from loguru import logger
from ai_model import build_fake_ai_model

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.post("/process/{some_string}")
def process_smt(some_string: str):
    return {"processed_string": some_string + "_processed"}


class PredictorTask(Task):
    abstract= True
    def __init__(self, ):
        self.ai_model = build_fake_ai_model()
        
    def __call__(self, *args, **kwargs):
        if not self.ai_model:
            self.ai_model = build_fake_ai_model()
        return self.run(*args, **kwargs)
    
@celery_app.task(
    ignore_result=False,
    bind=True,
    base=PredictorTask,
)
def predict_single_string(self, input_string):
    """
    Essentially the run method of PredictTask
    """
    result  = self.ai_model.forward(input_string)
    return result

@app.post("/celery_post/{some_string}")
def push_to_queue(some_string):
    task_id = predict_single_string(some_string)
    return task_id

def get_task_result(task_id:str):
    """Fetch result for given task_id"""
    task = AsyncResult(task_id)
    if not task.ready():
        logger.info("Result is not ready for {}".format(task_id))
        return False, None
    logger.info("getting results")
    result = task.get()
    return True, result
