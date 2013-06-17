# btc-exchange

A demo application for interacting with the Mt. Gox API to do exchanges.

## Overview

The application implements a simple user interface and API for obtaining the
price for which a given amount of bitcoins can be obtained (buy) or the price
for which a given amount of bitcoins can be sold. All of the data is based on
the real-time order book provided by the Mt. Gox HTTP API as described here:

https://en.bitcoin.it/wiki/MtGox/API/HTTP/v1#Multi_Currency_depth

All prices are normalized to USD.

## Running Tests

To run the application tests and the development server, you first need to install the application's requirements. It is recommended to do this within a virtualenv:

``pip install -r requirements.txt``

Then to run tests:

``python manage.py test``

## Implementation

The application is implemented as a simple Django/Python WSGI application. There
are only 3 views:

* home:
  * endpoint: /
  * purpose: Basic user interface for submitting values to the buy or sell API endpoints

* buy:
  * endpoint: /buy/``amount``
  * purpose: Retrieving the value in USD that ``amount`` bitcoins would cost to buy.

* sell:
  * endpoint: /sell/``amount``
  * purpose: Retrieving the value in USD that ``amount`` bitcoins would be worth to sell.


## TODO

This was all put together in just a few hours. If I had more time to work on this, I would add these things:

1. Caching of API data - Every request to the ``buy`` and ``sell`` hits the Mt.Gox API directly and is not very performant. It would probably be a little more effective to either integrate the Mt. Gox streaming/websocket API or to implement a reasonable caching layer so that the order books were kept up to date out-of-band from the normal HTTP requests.

2. Notifications - It would be useful if, once a value for BTC was derived, the user could input a threshold or notification rule related to that value so that they could be notified when the best time to buy or sell may be present. It's not entirely realistic to query the API every time to grab the latest value for a buy or sell. It seems more realistic to be notified once a criteria of the data has been met.

3. Time-series Data - If the data gathered from the API was persisted in some way and indexed over time, it would be useful to provide charts and graphs displaying the data over time. It seems like the original data may have more context and relevance if it was displayed next to historical data.

4. Tests - The code isn't very well tested. There should be better coverage.
