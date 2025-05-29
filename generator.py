from openai import OpenAI

client = OpenAI(
    api_key = "sk-69e3413c29e9425a92c405f15046d3b0",
    # base_url = "http://192.168.4.228:23333/v1"
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

def generate_questions(prompt, context_list, count):
    print("==========开始生成试题========")
    print(f"========Prompt: {prompt}")
    context = "\n".join(context_list)
    print(f"========Context: {context}")
    full_prompt = f"""你是一名老师。根据以下参考题库与提示，生成 {count} 道试题。

要求：
1. 严格按照给定的题型要求
2. 题目难度适中
3. 知识点分布合理

提示: {prompt}
参考题库:
{context}

输出格式：
1. 每道题目单独一行
2. 选择题需要包含选项（A、B、C、D）
3. 最后一行标注"答案："并给出正确答案
"""
    print(f"========Full Prompt: {full_prompt}")
    response = client.chat.completions.create(
        model="qwen-turbo",
        messages=[{"role": "user", "content": full_prompt}],
        temperature=0.7
    )
    print("==========试题生成完成========", response.choices[0].message.content)
    return response.choices[0].message.content

# 测试用例
if __name__ == "__main__":
    prompt = "请生成一道关于机器学习的选择题，包含四个选项和正确答案。"
    context_list = [
        "机器学习是人工智能的一个分支，它使计算机能够从数据中学习和改进。",
        "监督学习和无监督学习是机器学习的两种主要类型。",
        "常见的机器学习算法包括线性回归、决策树和支持向量机。"
    ]
    count = 1
    
    questions = generate_questions(prompt, context_list, count)
    print(questions)
