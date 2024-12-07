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
    # Get up to 6 posts
    entries = feed.entries[:6]
    
    # Create HTML for each post
    for entry in entries:
        # Clean description
        description = re.sub('<[^<]+?>', '', entry.description)
        description = description[:150] + '...' if len(description) > 150 else description
        
        # Create post HTML
        post_html = f'''<div style="flex: 1; min-width: 300px; background-color: #1a1b27; border: 1px solid #2F81F7; border-radius: 8px; padding: 24px;">
            <h3 style="margin: 0 0 16px 0;">
                <a href="{entry.link.split('?')[0]}" style="color: #2F81F7; text-decoration: none; font-size: 24px;">{entry.title}</a>
            </h3>
            <p style="color: #a0aec0; margin: 16px 0;">{description}</p>
            <ul style="list-style: none; padding: 0; margin: 16px 0;">
                <li style="margin-bottom: 8px; color: #ffffff;">
                    <span style="display: inline-block; background-color: #2F81F7; padding: 4px 8px; border-radius: 4px; margin-right: 8px;">
                        Published
                    </span>
                    {parsedate_to_datetime(entry.published).strftime('%b %d, %Y')}
                </li>
            </ul>
            <div style="margin-top: 16px;">
                <a href="{entry.link.split('?')[0]}" style="display: inline-block; padding: 8px 16px; background-color: #2F81F7; color: white; text-decoration: none; border-radius: 4px;">Read Article</a>
            </div>
        </div>'''
        posts.append(post_html)
    
    # Ensure even number of posts for grid layout
    if len(posts) % 2 != 0:
        posts.append('''<div style="flex: 1; min-width: 300px;"></div>''')  # Empty div for grid alignment
    
    # Create pairs of posts
    pairs = []
    for i in range(0, len(posts), 2):
        pair = f'''<div style="display: flex; gap: 20px; width: 100%;">
            {posts[i]}
            {posts[i+1] if i+1 < len(posts) else ''}
        </div>'''
        pairs.append(pair)
    
    return '\n'.join(pairs)

def update_readme():
    with open('README.md', 'r', encoding='utf-8') as file:
        content = file.read()
    
    blog_posts = get_medium_posts()
    
    new_section = f'''<!-- BLOG-POST-LIST:START -->
<div align="center" style="margin: 40px auto; max-width: 1200px; padding: 0 20px;">
    <h2 style="color: #2F81F7; margin-bottom: 30px; display: flex; align-items: center; justify-content: center; gap: 15px;">
        <img src="https://raw.githubusercontent.com/Tarikul-Islam-Anik/Animated-Fluent-Emojis/master/Emojis/Objects/Open%20Book.png" alt="📚" width="32" height="32">
        Latest Articles
    </h2>
    <div style="display: flex; flex-direction: column; gap: 20px; width: 100%;">
        {blog_posts}
    </div>
    <div style="margin-top: 30px;">
        <a href="https://medium.com/@TheToriqul" style="display: inline-block; padding: 12px 24px; background-color: #2F81F7; color: white; text-decoration: none; border-radius: 8px; font-weight: 600; transition: background-color 0.3s;">
            View All Articles on Medium
        </a>
    </div>
</div>
<!-- BLOG-POST-LIST:END -->'''
    
    pattern = r"<!-- BLOG-POST-LIST:START -->.*?<!-- BLOG-POST-LIST:END -->"
    updated_content = re.sub(pattern, new_section, content, flags=re.DOTALL)
    
    with open('README.md', 'w', encoding='utf-8') as file:
        file.write(updated_content)

if __name__ == "__main__":
    update_readme()