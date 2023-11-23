import difflib
from bs4 import BeautifulSoup

def _find_content_differences(old_file_path, new_file_path, base_url):
    # Read the contents of the old and new HTML files
    with open(old_file_path, 'r') as old_file:
        old_content = old_file.read()

    with open(new_file_path, 'r') as new_file:
        new_content = new_file.read()

    # Find the differences between the old and new content
    old_soup = BeautifulSoup(old_content, 'html.parser')
    new_soup = BeautifulSoup(new_content, 'html.parser')

    diff_tags = []
    for tag in difflib.ndiff(str(old_soup).splitlines(), str(new_soup).splitlines()):
        if tag.startswith('- ') or tag.startswith('+ '):
            diff_tags.append(tag[2:])

    return diff_tags

print(_find_content_differences('main.html','main2.html','main.html'))