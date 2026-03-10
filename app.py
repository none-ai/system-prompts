from flask import Flask, render_template_string, jsonify, request
import os

app = Flask(__name__)

# AI Tools data with categories
AI_TOOLS = [
    {
        "name": "Augment Code",
        "description": "Enterprise-grade AI coding assistant with advanced code completion and refactoring capabilities.",
        "url": "https://augmentcode.com",
        "github": "https://github.com/augment-dev",
        "category": "code-completion"
    },
    {
        "name": "Claude Code",
        "description": "Anthropic's AI assistant for coding, featuring Claude 3.5 Sonnet with CLI tools and git integration.",
        "url": "https://claude.com/claude-code",
        "github": "https://github.com/anthropics/claude-code",
        "category": "ai-assistant"
    },
    {
        "name": "Cluely",
        "description": "AI companion that works across all your apps providing contextual assistance.",
        "url": "https://cluely.com",
        "github": None,
        "category": "ai-assistant"
    },
    {
        "name": "CodeBuddy",
        "description": "Lightweight AI pair programmer for collaborative coding sessions.",
        "url": "https://codebuddy.ai",
        "github": "https://github.com/codebuddy-ai",
        "category": "code-completion"
    },
    {
        "name": "Comet",
        "description": "ML platform for tracking experiments and model performance.",
        "url": "https://comet.com",
        "github": "https://github.com/comet-ml",
        "category": "ml-tools"
    },
    {
        "name": "Cursor",
        "description": "AI-first code editor built on VS Code with intelligent code generation.",
        "url": "https://cursor.sh",
        "github": "https://github.com/getcursor/cursor",
        "category": "code-editor"
    },
    {
        "name": "Devin AI",
        "description": "Autonomous AI software engineer from Cognition Labs.",
        "url": "https://devin.ai",
        "github": None,
        "category": "ai-engineer"
    },
    {
        "name": "Juni",
        "description": "AI-powered learning companion for coding education.",
        "url": "https://juni.com",
        "github": None,
        "category": "education"
    },
    {
        "name": "GitHub Copilot",
        "description": "AI pair programmer by GitHub and OpenAI, integrated into VS Code and other editors.",
        "url": "https://github.com/features/copilot",
        "github": None,
        "category": "code-completion"
    },
    {
        "name": "Tabnine",
        "description": "AI code completion assistant that learns from your code patterns.",
        "url": "https://tabnine.com",
        "github": "https://github.com/codota/tabnine",
        "category": "code-completion"
    },
    {
        "name": "Replit AI",
        "description": "AI-powered coding environment with instant deployment capabilities.",
        "url": "https://replit.com/ai",
        "github": None,
        "category": "code-editor"
    },
    {
        "name": "Codeium",
        "description": "Free AI-powered code completion and chat for developers.",
        "url": "https://codeium.com",
        "github": "https://github.com/codeium",
        "category": "code-completion"
    },
    {
        "name": "Amazon CodeWhisperer",
        "description": "AI code generation companion from AWS.",
        "url": "https://aws.amazon.com/codewhisperer",
        "github": None,
        "category": "code-completion"
    },
    {
        "name": "MutableAI",
        "description": "AI-powered coding platform with real-time collaboration.",
        "url": "https://mutable.ai",
        "github": None,
        "category": "ai-assistant"
    },
    {
        "name": "Blackbox AI",
        "description": "AI code assistant with chat and code generation capabilities.",
        "url": "https://blackbox.ai",
        "github": None,
        "category": "ai-assistant"
    }
]

# Category display names
CATEGORIES = {
    "code-completion": "代码补全",
    "code-editor": "代码编辑器",
    "ai-assistant": "AI助手",
    "ai-engineer": "AI工程师",
    "ml-tools": "机器学习工具",
    "education": "编程教育"
}

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GitHub热门: AI Coding Tools</title>
    <style>
        :root {
            --bg-primary: #1a1a2e;
            --bg-secondary: #16213e;
            --bg-card: rgba(255, 255, 255, 0.05);
            --border-color: rgba(255, 255, 255, 0.1);
            --text-primary: #fff;
            --text-secondary: #c9d1d9;
            --text-muted: #888;
            --accent-color: #58a6ff;
            --hover-color: rgba(0, 0, 0, 0.3);
        }
        .light-theme {
            --bg-primary: #f5f5f5;
            --bg-secondary: #ffffff;
            --bg-card: #ffffff;
            --border-color: rgba(0, 0, 0, 0.1);
            --text-primary: #1a1a2e;
            --text-secondary: #555;
            --text-muted: #666;
            --accent-color: #0969da;
            --hover-color: rgba(0, 0, 0, 0.1);
        }
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, var(--bg-primary) 0%, var(--bg-secondary) 100%);
            min-height: 100vh;
            padding: 40px 20px;
            color: var(--text-primary);
            transition: background 0.3s, color 0.3s;
        }
        .light-theme body {
            background: linear-gradient(135deg, #f0f2f5 0%, #ffffff 100%);
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
        }
        h1 {
            text-align: center;
            color: var(--text-primary);
            font-size: 2.5rem;
            margin-bottom: 10px;
            flex: 1;
        }
        .theme-toggle {
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 8px 12px;
            cursor: pointer;
            color: var(--text-primary);
            font-size: 1.2rem;
            transition: background 0.2s;
        }
        .theme-toggle:hover {
            background: var(--hover-color);
        }
        .subtitle {
            text-align: center;
            color: var(--text-muted);
            margin-bottom: 40px;
        }
        .controls {
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 15px;
            margin-bottom: 30px;
        }
        .search-box {
            flex: 1;
            min-width: 250px;
        }
        .search-box input {
            width: 100%;
            padding: 12px 20px;
            font-size: 1rem;
            border: 1px solid var(--border-color);
            border-radius: 8px;
            background: var(--bg-card);
            color: var(--text-primary);
            outline: none;
            transition: border-color 0.2s;
        }
        .search-box input::placeholder {
            color: var(--text-muted);
        }
        .search-box input:focus {
            border-color: var(--accent-color);
        }
        .filter-controls {
            display: flex;
            gap: 10px;
            align-items: center;
        }
        .filter-controls select {
            padding: 10px 15px;
            font-size: 0.95rem;
            border: 1px solid var(--border-color);
            border-radius: 8px;
            background: var(--bg-card);
            color: var(--text-primary);
            cursor: pointer;
        }
        .filter-btn {
            padding: 10px 15px;
            font-size: 0.95rem;
            border: 1px solid var(--border-color);
            border-radius: 8px;
            background: var(--bg-card);
            color: var(--text-primary);
            cursor: pointer;
            transition: all 0.2s;
        }
        .filter-btn.active {
            background: var(--accent-color);
            border-color: var(--accent-color);
        }
        .stats {
            text-align: center;
            margin-bottom: 20px;
            color: var(--text-muted);
        }
        .tools-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 20px;
        }
        .tool-card {
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 24px;
            transition: transform 0.3s, box-shadow 0.3s;
            cursor: pointer;
            position: relative;
        }
        .tool-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 30px var(--hover-color);
        }
        .tool-card.favorite {
            border-color: #f85149;
        }
        .favorite-btn {
            position: absolute;
            top: 15px;
            right: 15px;
            background: none;
            border: none;
            font-size: 1.3rem;
            cursor: pointer;
            color: var(--text-muted);
            transition: transform 0.2s;
        }
        .favorite-btn:hover {
            transform: scale(1.2);
        }
        .favorite-btn.active {
            color: #f85149;
        }
        .tool-category {
            display: inline-block;
            background: var(--accent-color);
            color: #fff;
            padding: 3px 10px;
            border-radius: 20px;
            font-size: 0.75rem;
            margin-bottom: 10px;
        }
        .tool-name {
            color: var(--accent-color);
            font-size: 1.3rem;
            margin-bottom: 10px;
        }
        .tool-description {
            color: var(--text-secondary);
            line-height: 1.6;
            margin-bottom: 15px;
        }
        .tool-links {
            display: flex;
            gap: 15px;
        }
        .tool-links a {
            color: var(--text-muted);
            text-decoration: none;
            font-size: 0.9rem;
            transition: color 0.2s;
        }
        .tool-links a:hover {
            color: var(--accent-color);
        }
        .footer {
            text-align: center;
            margin-top: 50px;
            color: var(--text-muted);
        }
        .no-results {
            text-align: center;
            color: var(--text-muted);
            grid-column: 1 / -1;
            padding: 40px;
        }
        /* Modal Styles */
        .modal-overlay {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.7);
            z-index: 1000;
            justify-content: center;
            align-items: center;
        }
        .modal-overlay.active {
            display: flex;
        }
        .modal {
            background: var(--bg-secondary);
            border: 1px solid var(--border-color);
            border-radius: 16px;
            padding: 30px;
            max-width: 600px;
            width: 90%;
            max-height: 80vh;
            overflow-y: auto;
            position: relative;
        }
        .modal-close {
            position: absolute;
            top: 15px;
            right: 15px;
            background: none;
            border: none;
            font-size: 1.5rem;
            color: var(--text-muted);
            cursor: pointer;
        }
        .modal-category {
            display: inline-block;
            background: var(--accent-color);
            color: #fff;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.85rem;
            margin-bottom: 15px;
        }
        .modal h2 {
            color: var(--accent-color);
            font-size: 1.8rem;
            margin-bottom: 15px;
        }
        .modal p {
            color: var(--text-secondary);
            line-height: 1.8;
            margin-bottom: 20px;
        }
        .modal-links {
            display: flex;
            gap: 15px;
        }
        .modal-links a {
            padding: 10px 20px;
            background: var(--accent-color);
            color: #fff;
            text-decoration: none;
            border-radius: 8px;
            transition: opacity 0.2s;
        }
        .modal-links a:hover {
            opacity: 0.9;
        }
        .pagination {
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 10px;
            margin-top: 30px;
        }
        .pagination button {
            padding: 8px 15px;
            border: 1px solid var(--border-color);
            border-radius: 6px;
            background: var(--bg-card);
            color: var(--text-primary);
            cursor: pointer;
            transition: all 0.2s;
        }
        .pagination button:hover:not(:disabled) {
            background: var(--accent-color);
            border-color: var(--accent-color);
        }
        .pagination button:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }
        .pagination .page-info {
            color: var(--text-secondary);
            font-size: 0.9rem;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>GitHub热门: AI Coding Tools</h1>
            <button class="theme-toggle" onclick="toggleTheme()" title="切换主题">🌙</button>
        </div>
        <p class="subtitle">精选AI编程辅助工具</p>

        <div class="controls">
            <div class="search-box">
                <input type="text" id="searchInput" placeholder="搜索工具..." oninput="filterTools()">
            </div>
            <div class="filter-controls">
                <select id="categoryFilter" onchange="filterTools()">
                    <option value="">全部分类</option>
                </select>
                <select id="sortSelect" onchange="filterTools()">
                    <option value="name">按名称排序</option>
                    <option value="category">按分类排序</option>
                </select>
                <button class="filter-btn" id="favoritesFilter" onclick="toggleFavoritesFilter()">
                    ❤️ 收藏 only
                </button>
            </div>
        </div>

        <div class="stats" id="stats"></div>

        <div class="tools-grid" id="toolsGrid"></div>

        <div class="pagination" id="pagination"></div>

        <div class="footer">
            <p>Built with Flask | 共 <span id="toolCount">0</span> 个工具</p>
        </div>
    </div>

    <!-- Modal -->
    <div class="modal-overlay" id="modalOverlay" onclick="closeModal(event)">
        <div class="modal" onclick="event.stopPropagation()">
            <button class="modal-close" onclick="closeModal()">&times;</button>
            <span class="modal-category" id="modalCategory"></span>
            <h2 id="modalTitle"></h2>
            <p id="modalDescription"></p>
            <div class="modal-links" id="modalLinks"></div>
        </div>
    </div>

    <script>
        const tools = {{ tools|tojson }};
        const categories = {{ categories|tojson }};
        let favorites = JSON.parse(localStorage.getItem('favorites') || '[]');
        let showFavoritesOnly = false;
        const ITEMS_PER_PAGE = 12;
        let currentPage = 1;
        let filteredToolsCache = [];

        // Initialize category filter
        function initCategories() {
            const select = document.getElementById('categoryFilter');
            for (const [key, value] of Object.entries(categories)) {
                const option = document.createElement('option');
                option.value = key;
                option.textContent = value;
                select.appendChild(option);
            }
        }

        // Toggle theme
        function toggleTheme() {
            document.body.classList.toggle('light-theme');
            const btn = document.querySelector('.theme-toggle');
            btn.textContent = document.body.classList.contains('light-theme') ? '☀️' : '🌙';
            localStorage.setItem('theme', document.body.classList.contains('light-theme') ? 'light' : 'dark');
        }

        // Load theme preference
        function loadTheme() {
            const theme = localStorage.getItem('theme');
            if (theme === 'light') {
                document.body.classList.add('light-theme');
                document.querySelector('.theme-toggle').textContent = '☀️';
            }
        }

        // Toggle favorites filter
        function toggleFavoritesFilter() {
            showFavoritesOnly = !showFavoritesOnly;
            document.getElementById('favoritesFilter').classList.toggle('active', showFavoritesOnly);
            filterTools();
        }

        // Toggle favorite
        function toggleFavorite(e, toolName) {
            e.stopPropagation();
            const index = favorites.indexOf(toolName);
            if (index > -1) {
                favorites.splice(index, 1);
            } else {
                favorites.push(toolName);
            }
            localStorage.setItem('favorites', JSON.stringify(favorites));
            filterTools();
        }

        // Render tools with pagination
        function renderTools(toolsToRender) {
            filteredToolsCache = toolsToRender;
            currentPage = 1;
            renderToolsPage();
            renderPagination();
        }

        function renderToolsPage() {
            const grid = document.getElementById('toolsGrid');
            const start = (currentPage - 1) * ITEMS_PER_PAGE;
            const end = start + ITEMS_PER_PAGE;
            const pageTools = filteredToolsCache.slice(start, end);

            if (filteredToolsCache.length === 0) {
                grid.innerHTML = '<p class="no-results">没有找到匹配的工具</p>';
                document.getElementById('pagination').innerHTML = '';
                return;
            }

            grid.innerHTML = pageTools.map(tool => `
                <div class="tool-card ${favorites.includes(tool.name) ? 'favorite' : ''}" onclick="showToolDetail('${tool.name}')">
                    <button class="favorite-btn ${favorites.includes(tool.name) ? 'active' : ''}" onclick="toggleFavorite(event, '${tool.name}')">
                        ${favorites.includes(tool.name) ? '❤️' : '🤍'}
                    </button>
                    <span class="tool-category">${categories[tool.category] || tool.category}</span>
                    <h2 class="tool-name">${tool.name}</h2>
                    <p class="tool-description">${tool.description}</p>
                    <div class="tool-links">
                        ${tool.url ? `<a href="${tool.url}" target="_blank">官网</a>` : ''}
                        ${tool.github ? `<a href="${tool.github}" target="_blank">GitHub</a>` : ''}
                    </div>
                </div>
            `).join('');

            document.getElementById('toolCount').textContent = filteredToolsCache.length;
            document.getElementById('stats').textContent = showFavoritesOnly ? `显示 ${filteredToolsCache.length} 个收藏工具` : `共 ${tools.length} 个工具，其中 ${favorites.length} 个收藏`;
        }

        function renderPagination() {
            const totalPages = Math.ceil(filteredToolsCache.length / ITEMS_PER_PAGE);
            const pagination = document.getElementById('pagination');

            if (totalPages <= 1) {
                pagination.innerHTML = '';
                return;
            }

            let html = `
                <button onclick="goToPage(${currentPage - 1})" ${currentPage === 1 ? 'disabled' : ''}>上一页</button>
                <span class="page-info">${currentPage} / ${totalPages}</span>
                <button onclick="goToPage(${currentPage + 1})" ${currentPage === totalPages ? 'disabled' : ''}>下一页</button>
            `;
            pagination.innerHTML = html;
        }

        function goToPage(page) {
            const totalPages = Math.ceil(filteredToolsCache.length / ITEMS_PER_PAGE);
            if (page < 1 || page > totalPages) return;
            currentPage = page;
            renderToolsPage();
            renderPagination();
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }

        // Filter and sort tools
        function filterTools() {
            const query = document.getElementById('searchInput').value.toLowerCase();
            const category = document.getElementById('categoryFilter').value;
            const sortBy = document.getElementById('sortSelect').value;

            let filtered = tools.filter(tool => {
                const matchesSearch = tool.name.toLowerCase().includes(query) ||
                    tool.description.toLowerCase().includes(query);
                const matchesCategory = !category || tool.category === category;
                const matchesFavorites = !showFavoritesOnly || favorites.includes(tool.name);
                return matchesSearch && matchesCategory && matchesFavorites;
            });

            // Sort
            filtered.sort((a, b) => {
                if (sortBy === 'category') {
                    return (categories[a.category] || a.category).localeCompare(categories[b.category] || b.category);
                }
                return a.name.localeCompare(b.name);
            });

            renderTools(filtered);
        }

        // Show tool detail modal
        function showToolDetail(toolName) {
            const tool = tools.find(t => t.name === toolName);
            if (!tool) return;

            document.getElementById('modalCategory').textContent = categories[tool.category] || tool.category;
            document.getElementById('modalTitle').textContent = tool.name;
            document.getElementById('modalDescription').textContent = tool.description;

            let linksHtml = '';
            if (tool.url) {
                linksHtml += `<a href="${tool.url}" target="_blank">访问官网</a>`;
            }
            if (tool.github) {
                linksHtml += `<a href="${tool.github}" target="_blank">GitHub</a>`;
            }
            document.getElementById('modalLinks').innerHTML = linksHtml;

            document.getElementById('modalOverlay').classList.add('active');
        }

        // Close modal
        function closeModal(event) {
            if (!event || event.target === document.getElementById('modalOverlay')) {
                document.getElementById('modalOverlay').classList.remove('active');
            }
        }

        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') closeModal();
        });

        // Initialize
        loadTheme();
        initCategories();
        filterTools();
    </script>
</body>
</html>
'''


@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE, tools=AI_TOOLS, categories=CATEGORIES)


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


@app.route('/api/categories')
def api_categories():
    """Get all categories"""
    return jsonify(CATEGORIES)


@app.route('/api/tools/category/<category>')
def api_tools_by_category(category):
    """Get tools by category"""
    filtered = [tool for tool in AI_TOOLS if tool['category'] == category]
    return jsonify(filtered)


@app.route('/api/stats')
def api_stats():
    """Get statistics about tools"""
    category_count = {}
    for tool in AI_TOOLS:
        cat = tool.get('category', 'unknown')
        category_count[cat] = category_count.get(cat, 0) + 1
    return jsonify({
        "total": len(AI_TOOLS),
        "by_category": category_count,
        "categories": list(CATEGORIES.keys())
    })


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'false').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)
