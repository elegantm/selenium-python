#!/bin/bash

images=registry.cn-hangzhou.aliyuncs.com/miku/selenium
tag=py38_01


docker build -t ${images}:${tag}  -f Dockerfile .

docker push ${images}:${tag}
