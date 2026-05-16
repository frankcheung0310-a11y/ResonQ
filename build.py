# build.py
import os
import markdown
import config
import shutil

# --- 配置 ---
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(PROJECT_DIR, 'docs') # 输出目录为 docs，方便 GitHub Pages 部署
TEMPLATES_DIR = os.path.join(PROJECT_DIR, 'templates')
ARTICLES_DIR = os.path.join(PROJECT_DIR, 'articles')
STATIC_DIR = os.path.join(PROJECT_DIR, 'static') # 如果有静态文件（CSS、图片等）

# --- 工具函数 ---
def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

# --- 构建主逻辑 ---
def build():
    # 1. 清理旧的输出
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.makedirs(OUTPUT_DIR)

    # 2. 如果有静态文件，复制过去
    if os.path.exists(STATIC_DIR):
        shutil.copytree(STATIC_DIR, OUTPUT_DIR, dirs_exist_ok=True)

    # 3. 读取模板
    index_template = read_file(os.path.join(TEMPLATES_DIR, 'index.html'))
    article_template = read_file(os.path.join(TEMPLATES_DIR, 'article.html'))

    # 4. 读取并转换文章 (使用 Markdown 文件)
    article_list = []
    if os.path.exists(ARTICLES_DIR):
        for filename in os.listdir(ARTICLES_DIR):
            if filename.endswith('.md'):
                md_content = read_file(os.path.join(ARTICLES_DIR, filename))
                
                # 分离 Markdown 元数据（标题、日期等）和正文
                # 这里使用最简单的方式：Markdown 第一行必须是标题 " # 标题 "
                lines = md_content.split('\n')
                title = lines[0].strip('# ').strip()
                post_content = '\n'.join(lines[1:])

                html_content = markdown.markdown(post_content)
                
                # 生成文章 URL
                article_slug = filename.rsplit('.', 1)[0]
                article_url = f"/articles/{article_slug}.html"
                
                # 渲染文章页
                full_article_html = article_template.replace('{{SITE_TITLE}}', config.SITE_TITLE)
                full_article_html = full_article_html.replace('{{ARTICLE_TITLE}}', title)
                full_article_html = full_article_html.replace('{{AUTHOR}}', config.SITE_AUTHOR)
                full_article_html = full_article_html.replace('{{SITE_DESCRIPTION}}', config.SITE_DESCRIPTION)
                full_article_html = full_article_html.replace('{{BASE_URL}}', config.BASE_URL)
                full_article_html = full_article_html.replace('{{CONTENT}}', html_content)
                
                # 写入文章 HTML 文件
                write_file(os.path.join(OUTPUT_DIR, 'articles', f'{article_slug}.html'), full_article_html)
                
                article_list.append({
                    'title': title,
                    'url': article_url
                })

    # 5. 渲染首页
    article_links_html = ""
    for article in article_list:
        article_links_html += f'<li><a href="{article["url"]}">{article["title"]}</a></li>'
    
    full_index_html = index_template.replace('{{SITE_TITLE}}', config.SITE_TITLE)
    full_index_html = full_index_html.replace('{{SITE_DESCRIPTION}}', config.SITE_DESCRIPTION)
    full_index_html = full_index_html.replace('{{ARTICLE_LIST}}', article_links_html)
    full_index_html = full_index_html.replace('{{BASE_URL}}', config.BASE_URL)
    
    # 写入首页 HTML 文件
    write_file(os.path.join(OUTPUT_DIR, 'index.html'), full_index_html)

    print(f"Website built successfully in {OUTPUT_DIR}")

if __name__ == "__main__":
    build()
