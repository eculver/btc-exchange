from decimal import Decimal
from django import http
from django.conf import settings
from django.views.generic.base import View, ContextMixin, TemplateView
from django.utils import simplejson as json
from mexbtcapi.api import mtgox
from mexbtcapi.concepts.currencies import USD, BTC
from mexbtcapi.concepts.currency import Amount

ONE_DOLLAR = Amount(1, USD)


class JsonResponseMixin(object):
    def render_to_response(self, context):
        "Returns a JSON response containing 'context' as payload"
        return self.get_json_response(self.convert_context_to_json(context))

    def get_json_response(self, content, **httpresponse_kwargs):
        "Construct an `HttpResponse` object."
        return http.HttpResponse(content,
                                 content_type='application/json',
                                 **httpresponse_kwargs)

    def convert_context_to_json(self, context):
        "Convert the context dictionary into a JSON object"
        return json.dumps(context)


class HomeView(TemplateView):
    template_name = "exchange/home.html"


class BaseApiView(JsonResponseMixin, ContextMixin, View):
    def get_xrt(self):
        xrt = mtgox.market(USD).getTicker().sell
        # returns a Decimal type
        return xrt.exchange_rate

    def get_avg(self, orders=[]):
        exchange_rates = [x.exchange_rate.exchange_rate for x in orders]

        # returns the average across the order values
        return sum(exchange_rates) / len(orders)

    def get_orders(self, depth):
        """Return the orders from the book that is in question.
        Should be overridden in child view"""
        return []

    def get_context_data(self, **kwargs):
        # validated by URL pattern
        amount = Decimal(self.kwargs.pop('amount'))

        depth = mtgox.market(USD).getDepth()
        orders = self.get_orders(depth)

        sought = Amount(amount, BTC)
        obtained = Amount(0, BTC)
        orders_from = []
        order_idx = 0

        # get all of the orders we could be purchasing from
        while obtained < sought:
            order = orders[order_idx]
            xrt = order.exchange_rate

            # we're always trying to buy/sell BTC, so make sure the amounts
            # are consistent
            order_btc_amount = xrt.convert(order.to_amount, BTC)

            obtained = obtained + order_btc_amount
            orders_from.append(order)

        # get average of all orders from which the purchase will be constructed
        # as a Decimal
        avg = self.get_avg(orders=orders_from)
        total = float(amount * avg)

        # add commission
        value = (total * settings.BTCX_COMMISSION) + total

        ctx = {
            'rate': {
                'value': value,
                'currency': 'USD',
                'amount': float(amount)
            }
         }
        return ctx

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


class BuyApiView(BaseApiView):
    def get_orders(self, depth):
        # get the ask book since we want to buy
        return depth.sell_orders

class SellApiView(BaseApiView):
    def get_orders(self, depth):
        # get the bid book since we want to sell
        return depth.buy_orders

