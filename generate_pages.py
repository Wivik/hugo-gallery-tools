#!/usr/bin/env python3

import argparse
from datetime import datetime, timezone
import os
import mimetypes
import jinja2

# mission : generate _index.md pages for Hugo Gallery
# run it from the images directory
# license GPL v2

## args

parser = argparse.ArgumentParser()
parser.add_argument(dest='path', action='store', help='Pictures path to generate _index.md')
parser.add_argument('-f', '--force', dest='force', action='store_true', default=False, help="Replace existing _index.md files")
args = parser.parse_args()

force = args.force
path = args.path

def deployTemplate(path, data):
    """deploy templatized _index.md file

    Args:
        path (str): template destination
        data (dict): data for template filling
    """
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader('./')
    )
    try:
        index_template = env.get_template('_index.md.j2')
    except jinja2.TemplateNotFound as err:
        print("Template "+ err +" not found")
        return 1

    render_template = index_template.render(title=data['title'], album_thumb=data['albumthumb'], resources=data['resources'])
    with open(os.path.join(path, '_index.md'), 'w') as file:
        file.write(render_template)
    file.close()

def main():
    """
        Main function
    """
    print("List all pictures from "+ path +" directory")
    pictures = sorted(os.listdir(os.path.join('./assets', path)))

    album_title = os.path.basename(path)
    print(album_title)

    date_now = datetime.now().replace(tzinfo=timezone.utc).replace(microsecond=0).isoformat()
    print(date_now)

    album_thumb=os.path.join(path, pictures[0])
    print(album_thumb)
    
    pictures_with_path = []
    for picture in pictures:
        print(os.path.join(path, picture))
        pictures_with_path.append(
            {
                "src": os.path.join(path, picture)
            }
        )
    print(pictures_with_path)

    index_file= {
            "title": album_title,
            "date": date_now,
            "albumthumb": album_thumb,
            "resources": pictures_with_path
        }


    print(index_file)
    print("Create directories "+os.path.join('./content', path))
    os.makedirs(os.path.join('./content', path))
    deployTemplate(os.path.join('./content', path), index_file)



if __name__ == "__main__":
    main()


