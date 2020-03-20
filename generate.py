#!/usr/bin/env python3

# generate site from static pages, loosely inspired by Jekyll
# run like this:
#   ./generate.py test/source output
# the generated `output` should be the same as `test/expected_output`

import os
import sys
import logging
import jinja2
import json

log = logging.getLogger(__name__)


def list_files(folder_path):
    # takes a folder path and iterates over rst files
    for name in os.listdir(folder_path):
        base, ext = os.path.splitext(name)
        if ext != '.rst':
            continue
        yield (os.path.join(folder_path, name), base)

def read_file(file_path):
    # takes a file at given path, returning the content and  metadata for template
    with open(file_path, 'r') as f:
        raw_metadata = ""
        for line in f:
            if line.strip() == '---':
                break
            raw_metadata += line
        content = ""
        for line in f:
            content += line
    return json.loads(raw_metadata), content

def write_output(output_path, name, html):
    if not os.path.isdir(output_path):
        os.mkdir(output_path)
    with open(os.path.join(output_path, name + '.html'), 'w') as f:
        f.write(html)

def generate_site(folder_path, output_path):
    # creates a jinja environment and generates the site using the template
    log.info("Generating site from %r", folder_path)
    jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(
        os.path.join(folder_path, 'layout')))
    for file_path, name in list_files(folder_path):
        metadata, content = read_file(file_path)
        template_name = metadata['layout']
        template = jinja_env.get_template(template_name)
        data = dict(metadata, content=content)
        html = template.render(**data)
        write_output(output_path, name, html)
        log.info("Writing %r with template %r", name, template_name)


def main():
    if len(sys.argv) < 3:
        print("Run like this: ./generate.py test/source output")
        sys.exit()

    generate_site(sys.argv[1], sys.argv[2])


if __name__ == '__main__':
    logging.basicConfig()
    main()
