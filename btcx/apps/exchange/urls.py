from django.conf import settings
from django.conf.urls.defaults import *
from btcx.apps.exchange.views import HomeView, BuyApiView, SellApiView

urlpatterns = patterns('',
    url(r'^/?$', HomeView.as_view(), name='home'),
    url(r'^buy/(?P<amount>\d+(\.\d+)?)/?$', BuyApiView.as_view(), name='buy_api'),
    url(r'^sell/(?P<amount>\d+(\.\d+)?)/?$', SellApiView.as_view(), name='sell_api'),
)
