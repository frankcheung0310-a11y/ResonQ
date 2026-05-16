import os
import markdown
import shutil

# --- 核心：强制使用当前工作目录 ---
# Cloudflare 在运行时，os.getcwd() 通常是仓库根目录
current_dir = os.getcwd()
OUTPUT_DIR = os.path.join(current_dir, 'dist')
TEMPLATES_DIR = os.path.join(current_dir, 'templates')
ARTICLES_DIR = os.path.join(current_dir, 'articles')
STATIC_DIR = os.path.join(current_dir, 'static')

def build():
    print(f"Build starting... Current working directory: {current_dir}")
    
    # 1. 准备目录
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(os.path.join(OUTPUT_DIR, 'articles'), exist_ok=True)
    print(f"Created output directory at: {OUTPUT_DIR}")

    # 2. 复制图片和静态文件
    if os.path.exists(STATIC_DIR):
        shutil.copytree(STATIC_DIR, OUTPUT_DIR, dirs_exist_ok=True)
        print("Static files (images) copied.")
    else:
        print("Warning: 'static' folder not found. Skipping static copy.")

    # 3. 读取模板
    try:
        with open(os.path.join(TEMPLATES_DIR, 'index.html'), 'r', encoding='utf-8') as f:
            index_tpl = f.read()
        with open(os.path.join(TEMPLATES_DIR, 'article.html'), 'r', encoding='utf-8') as f:
            article_tpl = f.read()
    except Exception as e:
        print(f"Error loading templates: {e}")
        return

    # 4. 渲染 Markdown
    article_links = []
    if os.path.exists(ARTICLES_DIR):
        files = [f for f in os.listdir(ARTICLES_DIR) if f.endswith('.md')]
        for filename in sorted(files, reverse=True):
            with open(os.path.join(ARTICLES_DIR, filename), 'r', encoding='utf-8') as f:
                content = f.read()
            
            lines = content.split('\n')
            title = lines[0].lstrip('#').strip() if lines else "Untitled"
            body = '\n'.join(lines[1:])
            html_body = markdown.markdown(body, extensions=['extra'])
            
            slug = filename.replace('.md', '')
            full_html = article_tpl.replace('{{ARTICLE_TITLE}}', title).replace('{{CONTENT}}', html_body).replace('{{SITE_TITLE}}', "ResonQ")
            
            with open(os.path.join(OUTPUT_DIR, 'articles', f'{slug}.html'), 'w', encoding='utf-8') as f:
                f.write(full_html)
            
            article_links.append(f'<li><a href="/articles/{slug}.html">{title}</a></li>')
            print(f"Processed: {filename}")

    # 5. 生成首页
    index_html = index_tpl.replace('{{ARTICLE_LIST}}', '\n'.join(article_links)).replace('{{SITE_TITLE}}', "ResonQ")
    with open(os.path.join(OUTPUT_DIR, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(index_html)

    print("Build Complete!")
    # 关键自检：列出根目录下的内容
    print(f"Final directory check (root): {os.listdir(current_dir)}")
    if 'dist' in os.listdir(current_dir):
        print(f"Success! 'dist' exists. Contents: {os.listdir(OUTPUT_DIR)}")
    else:
        print("Failure: 'dist' folder is missing from the root!")

if __name__ == "__main__":
    build()
