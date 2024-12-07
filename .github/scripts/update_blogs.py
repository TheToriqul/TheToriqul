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
    # Process posts in pairs
    for i in range(0, min(len(feed.entries), 6), 2):
        post1 = feed.entries[i]
        # Get description and clean HTML tags
        desc1 = re.sub('<[^<]+?>', '', post1.description)
        desc1 = desc1[:150] + '...' if len(desc1) > 150 else desc1
        
        # Create first post card
        card1 = {
            'title': post1.title,
            'url': post1.link.split('?')[0],
            'date': parsedate_to_datetime(post1.published).strftime('%b %d, %Y'),
            'description': desc1
        }
        
        # Get second post if available
        card2 = None
        if i + 1 < len(feed.entries):
            post2 = feed.entries[i + 1]
            desc2 = re.sub('<[^<]+?>', '', post2.description)
            desc2 = desc2[:150] + '...' if len(desc2) > 150 else desc2
            card2 = {
                'title': post2.title,
                'url': post2.link.split('?')[0],
                'date': parsedate_to_datetime(post2.published).strftime('%b %d, %Y'),
                'description': desc2
            }
        
        # Create row HTML with two cards
        row_html = f'''
        <div style="display: flex; justify-content: center; gap: 20px; margin-bottom: 20px;">
            <div style="flex: 1; background-color: #1a1b27; border: 1px solid #2F81F7; border-radius: 8px; padding: 24px; min-width: 300px;">
                <h3 style="margin: 0 0 16px 0;">
                    <a href="{card1['url']}" style="color: #2F81F7; text-decoration: none; font-size: 24px;">{card1['title']}</a>
                </h3>
                <p style="color: #a0aec0; margin: 16px 0;">{card1['description']}</p>
                <ul style="list-style: none; padding: 0; margin: 16px 0;">
                    <li style="margin-bottom: 8px; color: #ffffff;">
                        <span style="display: inline-block; background-color: #2F81F7; padding: 4px 8px; border-radius: 4px; margin-right: 8px;">
                            Published
                        </span>
                        {card1['date']}
                    </li>
                </ul>
                <div style="margin-top: 16px;">
                    <a href="{card1['url']}" style="display: inline-block; padding: 8px 16px; background-color: #2F81F7; color: white; text-decoration: none; border-radius: 4px;">Read Article</a>
                </div>
            </div>'''
        
        if card2:
            row_html += f'''
            <div style="flex: 1; background-color: #1a1b27; border: 1px solid #2F81F7; border-radius: 8px; padding: 24px; min-width: 300px;">
                <h3 style="margin: 0 0 16px 0;">
                    <a href="{card2['url']}" style="color: #2F81F7; text-decoration: none; font-size: 24px;">{card2['title']}</a>
                </h3>
                <p style="color: #a0aec0; margin: 16px 0;">{card2['description']}</p>
                <ul style="list-style: none; padding: 0; margin: 16px 0;">
                    <li style="margin-bottom: 8px; color: #ffffff;">
                        <span style="display: inline-block; background-color: #2F81F7; padding: 4px 8px; border-radius: 4px; margin-right: 8px;">
                            Published
                        </span>
                        {card2['date']}
                    </li>
                </ul>
                <div style="margin-top: 16px;">
                    <a href="{card2['url']}" style="display: inline-block; padding: 8px 16px; background-color: #2F81F7; color: white; text-decoration: none; border-radius: 4px;">Read Article</a>
                </div>
            </div>'''
            
        row_html += '</div>'
        posts.append(row_html)
    
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
        {blog_posts}
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