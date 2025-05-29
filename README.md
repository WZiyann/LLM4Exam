# LLM4Exam
LLM4Exam is a system designed to help users efficiently and conveniently create exam questions.

## Key Features
- Automatically generates exam questions using large language models
- Supports customizable question types and difficulty levels
- Simplifies the test creation process and improves productivity


## Language
Python==3.8

## Environment
```
fastapi>=0.68.0
uvicorn>=0.15.0
python-docx>=0.8.11
sentence-transformers>=0.4.1
faiss-cpu>=1.7.2
openai==1.8.2
pydantic>=1.8.2
python-multipart>=0.0.5
numpy>=1.21.0
```

## Start
```
python main.py
# 首次启动会自动加载paraphrase-multilingual-MiniLM-L12-v2模型，响应较慢
# 访问本地http://127.0.0.1:8000/
```
