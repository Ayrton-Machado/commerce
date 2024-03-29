from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('createlisting', views.create_listing, name='createlisting'),
    path('listing/<str:listing_id>', views.listing, name='listing'),
    path('listing/<str:listing_id>/bid', views.placeBid, name='placebid'),
    path('listing/<str:listing_id>/close', views.closeAuction, name='closeAuction'),
    path('listing/<str:listing_id>/comment', views.addComment, name='addComment'),
    path('watchlist', views.watchlist, name='watchlist'),
    path('watchlist/remove', views.watchlistRemove, name='watchlistRemove'),
    path('categories', views.Categories, name='categories'),
    path('categories/<str:which_category>', views.whichCategory, name='category'),
    path('error', views.error, name='error')
]
