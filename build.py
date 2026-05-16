import os
import markdown
import shutil

# --- 1. 核心路径配置 (适配 Cloudflare) ---
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
# 必须叫 dist，因为这是你在 Cloudflare 设置的 Build output directory
OUTPUT_DIR = os.path.join(PROJECT_DIR, 'dist') 
TEMPLATES_DIR = os.path.join(PROJECT_DIR, 'templates')
ARTICLES_DIR = os.path.join(PROJECT_DIR, 'articles')
STATIC_DIR = os.path.join(PROJECT_DIR, 'static')

# 假设的站点配置（也可以写在 config.py，但这里直接内置更稳）
SITE_TITLE = "ResonQ"
SITE_DESCRIPTION = "Deciphering the Quantum Resonance - A Journey into Information & Physics"
BASE_URL = "https://resonq.com"

def build():
    print("Starting build process...")

    # 2. 清理并重新创建输出目录
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.makedirs(OUTPUT_DIR)
    os.makedirs(os.path.join(OUTPUT_DIR, 'articles'), exist_ok=True)

    # 3. 核心：搬运静态文件（图片就靠这一步）
    if os.path.exists(STATIC_DIR):
        # 将 static 文件夹内的所有子目录（如 images）复制到 dist 根目录
        shutil.copytree(STATIC_DIR, OUTPUT_DIR, dirs_exist_ok=True)
        print(f"Success: Copied static files to {OUTPUT_DIR}")

    # 4. 读取 HTML 模板
    try:
        index_tpl = open(os.path.join(TEMPLATES_DIR, 'index.html'), encoding='utf-8').read()
        article_tpl = open(os.path.join(TEMPLATES_DIR, 'article.html'), encoding='utf-8').read()
    except Exception as e:
        print(f"Error: Templates not found. {e}")
        return

    # 5. 处理所有 Markdown 文章
    article_list = []
    if os.path.exists(ARTICLES_DIR):
        for filename in sorted(os.listdir(ARTICLES_DIR), reverse=True):
            if filename.endswith('.md'):
                path = os.path.join(ARTICLES_DIR, filename)
                with open(path, 'r', encoding='utf-8') as f:
                    raw_content = f.read()
                
                # 分离标题和内容
                lines = raw_content.split('\n')
                title = lines[0].lstrip('#').strip()
                body = '\n'.join(lines[1:])
                
                # 转换 Markdown (开启 extra 扩展以支持更多格式)
                html_body = markdown.markdown(body, extensions=['extra', 'codehilite'])

                # 渲染单篇文章页
                slug = filename.replace('.md', '')
                rendered_article = article_tpl.replace('{{ARTICLE_TITLE}}', title)
                rendered_article = rendered_article.replace('{{CONTENT}}', html_body)
                rendered_article = rendered_article.replace('{{SITE_TITLE}}', SITE_TITLE)
                rendered_article = rendered_article.replace('{{BASE_URL}}', BASE_URL)

                # 写入文章文件
                output_path = os.path.join(OUTPUT_DIR, 'articles', f'{slug}.html')
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(rendered_article)
                
                article_list.append({'title': title, 'url': f'/articles/{slug}.html'})
                print(f"Rendered: {title}")

    # 6. 渲染首页索引
    links_html = ""
    for item in article_list:
        links_html += f'<li><a href="{item["url"]}">{item["title"]}</a></li>'
    
    rendered_index = index_tpl.replace('{{ARTICLE_LIST}}', links_html)
    rendered_index = rendered_index.replace('{{SITE_TITLE}}', SITE_TITLE)
    rendered_index = rendered_index.replace('{{SITE_DESCRIPTION}}', SITE_DESCRIPTION)

    with open(os.path.join(OUTPUT_DIR, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(rendered_index)

    print(f"Build Complete! All files are in: {OUTPUT_DIR}")

if __name__ == "__main__":
    build()
