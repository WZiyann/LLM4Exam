from docx import Document
from docx.shared import Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.oxml.ns import qn
import os
import uuid

def generate_word_doc(questions_str, subject):
    # 创建临时文件夹
    if not os.path.exists("./tmp"):
        os.makedirs("./tmp")
    
    doc = Document()
    
    # ==================== 设置全局样式 ====================
    # 设置正文字体（中文字体用宋体，西文Times New Roman）
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Times New Roman'
    normal_style._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')
    normal_style.font.size = Pt(12)  # 小四号字
    
    # ==================== 设置试卷标题 ====================
    title = doc.add_heading(level=0)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title_run = title.add_run(f"{subject}考试试卷")
    title_run.font.name = '黑体'
    title_run._element.rPr.rFonts.set(qn('w:eastAsia'), '黑体')
    title_run.font.size = Pt(22)  # 一号字
    title_run.bold = True
    
    # 添加考试信息行
    info = doc.add_paragraph()
    info.alignment = WD_ALIGN_PARAGRAPH.CENTER
    info_run = info.add_run("考试时间：120分钟　　满分：100分")
    info_run.font.name = '楷体'
    info_run._element.rPr.rFonts.set(qn('w:eastAsia'), '楷体')
    info_run.font.size = Pt(14)
    
    # ==================== 设置页面布局 ====================
    section = doc.sections[0]
    section.top_margin = Cm(2.5)     # 上边距
    section.bottom_margin = Cm(2.5)  # 下边距
    section.left_margin = Cm(3)      # 左边距
    section.right_margin = Cm(3)     # 右边距
    
    # ==================== 添加试题内容 ====================
    lines = questions_str.strip().split("\n")
    current_question = ""
    
    for line in lines:
        line = line.strip()
        if not line:  # 跳过空行
            continue
            
        # 合并连续的问题行（选项和答案）
        if line.startswith(("A.", "B.", "C.", "D.", "答案：")):
            current_question += "\n" + line
        else:
            # 处理前一个问题（如果有）
            if current_question:
                p = doc.add_paragraph()
                p_format = p.paragraph_format
                p_format.space_before = Pt(0)
                p_format.space_after = Pt(0)
                p_format.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
                # p_format.first_line_indent = Cm(0.74)  # 首行缩进2字符
                
                run = p.add_run(current_question)
                run.font.name = 'Times New Roman'
                run._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')
            
            # 开始新问题
            current_question = line
    
    # 处理最后一个问题
    if current_question:
        p = doc.add_paragraph()
        p_format = p.paragraph_format
        p_format.space_before = Pt(0)
        p_format.space_after = Pt(0)
        p_format.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
        # p_format.first_line_indent = Cm(0.74)  # 首行缩进2字符
        
        run = p.add_run(current_question)
        run.font.name = 'Times New Roman'
        run._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')
        
        # 特殊格式处理（题型标题）
        if current_question.startswith(('一、', '二、', '三、', '四、')):
            run.bold = True
            run.font.size = Pt(14)
            p_format.space_before = Pt(12)
            p_format.space_after = Pt(6)
            p_format.first_line_indent = Cm(0)  # 取消首行缩进

    # ==================== 保存文件 ====================
    filename = f"./tmp/{uuid.uuid4()}.docx"
    doc.save(filename)
    return filename