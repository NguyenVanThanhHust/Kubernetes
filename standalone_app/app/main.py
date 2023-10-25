from typing import Union

from fastapi import FastAPI

app = FastAPI()


@app.route('/health')
def health_check():
    return 'OK', 200


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
