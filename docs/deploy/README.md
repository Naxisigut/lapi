# 部署文档

本文档记录了与系统部署相关的对话和说明。

## 初始环境

项目使用 Pipenv 管理依赖，初始依赖包括：

- fastapi
- uvicorn 
- pydantic
- pydantic-settings

## Docker部署方案

### 1. 准备Docker环境

1. 在服务器上安装Docker

```bash
sudo apt update
sudo apt install docker.io
sudo systemctl start docker
sudo systemctl enable docker
```

### 2. 创建Dockerfile

在项目根目录创建 `Dockerfile`:

```dockerfile:lapi/Dockerfile
FROM python:3.8-slim

WORKDIR /app

RUN pip install pipenv

COPY Pipfile Pipfile.lock ./
RUN pipenv install --system --deploy

COPY ./app ./app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 3. 构建和运行Docker容器

#### 本地操作

1. 在本地构建Docker镜像

```bash
# 在lapi目录下执行
sudo docker build -t fastapi-app .
```

2. 给镜像打标签（替换 your-dockerhub-username 为您的Docker Hub用户名）

```bash
docker tag fastapi-app your-dockerhub-username/fastapi-app:latest
```

3. 登录Docker Hub

```bash
docker login
```

4. 推送镜像到Docker Hub

```bash
docker push your-dockerhub-username/fastapi-app:latest
```

#### 服务器操作

1. 在服务器上安装Docker（如果还没安装）

```bash
sudo apt update
sudo apt install docker.io
sudo systemctl start docker
sudo systemctl enable docker
```

2. 拉取镜像

```bash
sudo docker pull your-dockerhub-username/fastapi-app:latest
```

3. 运行容器

```bash
sudo docker run -d --name fastapi-container -p 8000:8000 your-dockerhub-username/fastapi-app:latest
```

### 4. 访问应用

现在可以通过以下地址访问您的应用：

```
http://your_server_ip:8000
```

### 5. 常用Docker命令

```bash
# 查看运行中的容器
sudo docker ps

# 查看容器日志
sudo docker logs fastapi-container

# 停止容器
sudo docker stop fastapi-container

# 启动容器
sudo docker start fastapi-container

# 重启容器
sudo docker restart fastapi-container
```

## 注意事项

- 部署前请确保服务器有足够的权限和资源
- 建议在生产环境中使用 HTTPS
- 记得定期备份数据和更新系统
- 以上步骤可能需要根据具体的云服务器环境做适当调整
- 确保服务器的8000端口已开放
- 如果后续需要配置域名和HTTPS，建议添加Nginx作为反向代理

## 对话记录

1. 用户询问如何将项目部署到云服务器
2. 提供了完整的部署步骤说明，包括环境准备、项目部署、服务配置等内容
3. 用户表示希望使用Docker进行简单部署，更新了Docker部署方案