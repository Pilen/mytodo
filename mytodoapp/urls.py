from django.conf.urls import url

from . import views

urlpatterns = [
    url(r"^$", views.index, name="index"),
    url(r"^api/add$", views.add, name="add"),
    url(r"^api/all$", views.get_all, name="all"),
    url(r"^api/change$", views.change, name="change"),
    url(r"^api/delete$", views.delete, name="delete"),

    url(r"^login$", views.login, name="login"),
    url(r"^register$", views.register, name="register"),
    url(r"^logout$", views.logout, name="logout"),
]
