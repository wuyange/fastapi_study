import asyncio
from datetime import datetime, timedelta, timezone
from decimal import Decimal
import os
import threading
import time
from jwt import InvalidTokenError
import jwt
from typing_extensions import Annotated
from passlib.context import CryptContext
from fastapi import FastAPI, BackgroundTasks, Query, Body, Request, Response, Depends, status
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
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
static_dir = os.path.dirname(os.path.abspath(__file__))
app.mount("/static", StaticFiles(directory=f"{static_dir}/static"), name="static")


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="/static/swagger-ui/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger-ui/swagger-ui.css",
    )


@app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
async def swagger_ui_redirect():
    return get_swagger_ui_oauth2_redirect_html()


@app.get("/redoc", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title=app.title + " - ReDoc",
        redoc_js_url="/static/redoc/bundles/redoc.standalone.js",
    )


class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None
    tags: List[str]
    
class Item2(BaseModel):
    name: Optional[str]
    description: Optional[str] = None
    price: float = Field(Ellipsis, 
                         title='这是price的title', 
                         description='这是price的描述')
    tax: float = None
    xxx: int
    
    @validator('xxx')
    def validator_xxx(cls, xxx):
        if 0 < xxx < 6:
            raise ValueError('error xxx')
        return xxx

@app.get("/")
def read_root(item: Union[Item, Item2]):
    print(item)
    return {'name':item.name}

@app.get("/1")
def read_root_1(item: Item=Depends()):
    print(item)
    return {'name':item.name}

@app.get("/items/{item_id}", response_model=Item)
def read_item(item_id: int, q: str = None):
    """
    Get a single item by ID
    """
    return {"item_id": item_id, "q": q}

@app.post("/items/", response_model=Item)
def create_item(item: Item) -> Item:
    """
    Create an item with all the information:
    - **name**: each item must have a name
    - **description**: a long description
    - **price**: required
    - **tax**: if the item doesn't have tax, you can omit this
    - **tags**: a set of unique tag strings for this item
    """
    return item

@app.post('/background_task')
async def background_task(tasks:BackgroundTasks) -> dict:
    return dict()

@app.get('/test_http_exception')
async def test_http_exception(
    test:str = Query('admin', 
                                  alias='test_1',
                                  title='这是一个title',
                                  description='这是一个描述',
                                  max_length=10)) -> Response:
    return Response(test, 404, {'test': 'asdasdasd'})

def username_check(username:str=Query(...)):
    if username != 'zhong':
        raise HTTPException(status_code=403, detail="用户名错误！没有权限访问！")
    return username

def age_check(username:str=Depends(username_check),age:int=Query(...)):
    if age <18:
        raise HTTPException(status_code=403, detail="用户名未满18岁!禁止吸烟！")
    return username,age


@app.get("/user/login/")
def user_login(username_and_age: Tuple = Depends(age_check)):
    return {
        'username': username_and_age[0],
        'age': username_and_age[1],
    }


@app.get("/user/info")
def user_info(username_and_age: Tuple = Depends(age_check, use_cache=False)):
    return {
        'username':username_and_age[0],
        'age': username_and_age[1],
    }

@app.get('/test_async_time')
async def test_async_time():
    await asyncio.sleep(10)
    return [time.time(), threading.current_thread().ident]


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    }
}


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None


class User(BaseModel):
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None


class UserInDB(User):
    hashed_password: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@app.get("/users/me/", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user


@app.get("/users/me/items/")
async def read_own_items(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return [{"item_id": "Foo", "owner": current_user.username}]

if __name__ == '__main__':
    import uvicorn
    # uvicorn.run('main:app', host="0.0.0.0", port=8000, reload=True)
    uvicorn.run('main:app', host="0.0.0.0", port=8000, reload=True)
