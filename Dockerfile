FROM python:3.8-slim

WORKDIR /app

RUN pip install pipenv

COPY Pipfile Pipfile.lock ./

# 确保安装所有必要的依赖
RUN pipenv install --system --deploy
RUN pip install uvicorn[standard] anyio

COPY ./app ./app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"] 