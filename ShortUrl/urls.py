"""ShortUrl URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from shorturlapp import views
from django.conf.urls import url
from ShortUrl.settings import ACCESSIBLE_SHORT_URL_KEY_LENGTH, URLS

urlpatterns = [
    url(URLS['ADMIN'], admin.site.urls),
    url(URLS['SHORT_URL'], views.short_url),
    url(URLS['GET_SHORT_URL'], views.set_short_url),
    url(URLS['GET_COUNT'], views.get_count),
    url(URLS['HOME_PAGE'], views.homepage),
    url(r'^.{%s,%s}/' % (ACCESSIBLE_SHORT_URL_KEY_LENGTH['MIN'], ACCESSIBLE_SHORT_URL_KEY_LENGTH['MAX']),
        views.redirect_to_long_url),

]
