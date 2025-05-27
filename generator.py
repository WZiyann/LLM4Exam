import openai
openai.api_key = "sk-ez96H15flvs8eOjyCWbhnrbqZvHohTiNN93AudDrR3kMHcWD"
openai.api_base = "https://api.key77qiqi.cn/v1"  

def generate_questions(prompt, context_list, count):
    context = "\n".join(context_list)
    full_prompt = f"""你是一名老师。根据以下参考题库与提示，生成 {count} 道符合要求的试题。

提示: {prompt}
参考题库:
{context}

请输出题目、选项（如有）、标准答案。"""
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": full_prompt}],
        temperature=0.7
    )
    return response['choices'][0]['message']['content']