"""consignment URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path
from consignment_app import views
from django.views.decorators.cache import cache_page
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),

    path('',views.index,name='index'),


    path('index_menu', views.index_menu, name='index_menu'),
    path('user_menu', views.user_menu, name='user_menu'),

    path('nav', views.nav, name='nav'),
    path('feedback', views.feedback, name='feedback'),
    path('view_feedback', views.view_feedback, name='view_feedback'),

    path('userlogin', views.userlogin, name='userlogin'),
    path('admin_home', views.admin_home, name='admin_home'),
    path('user_home', views.user_home, name='user_home'),

    path('addConsignment/', views.addConsignment, name='addConsignment'),
    path('printConsignment/<int:track_id>/', views.printConsignment, name='printConsignment'),
    path('view_consignment', views.view_consignment, name='view_consignment'),
    path('user_view_consignment', views.user_view_consignment, name='user_view_consignment'),

    path('consignment_edit/<int:pk>', views.consignment_edit, name='consignment_edit'),
    path('consignment_delete/<int:pk>', views.consignment_delete, name='consignment_delete'),
    path('invoiceConsignment/<int:pk>', views.invoiceConsignment, name='invoiceConsignment'),

    path('addTrack', views.addTrack, name='addTrack'),
    path('search_results', views.search_results, name='search_results'),

    path('user_search_results', views.user_search_results, name='user_search_results'),

    path('track_delete/<int:pk>', views.track_delete, name='track_delete'),

]
