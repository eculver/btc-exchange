from django.test import TestCase
from django.utils import simplejson as json
from django.core.urlresolvers import reverse


class ExchangeTestCase(TestCase):
    def test_home(self):
        url = reverse('home')
        resp = self.client.get(url)
        templates = [t.name for t in resp.templates]
        templates_expected = [
            'common/base.html',
            'common/loading.html',
            'exchange/home.html'
        ]

        # assert that the URL returns 200.
        self.assertEqual(resp.status_code, 200)

        # assert that the correct template was used.
        self.assertItemsEqual(templates, templates_expected)

    def test_buy_api(self):
        # make sure endpoint returns 200
        buy_url = reverse('buy_api', args=[10])
        resp = self.client.get(buy_url)
        self.assertEqual(resp.status_code, 200)

        # make sure the endpoint returns JSON
        self.assertEqual(resp['Content-Type'], 'application/json')

        # make sure the endpoint returns correct shape
        resp_json = json.loads(resp.content)
        self.assertTrue('rate' in resp_json)
        self.assertTrue('value' in resp_json['rate'])
        self.assertTrue('currency' in resp_json['rate'])
        self.assertTrue('amount' in resp_json['rate'])

    def test_sell_api(self):
        # make sure endpoint returns 200
        sell_url = reverse('sell_api', args=[10])
        resp = self.client.get(sell_url)
        self.assertEqual(resp.status_code, 200)

        # make sure the endpoint returns JSON
        self.assertEqual(resp['Content-Type'], 'application/json')

        # make sure the endpoint returns correct shape
        resp_json = json.loads(resp.content)
        self.assertTrue('rate' in resp_json)
        self.assertTrue('value' in resp_json['rate'])
        self.assertTrue('currency' in resp_json['rate'])
        self.assertTrue('amount' in resp_json['rate'])
