from django.shortcuts import render
from markdown2 import markdown
from . import util
from django.shortcuts import render, redirect
from django import forms
import random
class newpageform(forms.Form):
    page=forms.CharField(label="new page")

def entry(request, title):
    content = util.get_entry(title)  
    if content is None:
        return render(request, "encyclopedia/error.html", {
            "message": f"The requested page '{title}' was not found."
        })

    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": markdown(content) 
    })
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

#search
def search(request):
    query = request.GET.get("q", "").lower()  # Get search query from user input
    entries = util.list_entries()  # Get all available encyclopedia entries
    results = [entry for entry in entries if query in entry.lower()]  # Find partial matches

    # If there's an exact match, redirect to that entry
    if len(results) == 1 and results[0].lower() == query:
        return redirect("entry", title=results[0])

    # Otherwise, show search results
    return render(request, "encyclopedia/search.html", {
        "query": query,
        "results": results
    }) 

def new_page(request):
    if request.method == "POST":
        title = request.POST.get("title").strip()  # Get title from form
        content = request.POST.get("content").strip()  # Get content from form

        # Check if the entry already exists
        if util.get_entry(title) is not None:
            return render(request, "encyclopedia/new_page.html", {
                "error": f"An entry with the title '{title}' already exists.",
                "title": title,
                "content": content
            })

        # Save the new entry and redirect to the new page
        util.save_entry(title, content)
        return redirect("entry", title=title)

    return render(request, "encyclopedia/new_page.html")

#edit page
from django.shortcuts import render, redirect
from . import util

def edit_page(request, title):
    # Get the current content of the entry
    content = util.get_entry1(title)

    # If the entry doesn't exist, show an error page
    if content is None:
        return render(request, "encyclopedia/error.html", {"message": "Page not found."})

    if request.method == "POST":
        updated_content = request.POST.get("content").strip()  # Get updated content
        util.save_entry(title, updated_content)  # Save the changes
        return redirect("entry", title=title)  # Redirect back to the updated page

    return render(request, "encyclopedia/edit_page.html", {
        "title": title,
        "content": content
    })

#random
def random_page(request):
    entries = util.list_entries()  # Get all available entries
    if not entries:  # If no entries exist, redirect to home
        return redirect("index")

    random_title = random.choice(entries)  # Pick a random entry
    return redirect("entry", title=random_title)  # Redirect to that entry