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
    # Get up to 2 posts (for simplicity and matching the project layout)
    entries = feed.entries[:2]
    
    # Create both cards in a single container
    posts_html = f'''
    <div align="center">
        <table>
            <tr>
                <td width="50%">
                    <h3>
                        <a href="{entries[0].link.split('?')[0]}" style="color: #2F81F7; text-decoration: none;">
                            {entries[0].title}
                        </a>
                    </h3>
                    <p>{entries[0].description[:100].replace('<p>', '').replace('</p>', '')}...</p>
                    <ul>
                        <li>Published on Medium</li>
                        <li>Technical Article</li>
                        <li>Cloud & DevOps</li>
                    </ul>
                    <p>
                        <img src="https://img.shields.io/badge/Status-Published-00C853?style=flat&logo=checkmarx"/>
                        <img src="https://img.shields.io/badge/Date-{parsedate_to_datetime(entries[0].published).strftime('%b_%Y')}-00C853?style=flat"/>
                    </p>
                </td>
                <td width="50%">
                    <h3>
                        <a href="{entries[1].link.split('?')[0]}" style="color: #2F81F7; text-decoration: none;">
                            {entries[1].title}
                        </a>
                    </h3>
                    <p>{entries[1].description[:100].replace('<p>', '').replace('</p>', '')}...</p>
                    <ul>
                        <li>Published on Medium</li>
                        <li>Technical Article</li>
                        <li>Cloud & DevOps</li>
                    </ul>
                    <p>
                        <img src="https://img.shields.io/badge/Status-Published-00C853?style=flat&logo=checkmarx"/>
                        <img src="https://img.shields.io/badge/Date-{parsedate_to_datetime(entries[1].published).strftime('%b_%Y')}-00C853?style=flat"/>
                    </p>
                </td>
            </tr>
        </table>
    </div>'''
    
    return posts_html

def update_readme():
    with open('README.md', 'r', encoding='utf-8') as file:
        content = file.read()
    
    blog_posts = get_medium_posts()
    
    new_section = f'''<!-- BLOG-POST-LIST:START -->
<div align="center">
    <h2>📝 Latest Blog Posts</h2>
    {blog_posts}
    <div style="margin-top: 20px;">
        <a href="https://medium.com/@TheToriqul">
            <img src="https://img.shields.io/badge/READ_MORE_ON_MEDIUM-2F81F7?style=for-the-badge&logo=medium&logoColor=white" alt="Read More on Medium"/>
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