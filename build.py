import os
import markdown
import re
import shutil

# --- Configuration ---
POSTS_DIR = 'articles'      # 对应你截图中的 articles 文件夹
DIST_DIR = 'dist'          # Cloudflare 识别的输出目录
TEMPLATES_DIR = 'templates' # 对应你截图中的 templates 文件夹

# 强制确保输出目录结构正确 (Gritray 逻辑)
if not os.path.exists(DIST_DIR):
    os.makedirs(os.path.join(DIST_DIR, 'articles'), exist_ok=True)
elif not os.path.exists(os.path.join(DIST_DIR, 'articles')):
    os.makedirs(os.path.join(DIST_DIR, 'articles'), exist_ok=True)

# Load Templates
try:
    with open(f'{TEMPLATES_DIR}/index.html', 'r', encoding='utf-8') as f:
        index_tpl = f.read()
    with open(f'{TEMPLATES_DIR}/article.html', 'r', encoding='utf-8') as f:
        article_tpl = f.read()
except FileNotFoundError as e:
    print(f"Error: Template files not found in {TEMPLATES_DIR} folder.")
    exit(1)

posts_metadata = []

# --- Process Markdown Articles (Gritray 逻辑) ---
if not os.path.exists(POSTS_DIR):
    os.makedirs(POSTS_DIR)

for filename in os.listdir(POSTS_DIR):
    if filename.endswith('.md'):
        file_path = os.path.join(POSTS_DIR, filename)
        with open(file_path, 'r', encoding='utf-8') as f:
            raw_text = f.read()
            
            # 提取标题
            title_match = re.search(r'^#\s+(.*)', raw_text, re.MULTILINE)
            if title_match:
                title = title_match.group(1).strip()
                body_md = re.sub(r'^#\s+.*', '', raw_text, count=1, flags=re.MULTILINE)
            else:
                title = "Untitled Post"
                body_md = raw_text
            
            # 转换为 HTML (包含 Gritray 使用的插件)
            content_html = markdown.markdown(body_md, extensions=['extra', 'nl2br', 'sane_lists'])
            slug = filename.replace('.md', '.html')
            
            # 填充模板 (注意：根据你模板里的变量名，Gritray 用的是 {{TITLE}} 和 {{CONTENT}})
            full_article = article_tpl.replace('{{TITLE}}', title).replace('{{CONTENT}}', content_html)
            
            output_path = os.path.join(DIST_DIR, 'articles', slug)
            with open(output_path, 'w', encoding='utf-8') as out:
                out.write(full_article)
            
            posts_metadata.append({
                'title': title,
                'url': f'articles/{slug}'
            })

# Build Post Feed for Index
feed_html = ""
for post in posts_metadata:
    absolute_url = f"/{post['url']}"
    feed_html += f'''
    <a href="{absolute_url}" class="post-entry">
        <div class="post-title">{post['title']}</div>
    </a>'''

# Final Index Assembly
final_index = index_tpl.replace('{{POST_FEED}}', feed_html)
with open(os.path.join(DIST_DIR, 'index.html'), 'w', encoding='utf-8') as f:
    f.write(final_index)

# --- 关键修改：同步静态资源（含图片） ---
# 1. 搬运单个文件 (Gritray 原有逻辑)
static_assets = ['favicon.png', 'og-image.png']
for asset in static_assets:
    if os.path.exists(asset):
        shutil.copy(asset, os.path.join(DIST_DIR, asset))

# 2. 搬运整个 static 文件夹（ResonQ 的图片就在这里）
if os.path.exists('static'):
    # 这行会把 static/images 完整复制到 dist/static/images
    shutil.copytree('static', os.path.join(DIST_DIR, 'static'), dirs_exist_ok=True)
    print("Successfully synced: static folder (images)")

print(f"Build Complete! {len(posts_metadata)} articles generated.")
