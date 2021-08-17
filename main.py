import os
import schedule
import time
import requests
import json
from auth import initAuth, refreshAuth
from rates import Rates, updateCbrRates


def getBtrxBase(auth_data):
    r = requests.get(
        auth_data['client_endpoint']+'crm.currency.base.get'+'.json?&auth='+auth_data['access_token'])
    return r.json()['result']


def getBtrxCurrencies(auth_data):
    r = requests.get(
        auth_data['client_endpoint']+'crm.currency.list'+'.json?&auth='+auth_data['access_token'])
    return [d['CURRENCY'] for d in r.json()['result']]


def updateBtrxCurrencies(auth_data, rates):
    for currency in rates:
        params = {
            'id': currency,
            'fields[AMOUNT]': rates[currency],
            'fields[AMOUNT_CNT]': 1,
            'auth': auth_data['access_token']
        }
        r = requests.post(auth_data['client_endpoint'] +
                          'crm.currency.update', params=params)


def job():
    refreshAuth()
    with open('auth_data.json', 'r') as f:
        auth_data = json.load(f)
    btrx_base = getBtrxBase(auth_data)
    btrx_currencies = getBtrxCurrencies(auth_data)
    updateCbrRates()
    rates = Rates(btrx_currencies)
    updateBtrxCurrencies(auth_data, rates.convert(btrx_base))


if not os.path.isfile('auth_data.json'):
    initAuth()
    schedule.every().minute.do(job)
else:
    schedule.every().minute.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
