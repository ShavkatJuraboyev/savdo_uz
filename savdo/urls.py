from django.urls import path
from savdo.views import index, shop_detail, about, set_language, news, news_detail


urlpatterns = [
    path('', index, name='index'),
    path('shop-detail/<slug:slug>/', shop_detail, name='shop_detail'),
    path('about/', about, name='about'),
    path('set-language/', set_language, name='set_language'),

    path('news/', news, name="news"),
    path("news/<int:id>/", news_detail, name="news_detail"),

]