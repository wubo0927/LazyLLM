#!/bin/bash
# GitHub仓库初始化脚本

echo "🚀 初始化LazyLLM智能文档问答系统GitHub仓库"

# 1. 初始化Git仓库
git init

# 2. 添加所有文件
git add .

# 3. 创建初始提交
git commit -m "🎉 初始提交：基于LazyLLM的智能文档问答系统

✨ 功能特性：
- 自动PDF文档解析
- 智能问答系统
- 天气查询集成
- Web界面支持
- 模块化设计

🛠️ 技术栈：
- LazyLLM框架
- 通义千问API
- PyPDF2文档解析
- ReactAgent智能代理"

# 4. 添加远程仓库（需要替换为实际的GitHub仓库地址）
echo "请手动执行以下命令添加远程仓库："
echo "git remote add origin https://github.com/your-username/lazyllm-rag-system.git"
echo "git branch -M main"
echo "git push -u origin main"

echo "✅ Git仓库初始化完成！"
echo "📝 请记得："
echo "1. 在GitHub上创建新仓库"
echo "2. 替换上面的远程仓库地址"
echo "3. 执行推送命令"
