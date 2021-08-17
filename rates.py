from datetime import date
import xmltodict
import requests
import json


def updateCbrRates():
    cbr_url = 'https://www.cbr.ru/scripts/XML_daily.asp'
    r = requests.get(cbr_url, params={
        'date_req': date.today().strftime('%d/%m/%Y')})
    if r.status_code == 200:
        cbr_rates = xmltodict.parse(r.text)
        with open('cbr_rates.json', 'w') as f:
            json.dump(cbr_rates, f)
    return cbr_rates


class Rates:
    def __init__(self, currencies=[]):
        self.cbr = self.loadCbrRates()
        self.base = 'RUB'
        self.rates = self.getRates(currencies)

    def loadCbrRates(self):
        with open('cbr_rates.json', 'r') as f:
            cbr_rates = json.load(f)
            return cbr_rates

    def getRates(self, currencies=[]):
        if not currencies:
            rates = {self.base: 1.0}
            for currency_dict in self.cbr["ValCurs"]["Valute"]:
                char_code = currency_dict["CharCode"]
                value = float(currency_dict["Value"].replace(',', '.'))
                nominal = float(currency_dict["Nominal"].replace(',', '.'))
                rates[char_code] = value/nominal
        else:
            rates = dict.fromkeys(currencies, 1.0)
            for currency_dict in self.cbr["ValCurs"]["Valute"]:
                char_code = currency_dict["CharCode"]
                if char_code in currencies:
                    value = float(currency_dict["Value"].replace(',', '.'))
                    nominal = float(currency_dict["Nominal"].replace(',', '.'))
                    rates[char_code] = value/nominal
        return rates

    def convert(self, new_base):
        return {rate: self.rates[rate]/self.rates[new_base] for rate in self.rates}
