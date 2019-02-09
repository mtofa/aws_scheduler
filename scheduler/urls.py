from django.urls import path
from . import views

urlpatterns = [
    # templates/myapp need to have a file name base.html.
    # it is django convention else entry/ would not work as expected.
    # do not use rails way (application.html). Always use base.html
    path('', views.index, name='index'),
    path('new', views.new, name='new'),
    path('delete/<int:pk>', views.delete, name='delete'),
    path('create', views.create, name='create'),
    path('edit/<int:pk>', views.edit, name='edit'),
    path('update/<int:pk>', views.update, name='update'),
]