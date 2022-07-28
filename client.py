from typing import Optional, Dict, Any, Union
import functools
from dataclasses import asdict
import base64
import logging

from aiohttp import BasicAuth
from aiohttp import connector

from abstract_client import AbstractInteractionClient, InteractionResponseError
from configs import CloudPaymentsConfig as CPConf
from data_types import BasePayResponseData, TokenPayRequestData, CardPayRequestData
from validators import CloudPaymentValidator, BaseValidateError


class CloudPaymentClient(AbstractInteractionClient):
    _BASIC_AUTH: Optional[BasicAuth] = None
    REQUEST_TIMEOUT = CPConf.REQUEST_TIMEOUT
    CONNECT_TIMEOUT = CPConf.REQUEST_TIMEOUT
    BASE_URL = CPConf.BASE_URL
    SERVICE = 'service_name'

    def __init__(self, public_id: str, api_secret: str):
        self.CONNECTOR = connector.TCPConnector()
        self.logger = self._init_logger()

        super().__init__()

        self.public_id = public_id
        self._api_secret = api_secret
        self.validator = CloudPaymentValidator(service=self.SERVICE, logger=self.logger)

    @staticmethod
    def _init_logger():
        logging.basicConfig(level=logging.ERROR, filename='cloud_payment_error.log',
                            format='%(asctime)s %(levelname)s: %(message)s')
        return logging.getLogger(__name__)

    @property
    def api_secret(self):
        return None

    @property
    def basic_auth(self):
        if self._BASIC_AUTH:
            return self._BASIC_AUTH

        self._BASIC_AUTH = BasicAuth(login=self.public_id, password=self._api_secret)

        return self._BASIC_AUTH

    async def __aenter__(self):
        await self.session.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
        await self.CONNECTOR.close()

    async def _make_payment(self, url: str,
                            data: Union[CardPayRequestData, TokenPayRequestData]) -> BasePayResponseData:

        try:
            resp_data = await self.post(interaction_method='POST', url=url,
                                        data=data, auth=self.basic_auth)

        except InteractionResponseError as e:
            self.logger.error(msg=e.__str__())
            raise e

        validated_resp_data = self.validator.pay_response_data(resp_data)

        return validated_resp_data

    async def make_card_payment(self,
                                data: Dict[str, Any],
                                payment_type: str = 'charge') -> BasePayResponseData:

        validated_payment_type = self.validator.payment_type(payment_type)

        url = self.endpoint_url(CPConf.CARD_PAY_URL + validated_payment_type)

        validated_data = self.validator.card_pay_request_data(data)

        return await self._make_payment(url=url, data=asdict(validated_data))

    async def make_token_payment(self,
                                 data: Dict[str, Any],
                                 payment_type: str = 'charge') -> BasePayResponseData:

        validated_payment_type = self.validator.payment_type(payment_type)
        url = self.endpoint_url(CPConf.TOKEN_PAY_URL + validated_payment_type)

        validated_data = self.validator.token_pay_request_data(data)

        return await self._make_payment(url=url, data=asdict(validated_data))

    @staticmethod
    def decode_yandex_token(token: str) -> str:
        decode_token = base64.b64decode(token.encode("ascii")).decode("ascii")
        return decode_token

    async def make_payment_by_yandex_token(self,
                                           data: Dict[str, Any],
                                           payment_type: str = 'charge'):

        validated_payment_type = self.validator.payment_type(payment_type)
        url = self.endpoint_url(CPConf.TOKEN_PAY_URL + validated_payment_type)

        validated_data = self.validator.token_pay_request_data(data)
        validated_data.Token = self.decode_yandex_token(validated_data.Token)

        return await self._make_payment(url=url, data=asdict(validated_data))
