import feedparser
import os
import re

def get_medium_posts():
    username = os.getenv('MEDIUM_USERNAME', '@TheToriqul')
    feed_url = f'https://medium.com/feed/{username}'
    feed = feedparser.parse(feed_url)
    
    posts = []
    for entry in feed.entries[:3]:
        title = entry.title
        url = entry.link.split('?')[0]
        posts.append(f'<div class="blog-post" style="margin-bottom: 10px;">&nbsp;&nbsp;📝 <a href="{url}">{title}</a></div>')
    
    return '\n'.join(posts)

def update_readme():
    with open('README.md', 'r', encoding='utf-8') as file:
        content = file.read()
    
    blog_posts = get_medium_posts()
    
    new_section = f'''<!-- BLOG-POST-LIST:START -->
<div align="left" style="margin-top: 10px;">
{blog_posts}
</div>

<div align="center">
  <a href="https://medium.com/@TheToriqul">
    <img src="https://img.shields.io/badge/READ_MORE_ON_MEDIUM-2F81F7?style=for-the-badge&logo=medium&logoColor=white" alt="Read More on Medium"/>
  </a>
</div>
<!-- BLOG-POST-LIST:END -->'''
    
    pattern = r"<!-- BLOG-POST-LIST:START -->.*?<!-- BLOG-POST-LIST:END -->"
    updated_content = re.sub(pattern, new_section, content, flags=re.DOTALL)
    
    with open('README.md', 'w', encoding='utf-8') as file:
        file.write(updated_content)

if __name__ == "__main__":
    update_readme()