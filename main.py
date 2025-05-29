from fastapi import FastAPI, UploadFile, File, Form, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from rag import search_similar_questions
from generator import generate_questions
from docgen import generate_word_doc
import uuid, os
from typing import List
app = FastAPI()

# 允许本地静态页面跨域访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 或指定你的前端地址
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 定义请求体的数据模型
class QuestionTypeItem(BaseModel):
    type: str
    count: int

class GenerationRequest(BaseModel):
    subject: str
    grade: str
    question_types: List[QuestionTypeItem]  # 题目类型列表
    prompt: str

# 生成试卷接口
@app.post("/generate")
def generate_exam(request: GenerationRequest):
    print(f"-----Received request: {request}----------")
    all_questions = ""
    # 遍历所有题目类型
    for item in request.question_types:
        # 检索相似问题作为上下文
        context = search_similar_questions(request.prompt)
        # 基于上下文和提示生成题目
        generated = generate_questions(
            f"{request.prompt}。请注意！！！生成的题型是：{item.type}", 
            context, 
            item.count
        )
        all_questions += f"[{item.type}]\n{generated}\n\n"

    print(f"all_questions：\n{all_questions}")
    # 生成Word文档并返回文件路径
    doc_path = generate_word_doc(all_questions, request.subject)
    print(f"生成的Word文档路径：{doc_path}")
    return {"file": doc_path}

# 文件下载接口
@app.get("/download")
def download_file(path: str = Query(..., description="Word文档路径")):
    # 返回Word文档文件
    return FileResponse(
        path,
        media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        filename=os.path.basename(path)
    )

app.mount("/", StaticFiles(directory="static", html=True), name="static")