import re

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
import markdown2
import os


def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))




def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        f = default_storage.open(f"entries/{title}.md")
        return f.read().decode("utf-8")
    except FileNotFoundError:
        return None
def save_entry(title, content):
    """
    Saves an encyclopedia entry with the given title and Markdown content.
    If an existing entry with the same title exists, it is replaced.
    """
    filename = f"entries/{title}.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)

def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title and converts it to HTML.
    Returns None if the entry does not exist.
    """
    try:
        with open(f"entries/{title}.md", "r", encoding="utf-8") as f:
            markdown_content = f.read()  # Read Markdown content
            return markdown2.markdown(markdown_content)  # Convert Markdown to HTML
    except FileNotFoundError:
        return None  # Return None if file doesn't exist
