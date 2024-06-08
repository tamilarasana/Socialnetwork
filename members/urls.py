from django.urls import path
from .views import *

urlpatterns = [
    path('login/', LoginView, name="login"),
    path('signup/', SignupView, name="signup"),
    path('search/', searchUsers, name="search"),
    path('friend_req/', sendFriendRequest, name="send_friend_request"),
    path('friend_request/<int:key>/', respondFriendRequest, name="respond_friend_request"),
    path('friends/', listFriends, name="list_friends"),
    path('pending_request/', listPendingRequests, name="pendingrequests"),
]