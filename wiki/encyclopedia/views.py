from django.shortcuts import render, redirect
from django.http import HttpResponse
import markdown2, random
from django.contrib import messages

from . import util

#display list of entries
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

#convert markdown to html and display entries
def entry_page(request,title):
    entry_content = util.get_entry(title)
    return render(request,"encyclopedia/entry.html",{
                "title": title,
                "value":markdown2.markdown(entry_content) if entry_content else None
    })

#use for search
def search(request):
    entries = util.list_entries()
    query = request.GET.get("q", "")
    for i in entries:
        if i.lower() == query.lower():
            return redirect('wiki:entry', title=query)
        
    for i in entries:
        query_list = [entry for entry in entries if query.lower() in entry.lower() ]
        return render(request,"encyclopedia/search_result.html", {
            "entries": query_list
        })

#random page 
def random_page(request):
    entries = util.list_entries()
    choice = random.choice(entries)

    entry_content = util.get_entry(choice)
    return render(request,"encyclopedia/entry.html",{
        "title" : choice,
        "value": markdown2.markdown(entry_content)
    })

#edit Page
def edit_page(request,title):
    #when the data is submitted to form
    if request.method == "POST":
        content = request.POST.get('textbox','').replace('\r\n','\n').strip() # to remove extra line space we added replace('\r\n', '\n')
        if content:
            util.save_entry(title,content)
            return redirect('wiki:entry',title)


    else:
        #when the edit button is clicked and data is not submitted to form GET Request 
        content = util.get_entry(title)
        return render(request,"encyclopedia/edit.html",{
        "title":title,
        "value": content #no need to convert to html here because this section is for user to edit in markdown format
        })


#new page
def new_page(request):
    if request.method =="POST":
        title = request.POST.get('title_box','').strip()
        content = request.POST.get('blog_box','').strip()

        # # Check if title is empty or already exists
        
        # if not title:  #used require html to eliminate this
        #     messages.error(request, "Title cannot be empty.")
        #     return render(request, 'encyclopedia/new_page.html')

        if title.lower() in [i.lower() for i in util.list_entries()]:
            messages.error(request, f"An entry with the title '{title}' already exists.")
            return render(request, 'encyclopedia/new_page.html')


        # Save the entry
        util.save_entry(title, content)
        messages.success(request, f"The page '{title}' has been successfully created.")
        return redirect('wiki:entry', title=title)


    else:
        return render(request,'encyclopedia/new_page.html')