import feedparser
import os
import re
from datetime import datetime
from email.utils import parsedate_to_datetime

def convert_tag_to_badge(tag):
    """Convert Medium tags to badges matching tech stack style"""
    tag_mappings = {
        'aws': ('AWS', '232F3E', 'amazonaws'),
        'kubernetes': ('Kubernetes', '326CE5', 'kubernetes'),
        'docker': ('Docker', '2496ED', 'docker'),
        'devops': ('DevOps', '2088FF', 'githubactions'),
        'cloud': ('Cloud', '4285F4', 'googlecloud'),
        'python': ('Python', '3776AB', 'python'),
        'terraform': ('Terraform', '7B42BC', 'terraform'),
        'nodejs': ('Node.js', '339933', 'node.js'),
        'javascript': ('JavaScript', 'F7DF1E', 'javascript'),
        'automation': ('Automation', '2088FF', 'githubactions'),
        'linux': ('Linux', 'FCC624', 'linux'),
        'ansible': ('Ansible', 'EE0000', 'ansible'),
        'cicd': ('CI/CD', '2088FF', 'githubactions'),
        'git': ('Git', 'F05032', 'git'),
        'microservices': ('Microservices', '326CE5', 'kubernetes'),
        'security': ('Security', 'FF0000', 'shieldsdotio'),
        'monitoring': ('Monitoring', 'E6522C', 'prometheus')
    }
    
    tag = tag.lower().replace(' ', '-')
    if tag in tag_mappings:
        name, color, icon = tag_mappings[tag]
        return f'<img src="https://img.shields.io/badge/{name}-{color}?style=for-the-badge&logo={icon}&logoColor=white"/>'
    return None

def get_medium_posts():
    username = os.getenv('MEDIUM_USERNAME', '@TheToriqul')
    feed_url = f'https://medium.com/feed/{username}'
    feed = feedparser.parse(feed_url)
    
    entries = feed.entries[:2]
    
    def format_post(entry):
    # Get only tech-related tags and limit to top 3
    all_tags = [tag['term'] for tag in entry.get('tags', [])]
    tech_badges = [badge for badge in map(convert_tag_to_badge, all_tags) if badge is not None][:3]
    # If no tags, add a placeholder badge
    tag_section = '\n          '.join(tech_badges) if tech_badges else '<img src="https://img.shields.io/badge/Article-2F81F7?style=for-the-badge&logo=medium&logoColor=white"/>'
    
    return {
        'title': entry.title,
        'desc': re.sub('<[^<]+?>', '', entry.description)[:150] + '...',
        'url': entry.link.split('?')[0],
        'date': parsedate_to_datetime(entry.published).strftime('%b_%Y'),
        'tags': tag_section
    }
    
    posts = [format_post(entry) for entry in entries]
    
    posts_html = '''
## 📝 Latest Blog Posts

<div align="center">
  <table>
    <tr>
      <td align="center" width="50%">
        <h3>{title}</h3>
        <p align="justify">{desc}</p>
        <p>
          <img src="https://img.shields.io/badge/Published-{date}-00C853?style=flat&logo=medium"/>
          <img src="https://img.shields.io/badge/Read_Time-10_min-2F81F7?style=flat"/>
        </p>
        <p>
          {tags}
        </p>
        <a href="{url}">
          <img src="https://img.shields.io/badge/Read_Article-2F81F7?style=for-the-badge&logo=medium"/>
        </a>
      </td>'''.format(**posts[0])

    if len(posts) > 1:
        posts_html += '''
      <td align="center" width="50%">
        <h3>{title}</h3>
        <p align="justify">{desc}</p>
        <p>
          <img src="https://img.shields.io/badge/Published-{date}-00C853?style=flat&logo=medium"/>
          <img src="https://img.shields.io/badge/Read_Time-8_min-2F81F7?style=flat"/>
        </p>
        <p>
          {tags}
        </p>
        <a href="{url}">
          <img src="https://img.shields.io/badge/Read_Article-2F81F7?style=for-the-badge&logo=medium"/>
        </a>
      </td>'''.format(**posts[1])

    posts_html += '''
    </tr>
  </table>

  <p align="center">
    <a href="https://medium.com/@TheToriqul">
      <img src="https://img.shields.io/badge/MORE_ON_MEDIUM-2F81F7?style=for-the-badge&logo=medium&logoColor=white"/>
    </a>
  </p>
</div>'''

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
