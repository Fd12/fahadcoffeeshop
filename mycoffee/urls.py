from django.conf.urls import url
from . import views


app_name="mycoffee"

urlpatterns = [
	url(r'^signup/$', views.usersignup, name="signup"),
	url(r'^login/$', views.userlogin, name="login"),
	url(r'^logout/$', views.userlogout, name="logout"),
	url(r'^create_coffee/$', views.create_coffee, name='create_coffee'),
	url(r'^ajax_price/$', views.ajax_price, name="ajax_price"),
	url(r'^$', views.coffee_list, name='coffee_list'),
	url(r'^coffee_detail/(?P<coffee_id>[0-9]+)/$', views.coffee_detail, name="coffee_detail"),


]