#!/bin/bash


service_name=selenium
image=registry.cn-hangzhou.aliyuncs.com/miku/selenium
tag=py38_01



docker stop ${service_name}
docker rm ${service_name}

docker run  -it  --name=${service_name} \
    -w /app \
    -v $(pwd):/app \
    ${image}:${tag} \
      python main.py
