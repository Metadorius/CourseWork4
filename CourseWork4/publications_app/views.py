from django.shortcuts import render, redirect
from django.http import HttpResponse
from .docx_generator import generate_docx
from django.templatetags.static import static
from django.views.generic import ListView, DetailView
from .models import *


class AuthorIndexView(ListView):
    model = Author
    context_object_name = 'authors'
    template_name = 'author_list.html'


class AuthorDetailView(DetailView):
    model = Author
    context_object_name = 'author'
    template_name = 'author_details.html'


def generate_report(request, pk):
    context = dict()
    context['content'] = []

    t = Author.objects.get(id=pk)

    context['author'] = f'{t}'.upper()

    context['short_author'] = f'{t.short_name()}'

    for i, w in enumerate(sorted(t.works.all(), key=lambda w: w.get_year()), 1):
        work_info = dict()
        work_info['num'] = i
        work_info['title'] = w.title

        work_info['type'] = w.work_type

        work_info['data'] = w.get_work_data()

        authorship = WorkAuthorship.objects.get(author=t, work=w)

        if not hasattr(w, 'pages_number'):
            pass
        elif authorship.pages_authored:
            work_info['author_pages'] = authorship.pages_authored
            work_info['pages'] = w.pages_number
        else:
            work_info['author_pages'] = w.pages_number

        work_info['coauthors'] = ', \n'.join(sorted([a.short_name() for a in authorship.get_other_authors().all()]))

        context['content'].append(work_info)

    file_name = f'Звіт {t}.docx'
    generate_docx('form11.docx', context, file_name)

    return redirect(static(f'generated/{file_name}'))
