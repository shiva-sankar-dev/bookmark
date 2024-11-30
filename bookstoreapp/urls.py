from django.urls import path
from bookstoreapp import views

urlpatterns = [
    path('login/',views.loginpage,name="loginpage"),
    path('logout/',views.logoutpage,name="logout"),
    path('signup',views.registrationpage,name="registrationpage"),
    path('',views.index,name="homepage"),
    path('booklist/',views.booklist,name="booklist"),
    path('wishlist/',views.wishlist,name="wishlist"),
    path('wishlist_toggle/',views.wishlist_toggle,name="wishlist_toggle"),
    path('filterlist/<str:genre>',views.filterlist,name="filterlist"),
    path('contactus/',views.contactus,name="contactus"),
    path('aboutus/',views.aboutus,name="aboutus"),
    path('remove_cart_item/<int:id>',views.remove_cart_item,name="remove_cart_item"),
    path('cart/',views.cart,name="cart"),
    path('details/<str:id>/',views.details,name="details"),
]
