import os
import asyncio

from client import CloudPaymentClient

PUBLIC_KEY = 'xxxxxxxxxxxx'
API_SECRET = os.environ.get('CLOUD_PAYMENT_API_SECRET')

DATA = {
    "Amount": 0.01,
    "Currency": "RUB",
    "InvoiceId": "1234567",
    "Description": "Оплата товаров в example.com",
    "AccountId": "user_x",
    "Token": "c3VjY2Vzc18xMTExYTNlMC0yNDI4LTQ4ZmItYTUzMC0xMjgxNWQ5MGQwZTg=",
}


async def main():
    async with CloudPaymentClient(public_id=PUBLIC_KEY, api_secret=API_SECRET) as client:
        payment_resp = await client.make_payment_by_yandex_token(data=DATA, payment_type='charge')

        # payment_resp.Success
        # payment_resp.Message
        # payment_resp.Model


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
