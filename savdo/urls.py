from django.urls import path
from savdo.views import index, shop_detail, make_order, about, set_language


urlpatterns = [
    path('', index, name='index'),
    path('shop-detail/<slug:slug>/', shop_detail, name='shop_detail'),
    path('make-order/', make_order, name='make_order'),
    path('about/', about, name='about'),
    path('set-language/', set_language, name='set_language'),
]