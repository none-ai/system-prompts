# GitHub热门: AI Coding Tools

展示精选的AI编程辅助工具的Flask Web应用。

## 包含的工具

- Augment Code
- Claude Code
- Cluely
- CodeBuddy
- Comet
- Cursor
- Devin AI
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
| `/health` | GET | 健康检查 |

## 环境变量

- `PORT`: 服务器端口 (默认: 5000)
