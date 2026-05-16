import os
import markdown
import config
import shutil

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
# 自动生成到一个临时目录用于部署
OUTPUT_DIR = os.path.join(PROJECT_DIR, 'public') 
TEMPLATES_DIR = os.path.join(PROJECT_DIR, 'templates')
ARTICLES_DIR = os.path.join(PROJECT_DIR, 'articles')
STATIC_DIR = os.path.join(PROJECT_DIR, 'static')

def build():
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.makedirs(OUTPUT_DIR)

    # 自动处理图片：将 static 下的所有内容复制到输出目录
    if os.path.exists(STATIC_DIR):
        shutil.copytree(STATIC_DIR, OUTPUT_DIR, dirs_exist_ok=True)

    index_template = open(os.path.join(TEMPLATES_DIR, 'index.html'), encoding='utf-8').read()
    article_template = open(os.path.join(TEMPLATES_DIR, 'article.html'), encoding='utf-8').read()

    article_list = []
    if os.path.exists(ARTICLES_DIR):
        for filename in sorted(os.listdir(ARTICLES_DIR), reverse=True):
            if filename.endswith('.md'):
                content = open(os.path.join(ARTICLES_DIR, filename), encoding='utf-8').read()
                lines = content.split('\n')
                title = lines[0].replace('#', '').strip()
                body = '\n'.join(lines[1:])
                html_body = markdown.markdown(body, extensions=['extra'])

                slug = filename.replace('.md', '')
                
                # 填充模板
                page = article_template.replace('{{SITE_TITLE}}', config.SITE_TITLE)
                page = page.replace('{{ARTICLE_TITLE}}', title)
                page = page.replace('{{CONTENT}}', html_body)
                page = page.replace('{{BASE_URL}}', config.BASE_URL)

                os.makedirs(os.path.join(OUTPUT_DIR, 'articles'), exist_ok=True)
                with open(os.path.join(OUTPUT_DIR, 'articles', f'{slug}.html'), 'w', encoding='utf-8') as f:
                    f.write(page)
                
                article_list.append(f'<li><a href="/articles/{slug}.html">{title}</a></li>')

    index_page = index_template.replace('{{ARTICLE_LIST}}', '\n'.join(article_list))
    index_page = index_page.replace('{{SITE_TITLE}}', config.SITE_TITLE)
    index_page = index_page.replace('{{SITE_DESCRIPTION}}', config.SITE_DESCRIPTION)
    
    with open(os.path.join(OUTPUT_DIR, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(index_page)
    print("Build Complete!")

if __name__ == "__main__":
    build()
