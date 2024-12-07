import feedparser
import os
import re
from datetime import datetime
from email.utils import parsedate_to_datetime

def get_medium_posts():
    username = os.getenv('MEDIUM_USERNAME', '@TheToriqul')
    feed_url = f'https://medium.com/feed/{username}'
    feed = feedparser.parse(feed_url)
    
    posts = []
    for entry in feed.entries[:3]:
        title = entry.title
        url = entry.link.split('?')[0]
        # Using email.utils to parse the date correctly
        date = parsedate_to_datetime(entry.published).strftime('%b %d, %Y')
        
        post_html = f'''<div class="blog-post" style="margin-bottom: 20px; padding: 15px; background-color: #1a1b27; border-radius: 8px; border: 1px solid #2F81F7;">
            <div style="display: flex; align-items: center; margin-bottom: 8px;">
                <img src="https://raw.githubusercontent.com/Tarikul-Islam-Anik/Animated-Fluent-Emojis/master/Emojis/Objects/Memo.png" alt="📝" width="20" height="20" style="margin-right: 8px;">
                <span style="color: #2F81F7; font-size: 12px;">{date}</span>
            </div>
            <a href="{url}" style="color: #ffffff; text-decoration: none; font-size: 14px; font-weight: 500; display: block; margin-left: 28px;">{title}</a>
        </div>'''
        posts.append(post_html)
    
    return '\n'.join(posts)

def update_readme():
    with open('README.md', 'r', encoding='utf-8') as file:
        content = file.read()
    
    blog_posts = get_medium_posts()
    
    new_section = f'''<!-- BLOG-POST-LIST:START -->
<div align="center" style="margin: 20px 0;">
    <div style="max-width: 800px; margin: 0 auto;">
        <h3 style="color: #2F81F7; margin-bottom: 20px; display: flex; align-items: center; justify-content: center; gap: 10px;">
            <img src="https://raw.githubusercontent.com/Tarikul-Islam-Anik/Animated-Fluent-Emojis/master/Emojis/Objects/Open%20Book.png" alt="📚" width="24" height="24">
            Latest Articles
        </h3>
        <div align="left">
            {blog_posts}
        </div>
        <div style="margin-top: 15px;">
            <a href="https://medium.com/@TheToriqul">
                <img src="https://img.shields.io/badge/READ_MORE_ON_MEDIUM-2F81F7?style=for-the-badge&logo=medium&logoColor=white" alt="Read More on Medium"/>
            </a>
        </div>
    </div>
</div>
<!-- BLOG-POST-LIST:END -->'''
    
    pattern = r"<!-- BLOG-POST-LIST:START -->.*?<!-- BLOG-POST-LIST:END -->"
    updated_content = re.sub(pattern, new_section, content, flags=re.DOTALL)
    
    with open('README.md', 'w', encoding='utf-8') as file:
        file.write(updated_content)

if __name__ == "__main__":
    update_readme()