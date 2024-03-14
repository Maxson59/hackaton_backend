from django.urls import path
from user import views

app_name = 'user'

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('me/', views.UserMeView.as_view(), name='me'),
    path(
        'me/upload-image/',
        views.UserMeCustomActionsView.as_view({'patch': 'upload_image'}),
        name='upload-image'
    ),
]
