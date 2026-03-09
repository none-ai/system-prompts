# GitHub热门: AI Coding Tools

展示精选的AI编程辅助工具的Flask Web应用。

## 包含的工具

- Augment Code
- Claude Code
- Cluely
- CodeBuddy
- Codeium
- Comet
- Cursor
- Devin AI
- GitHub Copilot
- Blackbox AI
- MutableAI
- Replit AI
- Tabnine
- Amazon CodeWhisperer
- Juni

## 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
```

### 运行应用

```bash
python app.py
```

服务器将在 http://localhost:5000 启动。

## 路由

| 路径 | 方法 | 说明 |
|------|------|------|
| `/` | GET | 主页面，显示所有AI工具 |
| `/api/tools` | GET | 获取所有工具的JSON数据 |
| `/api/tools/<name>` | GET | 获取指定工具的详细信息 |
| `/api/categories` | GET | 获取所有分类 |
| `/api/tools/category/<category>` | GET | 获取指定分类的工具 |
| `/api/stats` | GET | 获取工具统计信息 |
| `/health` | GET | 健康检查 |
| `/api/tools/search?q=<query>` | GET | 搜索工具 |

## 功能特性

- **搜索/过滤工具**：支持按名称或描述实时搜索
- **分类浏览**：按分类筛选工具（代码补全、AI助手、代码编辑器等）
- **收藏功能**：点击心形图标收藏喜欢的工具，数据保存到本地
- **工具详情**：点击卡片查看工具详细信息弹窗
- **主题切换**：支持深色/浅色主题切换
- **排序功能**：按名称或分类排序工具列表
- **统计信息**：显示工具总数和分类统计
- **分页浏览**：支持分页查看大量工具，每页显示12个

## 环境变量

- `PORT`: 服务器端口 (默认: 5000)

## 技术栈

- Flask
- HTML/CSS/JavaScript
- LocalStorage (收藏功能)

作者: stlin256的openclaw
