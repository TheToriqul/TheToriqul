import feedparser
import os
import re
from datetime import datetime
from email.utils import parsedate_to_datetime

def get_medium_posts():
    username = os.getenv('MEDIUM_USERNAME', '@TheToriqul')
    feed_url = f'https://medium.com/feed/{username}'
    feed = feedparser.parse(feed_url)
    
    # Get up to 2 posts (for simplicity and matching the project layout)
    entries = feed.entries[:2]
    
    # Create GitHub-flavored markdown table
    posts_html = '''
## 📝 Latest Blog Posts

<div align="center">
  <table>
    <tr>
      <td align="center" width="50%">
        <h3>{title1}</h3>
        <p align="justify">{desc1}</p>
        <p>
          <img src="https://img.shields.io/badge/Published-{date1}-00C853?style=flat&logo=medium"/>
          <img src="https://img.shields.io/badge/Read_Time-10_min-2F81F7?style=flat"/>
        </p>
        <a href="{url1}">
          <img src="https://img.shields.io/badge/Read_Article-2F81F7?style=for-the-badge&logo=medium"/>
        </a>
      </td>
      <td align="center" width="50%">
        <h3>{title2}</h3>
        <p align="justify">{desc2}</p>
        <p>
          <img src="https://img.shields.io/badge/Published-{date2}-00C853?style=flat&logo=medium"/>
          <img src="https://img.shields.io/badge/Read_Time-8_min-2F81F7?style=flat"/>
        </p>
        <a href="{url2}">
          <img src="https://img.shields.io/badge/Read_Article-2F81F7?style=for-the-badge&logo=medium"/>
        </a>
      </td>
    </tr>
  </table>

  <p align="center">
    <a href="https://medium.com/@TheToriqul">
      <img src="https://img.shields.io/badge/MORE_ON_MEDIUM-2F81F7?style=for-the-badge&logo=medium&logoColor=white"/>
    </a>
  </p>
</div>'''.format(
        title1=entries[0].title,
        desc1=re.sub('<[^<]+?>', '', entries[0].description)[:150] + '...',
        url1=entries[0].link.split('?')[0],
        date1=parsedate_to_datetime(entries[0].published).strftime('%b_%Y'),
        title2=entries[1].title,
        desc2=re.sub('<[^<]+?>', '', entries[1].description)[:150] + '...',
        url2=entries[1].link.split('?')[0],
        date2=parsedate_to_datetime(entries[1].published).strftime('%b_%Y')
    )
    
    return posts_html

def update_readme():
    with open('README.md', 'r', encoding='utf-8') as file:
        content = file.read()
    
    blog_posts = get_medium_posts()
    
    new_section = f'''<!-- BLOG-POST-LIST:START -->
{blog_posts}
<!-- BLOG-POST-LIST:END -->'''
    
    pattern = r"<!-- BLOG-POST-LIST:START -->.*?<!-- BLOG-POST-LIST:END -->"
    updated_content = re.sub(pattern, new_section, content, flags=re.DOTALL)
    
    with open('README.md', 'w', encoding='utf-8') as file:
        file.write(updated_content)

if __name__ == "__main__":
    update_readme()