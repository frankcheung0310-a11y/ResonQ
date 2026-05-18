import os
import markdown
import shutil

def build():
    # 1. 强行在当前目录下创建 dist 文件夹
    # 只要这个文件夹出来了，Cloudflare 就能抓到它
    if os.path.exists('dist'):
        shutil.rmtree('dist')
    os.makedirs('dist/articles', exist_ok=True)

    # 2. 搬运图片 (这是你之前没有的功能)
    # 它会把你 static 文件夹里的所有东西拷贝到 dist 里
    if os.path.exists('static'):
        shutil.copytree('static', 'dist', dirs_exist_ok=True)
        print("✓ Images and static files copied.")

    # 3. 读取你的模板
    with open('templates/index.html', 'r', encoding='utf-8') as f:
        index_tpl = f.read()
    with open('templates/article.html', 'r', encoding='utf-8') as f:
        article_tpl = f.read()

    # 4. 转换你的所有 Markdown 文章
    article_links = []
    for filename in os.listdir('articles'):
        if filename.endswith('.md'):
            with open(f'articles/{filename}', 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 获取第一行当标题
            title = content.split('\n')[0].lstrip('# ')
            html_body = markdown.markdown(content, extensions=['extra'])
            
            slug = filename.replace('.md', '')
            # 填入文章模板
            full_html = article_tpl.replace('{{ARTICLE_TITLE}}', title).replace('{{CONTENT}}', html_body)
            
            # 保存到 dist/articles/ 目录下
            with open(f'dist/articles/{slug}.html', 'w', encoding='utf-8') as f:
                f.write(full_html)
            
            article_links.append(f'<li><a href="/articles/{slug}.html">{title}</a></li>')

    # 5. 生成首页
    final_index = index_tpl.replace('{{ARTICLE_LIST}}', '\n'.join(article_links))
    with open('dist/index.html', 'w', encoding='utf-8') as f:
        f.write(final_index)
    
    print("Build Complete! 'dist' folder is ready.")

if __name__ == "__main__":
    build()
