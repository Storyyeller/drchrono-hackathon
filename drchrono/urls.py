from django.conf.urls import include, url
from django.views.generic import TemplateView


from . import views


urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='index.html')),
    url(r'^redirect$', views.home),
    url(r'^checkin$', views.checkin),
    url(r'^editdata$', views.editdata),

    url(r'', include('social.apps.django_app.urls', namespace='social')),
]
