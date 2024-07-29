import asyncio
from decimal import Decimal
import os
import threading
import time
from fastapi import FastAPI, BackgroundTasks, Query, Body, Request, Response, Depends
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field, validator
from typing import List, Union, Optional, Tuple
from fastapi.openapi.utils import get_openapi
from fastapi.exceptions import HTTPException

# app对象
app = FastAPI(docs_url=None, redoc_url=None, title="test",
    description="shunyu test",
    version="3.0.1",)
    
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Custom API",
        version="3.0.1",
        description="This is a very custom OpenAPI schema",
        routes=app.routes,
    )
    # Here we override the OpenAPI version
    openapi_schema["openapi"] = "3.1.0"
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi


# 静态文件位置
static__dir = os.path.dirname(os.path.abspath(__file__))
app.mount("/static_", StaticFiles(directory=f"{static__dir}/static_"), name="static_")


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="/static_/swagger-ui/swagger-ui-bundle.js",
        swagger_css_url="/static_/swagger-ui/swagger-ui.css",
    )


@app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
async def swagger_ui_redirect():
    return get_swagger_ui_oauth2_redirect_html()


@app.get("/redoc", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title=app.title + " - ReDoc",
        redoc_js_url="/static_/redoc/bundles/redoc.standalone.js",
    )


# class Item(BaseModel):
#     name: str
#     description: Union[str, None] = None
#     price: float
#     tax: Union[float, None] = None
#     tags: List[str]
    
# class Item2(BaseModel):
#     name: Optional[str]
#     description: Optional[str] = None
#     price: float = Field(Ellipsis, 
#                          title='这是price的title', 
#                          description='这是price的描述')
#     tax: float = None
#     xxx: int
    
#     @validator('xxx')
#     def validator_xxx(cls, xxx):
#         if 0 < xxx < 6:
#             raise ValueError('error xxx')
#         return xxx

# @app.get("/")
# def read_root(item: Union[Item, Item2]):
#     print(item)
#     return {'name':item.name}

# @app.get("/1")
# def read_root_1(item: Item=Depends()):
#     print(item)
#     return {'name':item.name}

# @app.get("/items/{item_id}", response_model=Item)
# def read_item(item_id: int, q: str = None):
#     """
#     Get a single item by ID
#     """
#     return {"item_id": item_id, "q": q}

# @app.post("/items/", response_model=Item)
# def create_item(item: Item) -> Item:
#     """
#     Create an item with all the information:
#     - **name**: each item must have a name
#     - **description**: a long description
#     - **price**: required
#     - **tax**: if the item doesn't have tax, you can omit this
#     - **tags**: a set of unique tag strings for this item
#     """
#     return item

# @app.post('/background_task')
# async def background_task(tasks:BackgroundTasks) -> dict:
#     return dict()

# @app.get('/test_http_exception')
# async def test_http_exception(
#     test:str = Query('admin', 
#                                   alias='test_1',
#                                   title='这是一个title',
#                                   description='这是一个描述',
#                                   max_length=10)) -> Response:
#     return Response(test, 404, {'test': 'asdasdasd'})

# def username_check(username:str=Query(...)):
#     if username != 'zhong':
#         raise HTTPException(status_code=403, detail="用户名错误！没有权限访问！")
#     return username

# def age_check(username:str=Depends(username_check),age:int=Query(...)):
#     if age <18:
#         raise HTTPException(status_code=403, detail="用户名未满18岁!禁止吸烟！")
#     return username,age


# @app.get("/user/login/")
# def user_login(username_and_age: Tuple = Depends(age_check)):
#     return {
#         'username': username_and_age[0],
#         'age': username_and_age[1],
#     }


# @app.get("/user/info")
# def user_info(username_and_age: Tuple = Depends(age_check, use_cache=False)):
#     return {
#         'username':username_and_age[0],
#         'age': username_and_age[1],
#     }

# @app.get('/test_async_time')
# async def test_async_time():
#     await asyncio.sleep(10)
#     return [time.time(), threading.current_thread().ident]
# from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer
from typing_extensions import Annotated

# app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class User(BaseModel):
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None


def fake_decode_token(token):
    return User(
        username=token + "fakedecoded", email="john@example.com", full_name="John Doe"
    )


async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = fake_decode_token(token)
    return user


@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

if __name__ == '__main__':
    import uvicorn
    uvicorn.run('test:app', host="0.0.0.0", port=8000, reload=True)