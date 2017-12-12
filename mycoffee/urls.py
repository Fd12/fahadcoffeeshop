from django.conf.urls import url
from . import views


app_name="mycoffee"

urlpatterns = [
	url(r'^signup/$', views.usersignup, name="signup"),
	url(r'^login/$', views.userlogin, name="login"),
	url(r'^logout/$', views.userlogout, name="logout"),
	url(r'^create_coffee/$', views.create_coffee, name='create_coffee'),


]