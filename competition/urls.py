from django.conf.urls import url
from . import views
urlpatterns = [
    url(r"^$", views.view_competition_list, name="list"),
    url(r"^(?P<pk>\d+)/$", views.view_competition_detail, name="detail"),
    url(r"^(?P<pk>\d+)/edit$", views.update_competition, name="update"),
    url(r"^create/$", views.create_competition, name="create"),
    url(r"^download/(?P<filepath>[\w\d_\-/.]+)$", views.download, name="download"),
    # url(r"^login/$", views.LoginView.as_view(), name="login"),
    # url(r"^logout/$", views.LogoutView.as_view(), name="logout"),
    # url(r"^register/$", views.RegisterView.as_view(), name="register"),
    # url(r"^password-reset/$", views.PasswordResetView.as_view(), name="password_reset"),
    # url(r"^password-change/$", views.PasswordChangeView.as_view(), name="password_change"),
]
