from flask import Flask, render_template_string, jsonify, request
import os

app = Flask(__name__)

# AI Tools data
AI_TOOLS = [
    {
        "name": "Augment Code",
        "description": "Enterprise-grade AI coding assistant with advanced code completion and refactoring capabilities.",
        "url": "https://augmentcode.com",
        "github": "https://github.com/augment-dev"
    },
    {
        "name": "Claude Code",
        "description": "Anthropic's AI assistant for coding, featuring Claude 3.5 Sonnet with CLI tools and git integration.",
        "url": "https://claude.com/claude-code",
        "github": "https://github.com/anthropics/claude-code"
    },
    {
        "name": "Cluely",
        "description": "AI companion that works across all your apps providing contextual assistance.",
        "url": "https://cluely.com",
        "github": None
    },
    {
        "name": "CodeBuddy",
        "description": "Lightweight AI pair programmer for collaborative coding sessions.",
        "url": "https://codebuddy.ai",
        "github": "https://github.com/codebuddy-ai"
    },
    {
        "name": "Comet",
        "description": "ML platform for tracking experiments and model performance.",
        "url": "https://comet.com",
        "github": "https://github.com/comet-ml"
    },
    {
        "name": "Cursor",
        "description": "AI-first code editor built on VS Code with intelligent code generation.",
        "url": "https://cursor.sh",
        "github": "https://github.com/getcursor/cursor"
    },
    {
        "name": "Devin AI",
        "description": "Autonomous AI software engineer from Cognition Labs.",
        "url": "https://devin.ai",
        "github": None
    },
    {
        "name": "Juni",
        "description": "AI-powered learning companion for coding education.",
        "url": "https://juni.com",
        "github": None
    }
]

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GitHub热门: AI Coding Tools</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            min-height: 100vh;
            padding: 40px 20px;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        h1 {
            text-align: center;
            color: #fff;
            font-size: 2.5rem;
            margin-bottom: 10px;
        }
        .subtitle {
            text-align: center;
            color: #888;
            margin-bottom: 40px;
        }
        .search-box {
            text-align: center;
            margin-bottom: 30px;
        }
        .search-box input {
            width: 100%;
            max-width: 400px;
            padding: 12px 20px;
            font-size: 1rem;
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 8px;
            background: rgba(255, 255, 255, 0.1);
            color: #fff;
            outline: none;
            transition: border-color 0.2s;
        }
        .search-box input::placeholder {
            color: #888;
        }
        .search-box input:focus {
            border-color: #58a6ff;
        }
        .tools-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 20px;
        }
        .tool-card {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            padding: 24px;
            transition: transform 0.3s, box-shadow 0.3s;
        }
        .tool-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
        }
        .tool-name {
            color: #58a6ff;
            font-size: 1.3rem;
            margin-bottom: 10px;
        }
        .tool-description {
            color: #c9d1d9;
            line-height: 1.6;
            margin-bottom: 15px;
        }
        .tool-links {
            display: flex;
            gap: 15px;
        }
        .tool-links a {
            color: #8b949e;
            text-decoration: none;
            font-size: 0.9rem;
            transition: color 0.2s;
        }
        .tool-links a:hover {
            color: #58a6ff;
        }
        .footer {
            text-align: center;
            margin-top: 50px;
            color: #666;
        }
        .no-results {
            text-align: center;
            color: #888;
            grid-column: 1 / -1;
            padding: 40px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>GitHub热门: AI Coding Tools</h1>
        <p class="subtitle">精选AI编程辅助工具</p>
        <div class="search-box">
            <input type="text" id="searchInput" placeholder="搜索工具..." oninput="filterTools()">
        </div>
        <script>
            const tools = {{ tools|tojson }};

            function renderTools(toolsToRender) {
                const grid = document.getElementById('toolsGrid');
                if (toolsToRender.length === 0) {
                    grid.innerHTML = '<p class="no-results">没有找到匹配的工具</p>';
                    return;
                }
                grid.innerHTML = toolsToRender.map(tool => `
                    <div class="tool-card">
                        <h2 class="tool-name">${tool.name}</h2>
                        <p class="tool-description">${tool.description}</p>
                        <div class="tool-links">
                            ${tool.url ? `<a href="${tool.url}" target="_blank">官网</a>` : ''}
                            ${tool.github ? `<a href="${tool.github}" target="_blank">GitHub</a>` : ''}
                        </div>
                    </div>
                `).join('');
            }

            function filterTools() {
                const query = document.getElementById('searchInput').value.toLowerCase();
                const filtered = tools.filter(tool =>
                    tool.name.toLowerCase().includes(query) ||
                    tool.description.toLowerCase().includes(query)
                );
                renderTools(filtered);
            }

            renderTools(tools);
        </script>
        <div class="tools-grid" id="toolsGrid">
            {% for tool in tools %}
            <div class="tool-card">
                <h2 class="tool-name">{{ tool.name }}</h2>
                <p class="tool-description">{{ tool.description }}</p>
                <div class="tool-links">
                    {% if tool.url %}
                    <a href="{{ tool.url }}" target="_blank">官网</a>
                    {% endif %}
                    {% if tool.github %}
                    <a href="{{ tool.github }}" target="_blank">GitHub</a>
                    {% endif %}
                </div>
            </div>
            {% endfor %}
        </div>
        <div class="footer">
            <p>Built with Flask</p>
        </div>
    </div>
</body>
</html>
'''


@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE, tools=AI_TOOLS)


@app.route('/api/tools')
def api_tools():
    return jsonify(AI_TOOLS)


@app.route('/api/tools/<tool_name>')
def api_tool_detail(tool_name):
    for tool in AI_TOOLS:
        if tool['name'].lower().replace(' ', '-') == tool_name.lower():
            return jsonify(tool)
    return jsonify({"error": "Tool not found"}), 404


@app.route('/health')
def health():
    return jsonify({"status": "ok", "message": "Server is running"})


@app.route('/api/tools/search')
def api_tools_search():
    query = request.args.get('q', '').lower()
    if not query:
        return jsonify(AI_TOOLS)
    filtered = [
        tool for tool in AI_TOOLS
        if query in tool['name'].lower() or query in tool['description'].lower()
    ]
    return jsonify(filtered)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
