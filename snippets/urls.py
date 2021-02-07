from django.urls import path, include

from rest_framework import renderers
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns

from snippets import views
from snippets.views import api_root, SnippetViewSet, UserViewSet

# function based views
# urlpatterns = [
#     path('', views.snippet_list),
#     path('<int:pk>/', views.snippet_detail),
# ]

# class based views
# urlpatterns = [
#     # path('', views.SnippetList.as_view()),
#     path('', views.api_root),
#     path('<int:pk>/', views.SnippetDetail.as_view()),
#     path('<int:pk>/highlight/', views.SnippetHighlight.as_view()),
#     path('users/', views.UserList.as_view()),
#     path('users/<int:pk>/',views.UserDetail.as_view()),
# ]

# api endpoints
# urlpatterns = [
#     path('', views.api_root),
#     path('all/', views.SnippetList.as_view(), name='snippet-list'),
#     path('<int:pk>/', views.SnippetDetail.as_view(), name='snippet-detail'),
#     path('<int:pk>/highlight/', views.SnippetHighlight.as_view(), name='snippet-highlight'),
#     path('users/', views.UserList.as_view(), name='user-list'),
#     path('users/<int:pk>/',views.UserDetail.as_view(), name='user-detail'),
# ]

# snippet_list = SnippetViewSet.as_view({
#     'get' : 'list',
#     'post' : 'create'
# })

# snippet_detail = SnippetViewSet.as_view({
#     'get' : 'retrieve',
#     'put' : 'update',
#     'patch' : 'partial_update',
#     'delete' : 'destroy'
# })

# snippet_highlight = SnippetViewSet.as_view({
#     'get' : 'highlight'
# }, renderer_classes=[renderers.StaticHTMLRenderer])

# user_list = UserViewSet.as_view({
#     'get' : 'list'
# })

# user_detail = UserViewSet.as_view({
#     'get' : 'retrieve'
# })

# urlpatterns = [
#     path('', api_root),
#     path('all/', snippet_list, name='snippet-list'),
#     path('<int:pk>/', snippet_detail .as_view(), name='snippet-detail'),
#     path('<int:pk>/highlight/', snippet_highlight, name='snippet-highlight'),
#     path('users/', user_list, name='user-list'),
#     path('users/<int:pk>/', user_detail, name='user-detail'),
# ]

router = DefaultRouter()
router.register(r'snippets', views.SnippetViewSet)
router.register(r'users', views.UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

# urlpatterns = format_suffix_patterns(urlpatterns)