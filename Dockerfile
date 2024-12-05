FROM python:3.8-slim

WORKDIR /app

# 设置 pip 源为国内镜像，并增加超时时间
RUN pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/ \
    && pip config set global.timeout 1000

RUN pip install pipenv

COPY Pipfile Pipfile.lock ./

# 确保安装所有必要的依赖
RUN pipenv install --system --deploy
RUN pip install uvicorn[standard] anyio

COPY ./app ./app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"] 