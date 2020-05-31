from django.urls import path

from . import views

urlpatterns = [
    path('', views.AuthorIndexView.as_view()),
    path('authors', views.AuthorIndexView.as_view(), name='author_list'),
    path('authors/<int:pk>/', views.AuthorDetailView.as_view(), name='author_details'),
    path('authors/<int:pk>/report', views.generate_report, name='author_report'),
]
