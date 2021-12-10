from django.urls import path

from . import views


urlpatterns = [
	path('', views.store, name="store"),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),

	path('search/', views.search, name="search"),
	path('signup/', views.signup, name="signup"),

	path('login/', views.loginfunc, name="login"),
	path('logout/', views.logoutUser, name="logout"),
	path('forgot_password/', views.forgot, name="forgot"),
	path('getinfo/', views.getinfo, name="getinfo"),







	
	path('men/', views.men, name="men"),
	path('women/', views.women, name="women"),
	path('kids/', views.kids, name="kids"),
	path('electronics/', views.electronics, name="electronics"),
	path('aboutus/', views.about, name="aboutus"),
	path('conatactus/', views.contact, name="contactus"),



	path('update_item/',views.updateItem, name="update_item"),
	path('process_order/',views.processOrder, name="process_order"),
	path('product_view/<str:pk>',views.productView, name="product_view"),


]