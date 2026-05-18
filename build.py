import os
import markdown
import shutil

# --- 直接把配置写在这里，不再读取 config.py ---
SITE_TITLE = "ResonQ - Deciphering the Quantum Resonance"
SITE_DESCRIPTION = "A dedicated space for learning, sharing, and advocating for the success of quantum physics and computing."
BASE_URL = "https://resonq.com"

# 强制定位当前绝对路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, 'dist')
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
ARTICLES_DIR = os.path.join(BASE_DIR, 'articles')
STATIC_DIR = os.path.join(BASE_DIR, 'static')

def build():
    print(f"Build root: {BASE_DIR}")
    
    # 清理并创建 dist
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(os.path.join(OUTPUT_DIR, 'articles'), exist_ok=True)

    # 复制静态资源
    if os.path.exists(STATIC_DIR):
        shutil.copytree(STATIC_DIR, OUTPUT_DIR, dirs_exist_ok=True)
        print("✓ Static folder copied.")
    
    # 读取模板
    try:
        with open(os.path.join(TEMPLATES_DIR, 'index.html'), 'r', encoding='utf-8') as f:
            index_tpl = f.read()
        with open(os.path.join(TEMPLATES_DIR, 'article.html'), 'r', encoding='utf-8') as f:
            article_tpl = f.read()
    except Exception as e:
        print(f"Error loading templates: {e}")
        return

    # 渲染博文
    article_links = []
    if os.path.exists(ARTICLES_DIR):
        for filename in sorted(os.listdir(ARTICLES_DIR), reverse=True):
            if filename.endswith('.md'):
                with open(os.path.join(ARTICLES_DIR, filename), 'r', encoding='utf-8') as f:
                    content = f.read()
                
                lines = content.split('\n')
                title = lines[0].lstrip('#').strip()
                body = '\n'.join(lines[1:])
                html_body = markdown.markdown(body, extensions=['extra'])
                
                slug = filename.replace('.md', '')
                full_html = article_tpl.replace('{{ARTICLE_TITLE}}', title).replace('{{CONTENT}}', html_body).replace('{{SITE_TITLE}}', SITE_TITLE)
                
                with open(os.path.join(OUTPUT_DIR, 'articles', f'{slug}.html'), 'w', encoding='utf-8') as f:
                    f.write(full_html)
                article_links.append(f'<li><a href="/articles/{slug}.html">{title}</a></li>')

    # 生成首页
    index_html = index_tpl.replace('{{ARTICLE_LIST}}', '\n'.join(article_links)).replace('{{SITE_TITLE}}', SITE_TITLE)
    with open(os.path.join(OUTPUT_DIR, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(index_html)

    print("--- Build Complete! ---")
    print(f"Contents of {OUTPUT_DIR}: {os.listdir(OUTPUT_DIR)}")

if __name__ == "__main__":
    build()
