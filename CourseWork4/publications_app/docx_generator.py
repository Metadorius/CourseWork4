from docxtpl import DocxTemplate
import os
from django.contrib.staticfiles import finders


def generate_docx(template_filename, context, result_filename):
    tpl = DocxTemplate(finders.find(
        os.path.join('templates', template_filename)))
    tpl.render(context)
    tpl.save(os.path.join(finders.find('generated'), result_filename))
