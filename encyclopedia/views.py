from django.shortcuts import render

from django.http import HttpResponseRedirect
from django.urls import reverse

from . import util

import markdown2
import re
import html2markdown
from bs4 import BeautifulSoup
import random


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):

	if util.get_entry(title):
		context = {
			"content": markdown2.markdown(util.get_entry(title)),
			"title": title,
		}
		return render(request, "encyclopedia/entry.html", context)
	else:
		return render(request, "encyclopedia/error.html")
		
def search(request):
	searches = request.GET["q"]
	if util.get_entry(searches):
		results = markdown2.markdown(util.get_entry(searches))
		return render(request, "encyclopedia/entry.html", {
			"content": results,} )
	else:
		entries = util.list_entries()
		match = []
		for entry in entries:
			if entry.lower().startswith(searches.lower()):
				match.append(entry)
		context = {
			"entries": entries,
			"search": searches,
			"matches": match,
		}
		
		return render(request,"encyclopedia/search.html", context)

def new_entry(request):
	if request.method == "POST":
		title = request.POST["title"]
		content = request.POST["content"]

		util.save_entry(title, content)
		return HttpResponseRedirect(reverse(entry, args=(title,)))

	return render(request, "encyclopedia/new.html")

def edit_entry(request, title):
	if request.method == "POST":
		content = request.POST["content"]
		markdown_content = html2markdown.convert(content)
		util.save_entry(title, markdown_content)
		return HttpResponseRedirect(reverse(entry, args=(title,)))
	
	if util.get_entry(title):
		info = markdown2.markdown(util.get_entry(title))
		soup = BeautifulSoup(info, 'html.parser')
		soup.h1.decompose()
		
		context = {
			"title": title,
			"info": str(soup),
		}
		return render(request, "encyclopedia/edit.html", context)
	else:
		return render(request, "encyclopedia/error.html")

def random_pick(request):
	entries = util.list_entries()
	pick = random.choice(entries)
	return HttpResponseRedirect(reverse(entry, args=(pick,)))
