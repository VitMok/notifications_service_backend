from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()

router.register('total-statistic', views.TotalStatisticMailingListView, basename='totalstatistic')

urlpatterns = [
    path('clients/create/', views.ClientCreateView.as_view()),
    path('clients/<int:pk>/', views.ClientDetailView.as_view()),
    path('mailings/create/', views.MailingCreateView.as_view()),
    path('mailings/<int:pk>/statistic/', views.DetailStatisticMailingView.as_view()),
    path('mailings/<int:pk>/', views.MailingDetailView.as_view()),
]

urlpatterns += router.urls