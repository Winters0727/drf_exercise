from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns

from snippets import views

# function based views
# urlpatterns = [
#     path('', views.snippet_list),
#     path('<int:pk>/', views.snippet_detail),
# ]

# class based views
urlpatterns = [
    path('', views.SnippetList.as_view()),
    path('<int:pk>/', views.SnippetDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)