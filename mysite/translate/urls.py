"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from . import views
from .views import (TitleListView,
                    ContentListView,
                    ContentDetailView,
                    ContentCreateView)
from .models import Translate
from personal import views as user_views
from dashboard import views as dashboard_views

urlpatterns = [
    path('', views.home, name='home'),
    path('translator/', TitleListView.as_view(), name='translate'),
    # path('newcontent/', ContentCreateView.as_view(), name='newcontent'),
    path('newcontent/', views.create_new_content, name='newcontent'),
    path('contentlist/', views.content_by_library, name='contentlist'),
    path('translator/<int:pk>/', ContentDetailView.as_view(), name='contentdetail'),
    path('translator/<int:pk>/word/', views.manage_word_translation, name='createwordtranslation'),
    path('translator/<int:pk>/wordclass/', views.get_word_known_level, name='get-word-knownlevel'),
    #  path('translator/<int:pk>/translatewindow/', views.translator_window_design, name='translator-window-design'),
    path('timer/', views.timer, name='timer'),
    #  path('timer/word/', views.create_word_translation, name='word'),
    path('contentlist/<int:pk>/delete/', views.delete_content, name='delete'),
    path('profile/<int:pk>/', user_views.user_profile, name='profile'),

    path('timer/wordclass/', views.get_word_known_level, name='wordclass-test'),
    path('login/', user_views.user_login, name='login'),
    path('logout/', user_views.user_logout, name='logout'),
    path('register/', user_views.user_register, name='register'),

    #  -------------HOME PAGE pattern-------------
    path('index/', user_views.index, name='index'),

    #  -------------DASHBOARD patterns-------------

    path('chart/', dashboard_views.chart, name='chart'),
    path('dashboard/', dashboard_views.dashboard, name='dashboard'),
    path('dashboard/main_dashboard_data/', dashboard_views.main_dashboard_data, name='main_dashboard_data'),
    path('dashboard/salesperson_yearly/', dashboard_views.main_dashboard_salesperson, name='salesperson_yearly'),
    path('dashboard/monthly_table/', dashboard_views.main_dashboard_monthly_table, name='monthly_table'),
    path('dashboard/customer_yearly/', dashboard_views.main_dashboard_customer_chart, name='customer_yearly'),
    path('dashboard/product_yearly/', dashboard_views.main_dashboard_product_chart, name='product_yearly'),
    path('dashboard/sub_dashboard/', dashboard_views.sub_dashboard_view, name='sub_dashboard'),
    path('getdata/', dashboard_views.get_revenue_by_customer, name='getdata'),
    path('chart/getrebvyprod/', dashboard_views.get_revenue_by_product, name='getrebvyprod')
    # path('translator/<int:pk>/<word>/', views.word_view, name='contentword'),
]
