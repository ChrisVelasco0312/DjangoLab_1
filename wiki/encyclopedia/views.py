from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
import markdown2
from django import forms
from . import util
import random


class NewSearchForm(forms.Form):
    search = forms.CharField(label="Search")


form = NewSearchForm()


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        'randomEntry': randomEntry(),
        "form": form
    })


def entry(request, entry):
    if util.get_entry(entry) == None:
        # return HttpResponse(f'The entry {entry} was not found')
        return render(request, 'encyclopedia/404.html')
    else:
        html = markdown2.markdown(util.get_entry(entry))
        return render(request, 'encyclopedia/entry.html', {
            # markdown2.markdown(util.get_entry(entry)),
            'content': html,
            'entry': entry,
            "form": form,
        })


def search(request):
    newForm = NewSearchForm(request.GET)
    entryList = util.list_entries()
    newForm.is_valid()
    search = newForm.cleaned_data['search']

    newSearchList = list(
        filter(lambda x: search.capitalize() in x, entryList))

    print(newSearchList)

    searchContext = {
        'search': search,
        'entries': entryList,
        'form': form,
        'newSearchList': newSearchList
    }
    if search in entryList:
        return entry(request, search)
    else:
        return render(request, 'encyclopedia/search.html', searchContext)


def create(request):
    title = request.POST.get('title')
    content = request.POST.get('content')
    if content != None:
        util.save_entry(title, content)
        return entry(request, title)
    return render(request, 'encyclopedia/create.html')


def edit(request, entry):
    content = util.get_entry(entry)

    return render(request, 'encyclopedia/edit.html', {
        'entry': entry,
        'content': content,
    })


def randomEntry():
    entryList = util.list_entries()
    ranEntry = random.choice(entryList)
    return ranEntry
