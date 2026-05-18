import os
import markdown
import shutil

# 获取脚本所在目录（根目录）
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, 'dist')

def build():
    # 1. 强制重置 dist 目录
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.makedirs(OUTPUT_DIR)
    os.makedirs(os.path.join(OUTPUT_DIR, 'articles'))

    # 2. 复制静态资源 (static 目录)
    if os.path.exists('static'):
        shutil.copytree('static', OUTPUT_DIR, dirs_exist_ok=True)

    # 3. 读取模板
    with open('templates/index.html', 'r', encoding='utf-8') as f:
        index_tpl = f.read()
    with open('templates/article.html', 'r', encoding='utf-8') as f:
        article_tpl = f.read()

    # 4. 处理文章
    article_links = []
    articles_path = 'articles'
    for filename in sorted(os.listdir(articles_path), reverse=True):
        if filename.endswith('.md'):
            with open(os.path.join(articles_path, filename), 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 简单的 Markdown 处理
            title = content.split('\n')[0].lstrip('# ')
            html_body = markdown.markdown(content)
            
            slug = filename.replace('.md', '')
            full_html = article_tpl.replace('{{ARTICLE_TITLE}}', title).replace('{{CONTENT}}', html_body)
            
            with open(os.path.join(OUTPUT_DIR, 'articles', f'{slug}.html'), 'w', encoding='utf-8') as f:
                f.write(full_html)
            article_links.append(f'<li><a href="/articles/{slug}.html">{title}</a></li>')

    # 5. 生成首页
    final_index = index_tpl.replace('{{ARTICLE_LIST}}', '\n'.join(article_links))
    with open(os.path.join(OUTPUT_DIR, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(final_index)
    
    print("Build Complete! dist folder created at:", OUTPUT_DIR)

if __name__ == "__main__":
    build()
