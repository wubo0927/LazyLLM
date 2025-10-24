# 基于LazyLLM的智能文档问答系统

## 项目简介

本项目基于LazyLLM框架构建了一个智能文档问答系统，能够自动解析PDF文档并回答相关问题。系统采用RAG（检索增强生成）技术，结合通义千问大语言模型，实现了高效的文档理解和智能问答功能。

### 核心功能
- 🔍 **自动文档解析**：自动扫描并解析docs文件夹中的所有PDF文档
- 🤖 **智能问答**：基于文档内容回答用户问题
- 🛠️ **工具调用**：支持多种搜索工具（学生信息、前端经验、GPA比较等）

## 技术架构

```
项目结构
├── direct_rag.py        # 智能文档问答系统（核心）
├── docs/               # PDF文档存储文件夹
│   ├── *.pdf          # 自动扫描所有PDF文件
├── requirements.txt    # 依赖包列表
└── README.md          # 项目说明文档
```

## 实现步骤

### 1. 环境准备
```bash
# 安装依赖
pip install lazyllm PyPDF2

# 设置环境变量
set QWEN_API_KEY=your-api-key-here
```

### 2. 文档准备
将PDF文档放入`docs`文件夹，系统会自动扫描并加载所有PDF文件。

### 3. 运行系统
```bash
# 运行文档问答系统
python direct_rag.py
```

## 核心代码

### 自动文档加载
```python
def load_all_documents():
    """自动加载docs文件夹中的所有PDF文档"""
    docs_path = os.path.join(os.path.dirname(__file__), "docs")
    
    # 自动扫描docs文件夹中的所有PDF文件
    pdf_files = [f for f in os.listdir(docs_path) if f.lower().endswith('.pdf')]
    
    for pdf_file in pdf_files:
        pdf_path = os.path.join(docs_path, pdf_file)
        content = extract_text_from_pdf(pdf_path)
        DOCUMENTS[pdf_file] = content
```

### RAG问答系统
```python
# 创建智能助手
agent = ReactAgent(
    llm=OnlineChatModule(stream=False),
    tools=['search_student_info', 'get_frontend_experience', 'get_gpa_info'],
    prompt="""你是一个智能文档分析助手...""",
    stream=False
)

# 为每个问题创建独立实例，避免会话状态污染
fresh_agent = ReactAgent(...)
response = fresh_agent.forward(question)
```

## 效果展示

### 文档自动加载
```
发现 7 个PDF文件:
[OK] 已加载: 张伟的个人简历.pdf (2298 字符)
[OK] 已加载: 李晨的个人简历.pdf (2370 字符)
[OK] 已加载: 李晨的技术博客文章.pdf (5345 字符)
...
成功加载 7 个文档
```

### 智能问答效果
```
问题: 如果想选用一名同学负责前端，谁可能比较有经验?

回答: 根据文档信息，**张伟**是最有经验的前端开发选择：

1. **开源项目经验**：
   - 张伟是"FudanUI"前端组件库项目的主要开发者
   - 项目获得超过3000个star，深受开发者喜爱

2. **学术背景**：
   - 复旦大学计算机学院学士，GPA: 3.6/4.0
   - 上海交通大学硕士，研究方向为前端架构优化

3. **工作经验**：
   - 腾讯高级前端工程师
   - 负责电商平台前端架构设计，PV超过800万
```

## 技术亮点

1. **自动文档识别**：无需硬编码文件名，自动扫描docs文件夹
2. **会话状态隔离**：为每个问题创建独立agent实例，避免状态污染
3. **多工具集成**：支持文档搜索、前端经验分析、GPA比较等多种工具
4. **错误处理**：完善的异常处理和用户友好的错误提示

## 部署说明

1. 克隆项目到本地
2. 安装依赖包
3. 设置API密钥环境变量
4. 将PDF文档放入docs文件夹
5. 运行程序

## 许可证

MIT License