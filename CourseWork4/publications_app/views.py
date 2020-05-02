from django.shortcuts import render, redirect
from django.http import HttpResponse
from .docx_generator import generate_docx
from django.templatetags.static import static


def index(request):
    context = dict()
    context['author'] = 'test'
    context['content'] = [[1, 2, 3, 4, 5, 6]]

    generate_docx('form11.docx', context, 'test.docx')

    return redirect(static('generated/test.docx'))
