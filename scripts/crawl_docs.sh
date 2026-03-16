#!/bin/bash
BASE=docs-corpus
mkdir -p $BASE/{rust,langchain,docker,fastapi}

cd $BASE/rust && wget -r -k -l 2 -p -E -nc -np https://doc.rust-lang.org/book/ &
cd ../langchain && wget -r -k -l 3 -p -E -nc -np https://python.langchain.com/v0.3/docs/ &
cd ../docker && wget -r -k -l 2 -p -E -nc -np https://docs.docker.com/ &
cd ../fastapi && wget -r -k -l 2 -p -E -nc -np https://fastapi.tiangolo.com/ &
wait  # 等所有完成
echo "爬取完成！总文件夹: $BASE"
