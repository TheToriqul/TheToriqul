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
    for entry in feed.entries[:6]:  # Get 6 latest posts
        title = entry.title
        url = entry.link.split('?')[0]
        date = parsedate_to_datetime(entry.published).strftime('%b %d, %Y')
        
        # Get the first 150 characters of the description/content
        description = re.sub('<[^<]+?>', '', entry.description)
        description = description[:150] + '...' if len(description) > 150 else description
        
        # Create card HTML
        post_html = f'''<div class="blog-card" style="width: calc(50% - 20px); min-width: 300px; background-color: #1a1b27; border-radius: 12px; border: 1px solid #2F81F7; overflow: hidden; margin: 10px;">
            <div style="padding: 20px;">
                <div style="display: flex; align-items: center; margin-bottom: 12px;">
                    <img src="https://raw.githubusercontent.com/Tarikul-Islam-Anik/Animated-Fluent-Emojis/master/Emojis/Objects/Memo.png" alt="📝" width="24" height="24" style="margin-right: 10px;">
                    <span style="color: #2F81F7; font-size: 14px;">{date}</span>
                </div>
                <h3 style="color: #ffffff; margin: 0 0 12px 0; font-size: 16px; line-height: 1.4;">
                    <a href="{url}" style="color: inherit; text-decoration: none; font-weight: 600;">{title}</a>
                </h3>
                <p style="color: #a0aec0; font-size: 14px; line-height: 1.6; margin: 0 0 15px 0;">{description}</p>
                <a href="{url}" style="display: inline-block; padding: 8px 16px; background-color: #2F81F7; color: white; text-decoration: none; border-radius: 6px; font-size: 14px; transition: background-color 0.3s;">Read More</a>
            </div>
        </div>'''
        posts.append(post_html)
    
    return '\n'.join(posts)

def update_readme():
    with open('README.md', 'r', encoding='utf-8') as file:
        content = file.read()
    
    blog_posts = get_medium_posts()
    
    new_section = f'''<!-- BLOG-POST-LIST:START -->
<div align="center" style="margin: 40px 0;">
    <div style="max-width: 1200px; margin: 0 auto;">
        <h2 style="color: #2F81F7; margin-bottom: 30px; display: flex; align-items: center; justify-content: center; gap: 15px;">
            <img src="https://raw.githubusercontent.com/Tarikul-Islam-Anik/Animated-Fluent-Emojis/master/Emojis/Objects/Open%20Book.png" alt="📚" width="32" height="32">
            Latest Articles
        </h2>
        <div style="display: flex; flex-wrap: wrap; justify-content: center; gap: 20px; margin: 0 auto;">
            {blog_posts}
        </div>
        <div style="margin-top: 30px;">
            <a href="https://medium.com/@TheToriqul" style="display: inline-block; padding: 12px 24px; background-color: #2F81F7; color: white; text-decoration: none; border-radius: 8px; font-weight: 600; transition: background-color 0.3s;">
                View All Articles on Medium
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