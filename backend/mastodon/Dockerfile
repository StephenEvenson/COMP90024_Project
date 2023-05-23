FROM python:3.10
# 设置工作目录
WORKDIR /data/app
# 复制本地依赖, 每个COPY会新建一个镜像层
COPY . .

# 设置环境变量
# 不要生成pyc文件
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 安装依赖, 由于aioredis依赖的hiredis以及cryptography需要编译, 所以这里需要add这些包, 这样依赖，容器就会变得很大...
RUN apt-get -y install gcc libffi-dev && pip install --upgrade pip && pip install -r requirements.txt

# 指明监听的端口
EXPOSE 8080

# 运行的命令
CMD ["python", "mastodon_harvester.py"]