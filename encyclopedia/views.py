from django import forms
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.http import HttpResponse
from django.utils.safestring import mark_safe

from . import util
import random
import markdown2
from markdown2 import Markdown

""" Define classes for search, create and edit page forms """

class SearchForm(forms.Form):

    search = forms.CharField(label="Search", max_length=15)

class CreatePageForm(forms.Form):    

    pagetitle = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Your Title"}))
    pagecontent = forms.CharField(widget=forms.Textarea(attrs={"placeholder": "Your Description"}))

    """ Set up validation error incase title exists (currently not working) """
    def clean_titlename(self):

        check_title = self.cleaned_data['pagetitle']
        check_entry = util.list_entries()

        if check_title in check_entry:
            raise forms.ValidationError('Title already exists try another')        
        else:
            return check_title
        
class EditPageForm(forms.Form):
    
    pagetitle = forms.CharField()
    pagecontent = forms.CharField()
   
    def clean_titlename(self):

        check_title = self.cleaned_data['pagetitle']
        check_entry = util.list_entries()

""" intitialize variables - result for the index page, and search results for search results"""

result = util.list_entries()
searchresult = []

""" index page that presents all the encyclopedia entries """

def index(request):
   
    return render(request, "encyclopedia/index.html", {
        "entries":result,
        "form":SearchForm()
    })

""" Search any title from list of entries """
def search(request):

    if request.method == "POST":
        searchresult.clear()
        form = SearchForm(request.POST)
        allentries = util.list_entries()
        

        if form.is_valid():
            stitle = form.cleaned_data["search"]

            for entry in allentries:
                if stitle.casefold() in entry.casefold():
                    searchresult.append(entry)
            
        return HttpResponseRedirect(reverse("encyclopedia:search"))
        
    return render(request, "encyclopedia/search.html", {
            "results":searchresult,
            "form":SearchForm()
        })

""" Opens title page with content & edit feature when clicked"""

def title(request, name):

    content = util.get_entry(name)

    if content is not None:
        markdowner = Markdown()
        convertcontent = markdowner.convert(content)

    return render(request, "encyclopedia/title.html", {
        "exists": content is not None,
        "name": name,
        "form": SearchForm(),
        "content":convertcontent
    })

""" Create a new entry, returns error when title already exists """

def createpage(request):

    if request.method == "POST":
        createform = CreatePageForm(request.POST)

        if createform.is_valid():
            new_title = createform.cleaned_data["pagetitle"]
            new_content = createform.cleaned_data["pagecontent"]

            check_entry = util.list_entries()

            """ Error message """
            if check_title in check_entry:
                return HttpResponse("Title already exists-" + new_title)
            
            else:
                util.save_entry(new_title, new_content)
                return HttpResponse("Page was created with title " + new_title)


    else:
        return render(request, "encyclopedia/createpage.html", {
            "form":SearchForm(),
            "CreatePageForm":CreatePageForm()

    })

""" edit existing entry """

def editpage(request, name):

    if request.method == "POST":
        editform = EditPageForm(request.POST)

        if editform.is_valid():
            edit_title = editform.cleaned_data["pagetitle"]
            edit_content = editform.cleaned_data["pagecontent"]

            util.save_entry(edit_title, edit_content)

            return HttpResponseRedirect(reverse("encyclopedia:title", args=[edit_title]))
    
    content = util.get_entry(name)

    return render(request, "encyclopedia/editpage.html", {
        "form":SearchForm(),
        "EditPageForm":EditPageForm(),
        "name":name,
        "content":content          
        })

""" redirect to random title name """
def randompage(request):

    randomlist = util.list_entries()
    randomtitle = random.choice(randomlist)
    convertcontent = util.get_entry(randomtitle)

    return render(request, "encyclopedia/title.html", {
        "exists": convertcontent is not None,
        "name": randomtitle,
        "form":SearchForm(),
        "content":convertcontent
    })


    







