import feedparser
import os
import re

def get_medium_posts():
    username = os.getenv('MEDIUM_USERNAME', '@TheToriqul')
    feed_url = f'https://medium.com/feed/{username}'
    feed = feedparser.parse(feed_url)
    
    posts = []
    for entry in feed.entries[:3]:  # Get latest 3 posts
        title = entry.title
        url = entry.link.split('?')[0]  # Remove tracking parameters
        posts.append(f"* [{title}]({url})")
    
    return '\n'.join(posts)

def update_readme():
    with open('README.md', 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Get the new blog posts content
    blog_posts = get_medium_posts()
    
    # Create the new section with proper spacing
    new_section = f"<!-- BLOG-POST-LIST:START -->\n{blog_posts}\n<!-- BLOG-POST-LIST:END -->"
    
    # Replace the old section with new content
    pattern = r"<!-- BLOG-POST-LIST:START -->.*?<!-- BLOG-POST-LIST:END -->"
    updated_content = re.sub(pattern, new_section, content, flags=re.DOTALL)
    
    with open('README.md', 'w', encoding='utf-8') as file:
        file.write(updated_content)

if __name__ == "__main__":
    update_readme()