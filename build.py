import os
import markdown
import re
import shutil

# --- 配置 ---
POSTS_DIR = 'articles'
DIST_DIR = 'dist'
TEMPLATES_DIR = 'templates'
BASE_URL = 'https://resonq.com' # 用于预览卡片的地址

# 初始化目录
if os.path.exists(DIST_DIR):
    shutil.rmtree(DIST_DIR)
os.makedirs(os.path.join(DIST_DIR, 'articles'), exist_ok=True)

# 加载模板
try:
    with open(f'{TEMPLATES_DIR}/index.html', 'r', encoding='utf-8') as f:
        index_tpl = f.read()
    with open(f'{TEMPLATES_DIR}/article.html', 'r', encoding='utf-8') as f:
        article_tpl = f.read()
except FileNotFoundError:
    print("Error: Templates folder or files missing!")
    exit(1)

posts_metadata = []

# 处理 Markdown 文章
if os.path.exists(POSTS_DIR):
    for filename in os.listdir(POSTS_DIR):
        if filename.endswith('.md'):
            with open(os.path.join(POSTS_DIR, filename), 'r', encoding='utf-8') as f:
                raw_text = f.read()
            
            # 提取标题
            title_match = re.search(r'^#\s+(.*)', raw_text, re.MULTILINE)
            title = title_match.group(1).strip() if title_match else "Untitled Insight"
            body_md = re.sub(r'^#\s+.*', '', raw_text, count=1, flags=re.MULTILINE)
            
            # 转换内容
            content_html = markdown.markdown(body_md, extensions=['extra', 'nl2br', 'sane_lists'])
            slug = filename.replace('.md', '.html')
            
            # 填充预览卡片所需的变量
            full_article = article_tpl.replace('{{TITLE}}', title)
            full_article = full_article.replace('{{CONTENT}}', content_html)
            full_article = full_article.replace('{{URL}}', f'{BASE_URL}/articles/{slug}')
            
            with open(os.path.join(DIST_DIR, 'articles', slug), 'w', encoding='utf-8') as out:
                out.write(full_article)
            
            posts_metadata.append({'title': title, 'url': f'articles/{slug}'})

# 构建首页列表
feed_html = ""
for post in posts_metadata:
    feed_html += f'''
    <a href="/{post['url']}" class="post-entry">
        <div class="post-title">{post['title']}</div>
    </a>'''

# 生成首页
final_index = index_tpl.replace('{{POST_FEED}}', feed_html)
with open(os.path.join(DIST_DIR, 'index.html'), 'w', encoding='utf-8') as f:
    f.write(final_index)

# --- 静态资源搬运 ---
# 1. 搬运 favicon 等根目录文件
for asset in ['favicon.png', 'og-image.png']:
    if os.path.exists(asset):
        shutil.copy(asset, os.path.join(DIST_DIR, asset))

# 2. 搬运 static 文件夹 (包含 images)
if os.path.exists('static'):
    shutil.copytree('static', os.path.join(DIST_DIR, 'static'), dirs_exist_ok=True)
    print("Static assets synced.")

print(f"Build Successful: {len(posts_metadata)} posts.")
