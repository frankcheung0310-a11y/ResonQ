import os
import markdown
import shutil

# --- 核心：强制定位到脚本所在目录 ---
# Cloudflare Pages 的根目录通常就是脚本所在的目录
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(ROOT_DIR, 'dist')
TEMPLATES_DIR = os.path.join(ROOT_DIR, 'templates')
ARTICLES_DIR = os.path.join(ROOT_DIR, 'articles')
STATIC_DIR = os.path.join(ROOT_DIR, 'static')

def build():
    print(f"--- HARDCORE BUILD START ---")
    print(f"Root Directory Identified as: {ROOT_DIR}")
    
    # 1. 准备/清理输出目录
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(os.path.join(OUTPUT_DIR, 'articles'), exist_ok=True)
    print(f"Output directory initialized at: {OUTPUT_DIR}")

    # 2. 搬运静态资源
    if os.path.exists(STATIC_DIR):
        shutil.copytree(STATIC_DIR, OUTPUT_DIR, dirs_exist_ok=True)
        print("✓ Static resources (images/css) copied.")
    else:
        print("! Warning: No 'static' directory found at the root.")

    # 3. 读取 HTML 模板
    try:
        with open(os.path.join(TEMPLATES_DIR, 'index.html'), 'r', encoding='utf-8') as f:
            index_tpl = f.read()
        with open(os.path.join(TEMPLATES_DIR, 'article.html'), 'r', encoding='utf-8') as f:
            article_tpl = f.read()
    except Exception as e:
        print(f"CRITICAL ERROR: Failed to load templates: {e}")
        return

    # 4. 扫描并渲染全英文文章
    article_links = []
    if os.path.exists(ARTICLES_DIR):
        md_files = [f for f in os.listdir(ARTICLES_DIR) if f.endswith('.md')]
        for fname in sorted(md_files, reverse=True):
            with open(os.path.join(ARTICLES_DIR, fname), 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 格式化
            lines = content.split('\n')
            title = lines[0].lstrip('#').strip() if lines else "ResonQ Insight"
            body = '\n'.join(lines[1:])
            html_body = markdown.markdown(body, extensions=['extra'])
            
            slug = fname.replace('.md', '')
            full_html = article_tpl.replace('{{ARTICLE_TITLE}}', title).replace('{{CONTENT}}', html_body).replace('{{SITE_TITLE}}', "ResonQ")
            
            # 写入文章文件
            with open(os.path.join(OUTPUT_DIR, 'articles', f'{slug}.html'), 'w', encoding='utf-8') as f:
                f.write(full_html)
            
            article_links.append(f'<li><a href="/articles/{slug}.html">{title}</a></li>')
            print(f"✓ Rendered: {slug}")

    # 5. 生成首页
    final_index = index_tpl.replace('{{ARTICLE_LIST}}', '\n'.join(article_links)).replace('{{SITE_TITLE}}', "ResonQ")
    with open(os.path.join(OUTPUT_DIR, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(final_index)

    print(f"--- BUILD PROCESS COMPLETE ---")
    # 自我检查：列出 ROOT 目录下的所有文件夹，看看 dist 在不在
    print(f"Files currently in {ROOT_DIR}: {os.listdir(ROOT_DIR)}")

if __name__ == "__main__":
    build()
