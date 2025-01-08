from fastapi import APIRouter, Header, Request
from pydantic import BaseModel

# 定义请求体的模型
class HelloRequest(BaseModel):
    test: str

router = APIRouter()

@router.get("/hello", tags=["base"])
async def hello_get(test: str | None = Header(default=None)):
    if test == "get":
        return {"message": "hello, got your get request"}
    return {"message": "hello, got your request"}

@router.post("/hello", tags=["base"])
async def hello_post(request: HelloRequest):
    if request.test == "post":
        return {"message": "hello, got your post request"}
    return {"message": "invalid request"}

@router.get("/echo", tags=["base"])
async def echo_get(request: Request):
    # 获取所有查询参数
    params = dict(request.query_params)
    # 获取所有请求头
    headers = dict(request.headers)
    
    return {
        "query_params": params,
        "headers": headers,
        "method": request.method,
        "url": str(request.url)
    }

@router.post("/echo", tags=["base"])
async def echo_post(request: Request):
    # 获取所有查询参数
    params = dict(request.query_params)
    # 获取所有请求头
    headers = dict(request.headers)
    # 获取请求体
    body = await request.json()
    
    return {
        "query_params": params,
        "headers": headers,
        "body": body,
        "method": request.method,
        "url": str(request.url)
    }