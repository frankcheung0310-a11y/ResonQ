import os
import markdown
import shutil

# --- 核心：绝对路径定位 ---
# 不管脚本在哪里运行，强制获取当前脚本所在文件夹作为根目录
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(ROOT_DIR, 'dist')
TEMPLATES_DIR = os.path.join(ROOT_DIR, 'templates')
ARTICLES_DIR = os.path.join(ROOT_DIR, 'articles')
STATIC_DIR = os.path.join(ROOT_DIR, 'static')

def build():
    print(f"--- STARTING FINAL BUILD AT {ROOT_DIR} ---")
    
    # 1. 强制重置 dist 文件夹
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(os.path.join(OUTPUT_DIR, 'articles'), exist_ok=True)

    # 2. 复制图片 (确保 static/images 存在)
    if os.path.exists(STATIC_DIR):
        shutil.copytree(STATIC_DIR, OUTPUT_DIR, dirs_exist_ok=True)
        print("✓ Static resources copied.")
    else:
        print("! Warning: No 'static' directory found.")

    # 3. 读取模板
    try:
        with open(os.path.join(TEMPLATES_DIR, 'index.html'), 'r', encoding='utf-8') as f:
            idx_tpl = f.read()
        with open(os.path.join(TEMPLATES_DIR, 'article.html'), 'r', encoding='utf-8') as f:
            art_tpl = f.read()
    except Exception as e:
        print(f"! Error: Missing templates: {e}")
        return

    # 4. 处理 Markdown
    article_list = []
    if os.path.exists(ARTICLES_DIR):
        files = [f for f in os.listdir(ARTICLES_DIR) if f.endswith('.md')]
        for fname in sorted(files, reverse=True):
            with open(os.path.join(ARTICLES_DIR, fname), 'r', encoding='utf-8') as f:
                raw_md = f.read()
            
            lines = raw_md.split('\n')
            title = lines[0].lstrip('#').strip()
            body = '\n'.join(lines[1:])
            html_content = markdown.markdown(body, extensions=['extra'])
            
            slug = fname.replace('.md', '')
            # 填充模板
            full_page = art_tpl.replace('{{ARTICLE_TITLE}}', title).replace('{{CONTENT}}', html_content).replace('{{SITE_TITLE}}', "ResonQ")
            
            # 写入文章
            with open(os.path.join(OUTPUT_DIR, 'articles', f'{slug}.html'), 'w', encoding='utf-8') as f:
                f.write(full_page)
            
            article_list.append(f'<li><a href="/articles/{slug}.html">{title}</a></li>')
            print(f"✓ Processed article: {slug}")

    # 5. 写入首页
    final_index = idx_tpl.replace('{{ARTICLE_LIST}}', '\n'.join(article_list)).replace('{{SITE_TITLE}}', "ResonQ")
    with open(os.path.join(OUTPUT_DIR, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(final_index)

    print("--- BUILD SUCCESSFUL ---")
    print(f"Checking for 'dist' in {ROOT_DIR}: {os.path.exists(OUTPUT_DIR)}")
    print(f"Dist content: {os.listdir(OUTPUT_DIR)}")

if __name__ == "__main__":
    build()
