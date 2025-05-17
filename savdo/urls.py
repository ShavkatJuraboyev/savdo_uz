from django.urls import path
from savdo.views import index, shop_detail, make_order, about


urlpatterns = [
    path('', index, name='index'),
    path('shop-detail/', shop_detail, name='shop_detail'),
    path('make-order/', make_order, name='make_order'),
    path('about/', about, name='about'),
    # path('accounts/profile/', views.profile, name='profile'),
    # path('accounts/logout/', views.logout_view, name='logout'),
]