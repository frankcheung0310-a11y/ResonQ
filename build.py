import os
import markdown
import shutil

# --- 强制路径配置 ---
# 直接使用当前工作目录，确保 Cloudflare 能在根部看到 dist
BASE_DIR = os.getcwd()
OUTPUT_DIR = os.path.join(BASE_DIR, 'dist') 
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
ARTICLES_DIR = os.path.join(BASE_DIR, 'articles')
STATIC_DIR = os.path.join(BASE_DIR, 'static')

SITE_TITLE = "ResonQ"
SITE_DESCRIPTION = "Deciphering the Quantum Resonance"
BASE_URL = "https://resonq.com"

def build():
    print(f"Current Working Directory: {BASE_DIR}")
    
    # 确保输出目录干净且存在
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(os.path.join(OUTPUT_DIR, 'articles'), exist_ok=True)
    print(f"Created directory: {OUTPUT_DIR}")

    # 复制静态资源（图片等）
    if os.path.exists(STATIC_DIR):
        shutil.copytree(STATIC_DIR, OUTPUT_DIR, dirs_exist_ok=True)
        print("Static files copied.")

    # 加载模板
    index_tpl = open(os.path.join(TEMPLATES_DIR, 'index.html'), encoding='utf-8').read()
    article_tpl = open(os.path.join(TEMPLATES_DIR, 'article.html'), encoding='utf-8').read()

    article_list = []
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

                # 渲染并写入文章页
                full_html = article_tpl.replace('{{ARTICLE_TITLE}}', title)
                full_html = full_html.replace('{{CONTENT}}', html_body)
                full_html = full_html.replace('{{SITE_TITLE}}', SITE_TITLE)
                full_html = full_html.replace('{{BASE_URL}}', BASE_URL)

                with open(os.path.join(OUTPUT_DIR, 'articles', f'{slug}.html'), 'w', encoding='utf-8') as f:
                    f.write(full_html)
                
                article_list.append(f'<li><a href="/articles/{slug}.html">{title}</a></li>')
                print(f"Article rendered: {slug}")

    # 渲染并写入首页
    index_html = index_tpl.replace('{{ARTICLE_LIST}}', '\n'.join(article_list))
    index_html = index_html.replace('{{SITE_TITLE}}', SITE_TITLE)
    index_html = index_html.replace('{{SITE_DESCRIPTION}}', SITE_DESCRIPTION)

    with open(os.path.join(OUTPUT_DIR, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(index_html)

    print("!!! BUILD PROCESS FINISHED SUCCESSFULLY !!!")
    # 列出 dist 目录内容，方便在日志里查看到底生成没
    print(f"Files in dist: {os.listdir(OUTPUT_DIR)}")

if __name__ == "__main__":
    build()
