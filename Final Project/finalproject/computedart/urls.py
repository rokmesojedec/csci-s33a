from django.urls import path

from . import views

urlpatterns = [
    path("", views.showcase, name="showcase"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("config", views.config, name="config"),
    path("config/create", views.create_config, name="create"),
    path("config/<int:config_id>", views.view_config, name="config"),
    path("config/<int:config_id>/upload", views.upload, name="upload"),
    path("config/json/<int:config_id>", views.get_config, name="get_config"),
    path("config/user/<int:user_id>", views.user_configs, name="user_configs"),
]
