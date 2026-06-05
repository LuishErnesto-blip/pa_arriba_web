from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [
    path("", views.post_list, name="post_list"),
    path("crm/dashboard/", views.dashboard_crm, name="dashboard_crm"),
    path("<slug:slug>/", views.post_detail, name="post_detail"),
]
