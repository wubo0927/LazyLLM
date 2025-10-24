# 基于LazyLLM的智能文档问答系统

## 项目简介

本项目基于LazyLLM框架构建了一个智能文档问答系统，能够自动解析PDF文档并回答相关问题。系统采用RAG（检索增强生成）技术，结合通义千问大语言模型，实现了高效的文档理解和智能问答功能。

### 核心功能
- 🔍 **自动文档解析**：自动扫描并解析docs文件夹中的所有PDF文档
- 🤖 **智能问答**：基于文档内容回答用户问题
- 🛠️ **工具调用**：支持多种搜索工具（学生信息、前端经验、GPA比较等）

## 技术架构

### 核心技术栈
- **LazyLLM**：轻量级大语言模型框架
- **通义千问**：阿里云大语言模型API
- **PyPDF2**：PDF文档解析
- **ReactAgent**：智能代理框架

### 系统架构图
```
┌─────────────────┐    ┌─────────────────┐
│   PDF文档库     │    │   智能问答引擎   │
│   (docs/)       │───▶│   (ReactAgent)  │
└─────────────────┘    └─────────────────┘
         │                       │
         ▼                       ▼
┌─────────────────┐    ┌─────────────────┐
│   文档解析器     │    │   通义千问API    │
│   (PyPDF2)      │    │   (Qwen)        │
└─────────────────┘    └─────────────────┘
```

## 实现步骤

### 第一步：环境搭建

```bash
# 1. 安装Python依赖
pip install lazyllm PyPDF2

# 2. 设置API密钥
set QWEN_API_KEY=your-qwen-api-key-here
```

### 第二步：项目结构设计

```
项目目录
├── direct_rag.py        # 智能文档问答系统（核心）
├── docs/               # PDF文档存储文件夹
│   ├── *.pdf          # 自动扫描所有PDF文件
├── requirements.txt    # 依赖包列表
└── README.md          # 项目说明文档
```

### 第三步：核心功能实现

#### 1. 自动文档加载模块

```python
def load_all_documents():
    """自动加载docs文件夹中的所有PDF文档"""
    docs_path = os.path.join(os.path.dirname(__file__), "docs")
    
    # 自动扫描docs文件夹中的所有PDF文件
    pdf_files = [f for f in os.listdir(docs_path) if f.lower().endswith('.pdf')]
    
    for pdf_file in pdf_files:
        pdf_path = os.path.join(docs_path, pdf_file)
        try:
            content = extract_text_from_pdf(pdf_path)
            if content.strip():  # 只加载有内容的文件
                DOCUMENTS[pdf_file] = content
                print(f"[OK] 已加载: {pdf_file} ({len(content)} 字符)")
        except Exception as e:
            print(f"[ERROR] 加载失败: {pdf_file} - {str(e)}")
```

**技术亮点**：
- ✅ 无需硬编码文件名，自动扫描所有PDF文件
- ✅ 智能错误处理，跳过损坏或空文件
- ✅ 实时反馈加载状态和文档统计信息

#### 2. 智能问答引擎

```python
# 创建智能助手
agent = ReactAgent(
    llm=OnlineChatModule(stream=False),
    tools=['search_student_info', 'get_frontend_experience', 'get_gpa_info'],
    prompt="""你是一个智能文档分析助手，能够基于提供的文档内容回答关于学生信息的问题。
请根据用户的问题，调用相应的工具搜索文档信息，并基于找到的信息给出准确、详细的回答。""",
    stream=False
)

# 为每个问题创建独立实例，避免会话状态污染
fresh_agent = ReactAgent(...)
response = fresh_agent.forward(question)
```

**技术亮点**：
- 🔧 **会话状态隔离**：为每个问题创建独立agent实例，避免状态污染
- 🛠️ **多工具支持**：支持文档搜索、前端经验分析、GPA比较等多种专业工具
- 🎯 **精准回答**：基于文档内容提供准确、详细的回答

### 第四步：系统优化

#### 1. 错误处理优化
```python
# 类型安全比较
if data['status'] == '1' and int(data.get('count', 0)) > 0:
    # 安全地处理温度数据
    daytemp = str(live_info.get('daytemp', 'N/A'))
    nighttemp = str(live_info.get('nighttemp', 'N/A'))
```

#### 2. 编码问题解决
```python
# 避免emoji字符编码问题
print(f"[OK] 已加载: {pdf_file} ({len(content)} 字符)")
print(f"[ERROR] 加载失败: {pdf_file} - {str(e)}")
```

## 核心代码解析

### 1. 文档解析核心代码

```python
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
```

### 2. 智能搜索工具

```python
@fc_register("tool")
def search_student_info(query: str):
    """搜索学生相关信息"""
    results = []
    query_lower = query.lower()
    
    for filename, content in DOCUMENTS.items():
        if query_lower in content.lower():
            paragraphs = content.split('\n\n')
            for para in paragraphs:
                if query_lower in para.lower() and para.strip():
                    results.append({
                        "document": filename,
                        "content": para.strip()[:500]
                    })
    
    return json.dumps(results, ensure_ascii=False) if results else "未找到相关信息"
```

## 效果展示

### 1. 系统启动效果
```
正在加载PDF文档...
发现 7 个PDF文件:
[OK] 已加载: 张伟的个人简历.pdf (2298 字符)
[OK] 已加载: 李晨的个人简历.pdf (2370 字符)
[OK] 已加载: 李晨的技术博客文章.pdf (5345 字符)
...
成功加载 7 个文档
```

### 2. 智能问答效果

**问题1：前端负责人选择**
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
   - 主导Vue 2到Vue 3的技术升级
```

**问题2：学生信息查询**
```
问题: 李晨是一个怎样的同学?

回答: 李晨是一位**学术研究能力强、技术实力突出、项目经验丰富**的同学：

### 学术成就
- 浙江大学本科GPA 3.8/4.0，专业排名前10%
- 清华大学硕士，研究方向为自然语言处理
- 在国际会议发表3篇论文，其中1篇为第一作者

### 技术能力
- 字节跳动AI Lab算法工程师
- 专注RAG系统优化，准确率从64%提升到89%
- 响应延迟从2.3秒降低到1.4秒

### 综合素质
- 创新创业协会会长
- 获得省级创业大赛奖项
- 具备出色的团队协作和领导能力
```

**问题3：GPA比较**
```
问题: 张伟的GPA是不是最高的?

回答: 不是。根据文档信息：
- 李晨：3.8/4.0（最高）
- 王小明：3.7/4.0  
- 张伟：3.6/4.0（最低）

因此，李晨的GPA最高。
```

## 技术亮点总结

### 1. 自动化程度高
- ✅ 无需硬编码文件名，自动扫描docs文件夹
- ✅ 智能文档类型识别和内容提取
- ✅ 自动错误处理和状态反馈

### 2. 架构设计优秀
- 🔧 模块化设计，代码结构清晰
- 🛠️ 支持多种工具和功能扩展
- 🎯 会话状态隔离，避免状态污染

### 3. 用户体验佳
- 💬 支持自然语言交互
- 📊 实时反馈和状态显示

### 4. 扩展性强
- 🔌 易于添加新的文档类型支持
- 🛠️ 支持自定义工具和功能
- 📈 可扩展为更复杂的企业级应用

## 部署和使用

### 1. 环境准备
```bash
# 克隆项目
git clone https://github.com/your-username/lazyllm-rag-system.git
cd lazzllm-rag-system

# 安装依赖
pip install -r requirements.txt

# 设置API密钥
export QWEN_API_KEY="your-qwen-api-key"
```

### 2. 文档准备
将PDF文档放入`docs`文件夹，系统会自动扫描并加载。

### 3. 运行系统
```bash
# 运行文档问答系统
python direct_rag.py
```

## 项目总结

本项目成功构建了一个基于LazyLLM的智能文档问答系统，具有以下特点：

1. **技术先进**：采用最新的RAG技术，结合LazyLLM框架
2. **功能完整**：支持文档解析、智能问答等完整功能
3. **易于使用**：自动化程度高，用户只需放入文档即可使用
4. **扩展性强**：模块化设计，易于添加新功能
5. **实用价值**：可应用于企业文档管理、智能客服等实际场景

通过这个项目，我们不仅掌握了LazyLLM框架的使用，还深入理解了RAG技术的实现原理，为后续开发更复杂的企业级AI应用奠定了坚实基础。

## 代码托管

项目已上传至GitHub：https://github.com/your-username/lazyllm-rag-system

欢迎Star和Fork，一起交流学习！

---

**作者简介**：专注于AI技术研究和企业级应用开发，擅长大语言模型应用和RAG系统构建。

**联系方式**：如有问题欢迎在GitHub Issues中讨论或私信交流。
