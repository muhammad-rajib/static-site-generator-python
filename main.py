import os
from datetime import datetime
from jinja2 import Environment, PackageLoader
from markdown2 import markdown


content_dir = 'content'
template_dir = 'templates'
content_file_name = 'awesome.md'
POSTS = {}  # parse and collect all markdown file


def generate_index():
    # Generate Index
    global POSTS
    for markdown_file in os.listdir(content_dir):
        file_path = os.path.join('content', markdown_file)

        with open(file_path, 'r') as file:
            parsed_content = markdown(file.read(), extras=['metadata'])
            POSTS[markdown_file] = parsed_content

    # sort post datewise
    POSTS = {
        post: POSTS[post] for post in sorted(POSTS, key=lambda post: datetime.strptime(POSTS[post].metadata['date'], '%Y-%m-%d  %H:%M'), reverse=True)
    }

    env = Environment(loader=PackageLoader('main', 'templates'))
    index_template = env.get_template('index.html')
    post_data = [POSTS[post].metadata for post in POSTS]
    index_template_content = index_template.render(posts=post_data)

    with open('prepared_content/index.html', 'w') as file:
        file.write(index_template_content)


def generate_post():
    # Generate Post Content
    global POSTS

    for post in POSTS:
        metadata = POSTS[post].metadata

        post_data = {
            'content': POSTS[post],
            'title': metadata['title'],
            'date': metadata['date'],
        }

        env = Environment(loader=PackageLoader('main', 'templates'))
        post_template = env.get_template('layout.html')
        post_html_content = post_template.render(post=post_data)

        post_file_path = 'prepared_content/posts/{slug}/index.html'.format(
            slug=metadata['slug'])

        os.makedirs(os.path.dirname(post_file_path), exist_ok=True)
        with open(post_file_path, 'w') as file:
            file.write(post_html_content)


if __name__ == '__main__':
    # generate index
    generate_index()
    # generate post
    generate_post()
