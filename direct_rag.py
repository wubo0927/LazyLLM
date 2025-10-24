# -*- coding: utf-8 -*-
import os
import lazyllm
import PyPDF2
import json
from lazyllm import ReactAgent, fc_register, LOG, OnlineChatModule

# 配置API密钥
lazyllm.config.impl['qwen_api_key'] = os.environ.get('QWEN_API_KEY')

# 存储所有文档内容
DOCUMENTS = {}

def extract_text_from_pdf(pdf_path):
    """从PDF文件中提取文本"""
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text
    except Exception as e:
        print(f"Error reading PDF {pdf_path}: {str(e)}")
        return ""

def load_all_documents():
    """自动加载docs文件夹中的所有PDF文档"""
    docs_path = os.path.join(os.path.dirname(__file__), "docs")
    
    if not os.path.exists(docs_path):
        print(f"文档文件夹不存在: {docs_path}")
        return
    
    # 自动扫描docs文件夹中的所有PDF文件
    pdf_files = [f for f in os.listdir(docs_path) if f.lower().endswith('.pdf')]
    
    if not pdf_files:
        print("docs文件夹中没有找到PDF文件")
        return
    
    print(f"发现 {len(pdf_files)} 个PDF文件:")
    
    for pdf_file in pdf_files:
        pdf_path = os.path.join(docs_path, pdf_file)
        try:
            content = extract_text_from_pdf(pdf_path)
            if content.strip():  # 只加载有内容的文件
                DOCUMENTS[pdf_file] = content
                print(f"[OK] 已加载: {pdf_file} ({len(content)} 字符)")
            else:
                print(f"[SKIP] 跳过空文件: {pdf_file}")
        except Exception as e:
            print(f"[ERROR] 加载失败: {pdf_file} - {str(e)}")
    
    print(f"\n成功加载 {len(DOCUMENTS)} 个文档")

@fc_register("tool")
def search_student_info(query: str):
    """
    搜索学生相关信息
    
    Args:
        query (str): 搜索查询
    """
    try:
        results = []
        query_lower = query.lower()
        
        for filename, content in DOCUMENTS.items():
            if query_lower in content.lower():
                # 找到包含查询内容的段落
                paragraphs = content.split('\n\n')
                for para in paragraphs:
                    if query_lower in para.lower() and para.strip():
                        results.append({
                            "document": filename,
                            "content": para.strip()[:500]  # 限制长度
                        })
        
        if results:
            return json.dumps(results, ensure_ascii=False)
        else:
            return f"在文档中没有找到与 '{query}' 相关的信息。"
            
    except Exception as e:
        return f"搜索时出现错误：{str(e)}"

@fc_register("tool")
def get_frontend_experience():
    """
    获取前端开发经验信息
    
    Returns:
        str: 前端经验信息
    """
    try:
        frontend_keywords = ["前端", "frontend", "react", "vue", "javascript", "html", "css", "web", "网页", "界面"]
        results = []
        
        for filename, content in DOCUMENTS.items():
            for keyword in frontend_keywords:
                if keyword.lower() in content.lower():
                    # 找到包含前端关键词的段落
                    paragraphs = content.split('\n\n')
                    for para in paragraphs:
                        if keyword.lower() in para.lower() and para.strip():
                            results.append({
                                "document": filename,
                                "content": para.strip()[:500]
                            })
                            break
        
        if results:
            return json.dumps(results, ensure_ascii=False)
        else:
            return "没有找到前端开发相关的经验信息。"
            
    except Exception as e:
        return f"获取前端经验时出现错误：{str(e)}"

@fc_register("tool")
def get_gpa_info():
    """
    获取GPA相关信息
    
    Returns:
        str: GPA信息
    """
    try:
        gpa_keywords = ["gpa", "成绩", "绩点", "平均分", "学分"]
        results = []
        
        for filename, content in DOCUMENTS.items():
            for keyword in gpa_keywords:
                if keyword.lower() in content.lower():
                    paragraphs = content.split('\n\n')
                    for para in paragraphs:
                        if keyword.lower() in para.lower() and para.strip():
                            results.append({
                                "document": filename,
                                "content": para.strip()[:500]
                            })
                            break
        
        if results:
            return json.dumps(results, ensure_ascii=False)
        else:
            return "没有找到GPA相关信息。"
            
    except Exception as e:
        return f"获取GPA信息时出现错误：{str(e)}"

# 加载所有文档
print("正在加载PDF文档...")
load_all_documents()

# 创建智能助手
agent = ReactAgent(
    llm=OnlineChatModule(stream=False),
    tools=['search_student_info', 'get_frontend_experience', 'get_gpa_info'],
    prompt="""你是一个智能文档分析助手，能够基于提供的文档内容回答关于学生信息的问题。
请根据用户的问题，调用相应的工具搜索文档信息，并基于找到的信息给出准确、详细的回答。
重点关注学生的技能、经验、GPA等信息。""",
    stream=False
)

# 测试问题
questions = [
    "如果想选用一名同学负责前端，谁可能比较有经验?",
    "李晨是一个怎样的同学?", 
    "张伟的GPA是不是最高的?"
]

print("\n=== 基于PDF文档的RAG问答系统 ===")
print("已加载的文档数量:", len(DOCUMENTS))

for i, question in enumerate(questions, 1):
    print(f"\n问题 {i}: {question}")
    print("-" * 60)
    
    try:
        # 为每个问题创建新的agent实例，避免会话状态污染
        fresh_agent = ReactAgent(
            llm=OnlineChatModule(stream=False),
            tools=['search_student_info', 'get_frontend_experience', 'get_gpa_info'],
            prompt="""你是一个智能文档分析助手，能够基于提供的文档内容回答关于学生信息的问题。
请根据用户的问题，调用相应的工具搜索文档信息，并基于找到的信息给出准确、详细的回答。
重点关注学生的技能、经验、GPA等信息。""",
            stream=False
        )
        
        response = fresh_agent.forward(question)
        print(f"回答: {response}")
    except Exception as e:
        print(f"处理问题时出现错误: {e}")
    
    print("-" * 60)

print("\n=== 问答完成 ===")
