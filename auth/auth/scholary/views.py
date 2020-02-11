from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import scholarly


def search(request):
    if request.method == 'POST':
        author_name = request.POST.get('authorname')
        numbers_list = range(1, 1000)
        page = request.GET.get('page', 1)
        paginator = Paginator(numbers_list, 10)
        try:
            search_query = next(scholarly.search_author(author_name), 1).fill()
            numbers = paginator.page(page)
            mycontext = {
                'filled': search_query._filled,
                'affiliation': search_query.affiliation,
                'email': search_query.email,
                'id': search_query.id,
                'interests': search_query.interests,
                'citedby': search_query.citedby,
                # 'interests' : search_query.interests,
                'name': search_query.name,
                'url_picture': search_query.url_picture,
                'publications': search_query.publications,
                'total_publications': len(search_query.publications),
                'l' : [i for i in range(len(search_query.publications))],
                'publication_title': [(search_query.publications[i].bib['title']) for i in range(20)],
                #'publication_coauthor': [(search_query.publications.bib['author']) for i in range(len(search_query.publications))],
                #'publication_citedby': [(search_query.publications[i].bib['citedby']) for i in range(20)],
                #'publication_journal': [(search_query.publications.bib['journal']) for i in range(len(search_query.publications))],
                'numbers' : numbers
            }
            return render(request, 'scholary/author_search_result.html', mycontext)
        except PageNotAnInteger:
            numbers = paginator.page(1)
            return render(request, 'scholary/author_search_result.html', {'numbers': numbers})
        except EmptyPage:
            numbers = paginator.page(paginator.num_pages)
            return render(request, 'scholarly/author_search_result.html', {'numbers': numbers})
    else:
        return render(request, 'scholary/author_search.html', {})


def publication_search(request):
    if request.method == 'POST':
        publication = request.POST.get('publication')
        numbers_list = range(1, 1000)
        page = request.GET.get('page', 1)
        paginator = Paginator(numbers_list, 10)
        try:
            search_query = next(scholarly.search_pubs_query(publication), 1).fill()
            numbers = paginator.page(page)
            #search_query = list(scholarly.search_pubs_query(publication))
            #search_query = search_query[0].fill()
            mycontext = {
                'filled': search_query._filled,
                'abstract': search_query.bib['abstract'],
                'author': search_query.bib['author'],
                'title': search_query.bib['title'],
                'url': search_query.bib['url'],
                'journal': search_query.bib['journal'],
                'publisher': search_query.bib['publisher'],
                'date': search_query.bib['year'],
                'scholarcitedby': search_query.id_scholarcitedby,
                #'citation_per_year': search_query.cites_per_year,
                'citedby': search_query.citedby,
                'url_scholarbib': search_query.url_scholarbib,
                'source': search_query.source,
                'numbers': numbers

            }
            return render(request, 'scholary/publication_search_result.html', mycontext)
        except PageNotAnInteger:
            numbers = paginator.page(1)
            return render(request, 'scholary/publication_search_result.html', {'numbers': numbers})
        except EmptyPage:
            numbers = paginator.page(paginator.num_pages)
            return render(request, 'scholarly/publication_search_result.html', {'numbers': numbers})
        # close(scholarly.search_pubs_query(publication)
    else:
        return render(request, 'scholary/publication_search.html', {})


# def keyword_search(request, *args, **kwargs):
#     if request.method == 'POST':
#         keyword = request.POST.get('keyword')
#         try:
#             search_query = next(scholarly.search_keyword(keyword),1)
#             mycontext = {
#             'filled'  : search_query._filled,
#             'affiliation': search_query.affiliation,
#             'name'  : search_query.name,
#             'id'   : search_query.bib['id'],
#             'url_picture'     : search_query['url_picture'],
#             'citedby' : search_query.citedby,
#             'email' : search_query.email,
#             'interests' : search_query.interests
#         }
#             return render(request, 'scholary/keyword_search_result.html', mycontext)
#         except Exception:
#             print(Exception)
#             return HttpResponse('Nothing found at the moment')
#         #close(scholarly.search_pubs_query(publication)
#     else:
#         return render(request, 'scholary/keyword_search.html', {})
