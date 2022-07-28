import os


class CloudPaymentsConfig:

    BASE_URL = "https://api.cloudpayments.ru"
    CARD_PAY_URL = '/payments/cards/'
    TOKEN_PAY_URL = '/payments/tokens/'

    REQUEST_TIMEOUT = 300

    PAYMENT_TYPES = ['auth', 'charge']

    CURRENCY = ["RUB", "EUR", "USD", "GRB", "UAH", "BYR", "BYN", "KZT", "AZN", "CHF",
                "CZK", "CAD", "PLN", "SEK", "TRY", "CNY", "INR", "BRL", "ZAR", "UZS",
                "BGN", "RON", "AUD", "HKD", "GEL", "KGS", "AMD", "AED"]

    CULTURE_NAME = ["ru-RU", "en-US", "lv", "az", "kk", "uk", "pl", "vi", "tr"]
