# 在服务器上构建项目

本文档记录了如何在服务器上构建项目的步骤。

## 1. 准备工作

### 1.1 检查服务器环境

首先检查服务器是否安装了 Git：

```bash
git --version
```

如果没有安装 Git，在 Debian 系统上安装：

```bash
sudo apt update # 更新包索引
sudo apt install git -y # 安装 git, -y 表示自动确认
```

### 1.2 创建项目目录

创建并进入项目目录：

```bash
mkdir -p /home/projects # 创建项目目录
cd /home/projects # 进入目录
```

如果遇到权限问题，需要修改目录权限：

```bash
sudo chown -R $USER:$USER /home/projects
```

## 2. 获取代码

有多种方式可以将代码传输到服务器：

### 2.1 使用 Git（推荐）

如果代码在 Git 仓库中：

```bash
git clone <repository_url>
```

### 2.2 使用 SFTP 工具（如 XFTP）

1. 准备信息：
   - 服务器 IP 地址
   - 用户名（默认 root）
   - 密码
   - 端口号（默认 22）

2. XFTP 连接步骤：
   - 打开 XFTP，点击"新建连接"
   - 填写服务器信息（主机、用户名、密码等）
   - 连接成功后，将本地项目文件夹拖拽到服务器端

3. 如果需要重置阿里云服务器密码：
   - 登录阿里云控制台
   - 找到 ECS 实例
   - 选择"更多" -> "密码/密钥" -> "重置密码"
   - 重启实例使新密码生效

### 2.3 其他方法

也可以使用以下命令行工具：

```bash
# 使用 scp
scp -r ./lapi user@your_server_ip:/path/to/destination

# 使用 rsync
rsync -avz ./lapi user@your_server_ip:/path/to/destination
```

## 3. 验证

检查文件是否传输成功：

```bash
ls -l    # 列出目录内容
```

## 4. 构建项目

### 4.1 检查 Docker 环境

查看 Docker 版本，确认是否安装：

```bash
docker --version  # 显示 Docker 版本信息
```

如果未安装 Docker，在 Debian 系统上安装：

```bash
# 更新包索引
sudo apt update

# 安装必要的依赖包
sudo apt install -y apt-transport-https ca-certificates curl software-properties-common

# 添加 Docker 的官方 GPG 密钥
curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# 设置 Docker 稳定版仓库
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/debian $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# 再次更新包索引
sudo apt update

# 安装 Docker
sudo apt install -y docker-ce docker-ce-cli containerd.io
```

### 4.2 查看项目文件

进入项目目录并查看文件：

```bash
cd lapi                # 进入项目目录
ls -l                  # 列出目录内容，-l 表示显示详细信息
cat Dockerfile         # 查看 Dockerfile 内容，cat 命令用于显示文件内容
```
### 4.3 构建 Docker 镜像

查看 Dockerfile 内容：
```bash
cat Dockerfile         # 查看 Dockerfile 内容
```

Dockerfile 内容如下：
```dockerfile
FROM python:3.8-slim

WORKDIR /app

RUN pip install pipenv

COPY Pipfile Pipfile.lock ./
RUN pipenv install --system --deploy

COPY ./app ./app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

开始构建镜像：

```bash
# 构建 Docker 镜像
docker build -t lapi .  # -t 参数用于指定镜像名称，. 表示使用当前目录的 Dockerfile

# 检查镜像是否构建成功
docker images          # 列出所有镜像

# 运行容器
docker run -d -p 8000:8000 lapi  # -d 表示在后台运行，-p 表示端口映射

# 检查容器是否正在运行
docker ps             # 列出正在运行的容器
```

### 4.4 验证部署

检查服务是否正常运行：

```bash
docker ps -a    # -a 参数显示所有容器，包括未运行的

# 查看容器日志
docker logs $(docker ps -q -f name=lapi)  # 显示容器的日志输出

# 测试 API 是否可访问
curl http://localhost:8000/  # 测试 API 访问
```
## 注意事项

1. 确保有足够的磁盘空间
2. 确保有适当的文件权限
3. 如果使用 Git，确保有访问仓库的权限
4. 建议在操作前备份重要数据