FROM python:3.8-alpine3.10

# update apk repo
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.tuna.tsinghua.edu.cn/g' /etc/apk/repositories

# install chromedriver
RUN apk update
RUN apk add chromium chromium-chromedriver
# update time zone
RUN apk add -U tzdata && cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && apk del tzdata

# upgrade pip
RUN pip install -i https://mirrors.aliyun.com/pypi/simple/  --upgrade pip

# install selenium
RUN pip install -i https://mirrors.aliyun.com/pypi/simple/  selenium html5lib


WORKDIR /app

COPY requirements.txt .

RUN pip install -i https://mirrors.aliyun.com/pypi/simple/ -r requirements.txt
