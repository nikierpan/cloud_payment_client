from typing import Optional, Dict, Any
from logging import Logger

import marshmallow_dataclass
from marshmallow import ValidationError

from data_types import CardPayRequestData, TokenPayRequestData, BasePayResponseData
from configs import CloudPaymentsConfig as CPConf


class BaseValidateError(Exception):
    default_message = 'Backend data validation error'

    def __init__(self, *, service: str, message: Optional[str] = None):
        self.message = message or self.default_message
        self.service = service

    @property
    def name(self):
        return self.__class__.__name__

    def __str__(self):
        return f'{self.__class__.__name__}({self.service}: {self.message}'


class PaymentTypeValidateError(BaseValidateError):
    def __init__(self, *, service: str, wrong_type: str):

        self.wrong_type = wrong_type
        self.supported_types = CPConf.PAYMENT_TYPES

        self.message = f'{self.name}: Unsupported payment type: got "{self.wrong_type}", must be ' \
                       f'one of {self.supported_types} '

        super().__init__(service=service, message=self.message)


class RequestDataValidateError(BaseValidateError):
    def __init__(self, *, service: str, exception: ValidationError):

        self.message = f'{self.name}: {exception.messages}'

        super().__init__(service=service, message=self.message)


class ResponseDataValidateError(BaseValidateError):
    def __init__(self, *, service: str, exception: ValidationError):

        self.message = f'{self.name}: {exception.messages}'

        super().__init__(service=service, message=self.message)


class CloudPaymentValidator:
    def __init__(self, service: str, logger: Logger):
        self.service = service
        self.logger = logger

    def payment_type(self, payment_type: str):
        if payment_type not in CPConf.PAYMENT_TYPES:
            error = PaymentTypeValidateError(service=self.service, wrong_type=payment_type)
            self.logger.error(msg=error.message)
            raise error
        else:
            return payment_type

    def card_pay_request_data(self, data: Dict[str, Any]) -> CardPayRequestData:

        CardPayRequestDataSchema = marshmallow_dataclass.class_schema(CardPayRequestData)
        card_pay_request_data_schema = CardPayRequestDataSchema()

        try:
            card_pay_request_data = card_pay_request_data_schema.load(data)
        except ValidationError as e:
            error = RequestDataValidateError(service=self.service, exception=e)
            self.logger.error(msg=error.message)
            raise error

        return card_pay_request_data

    def token_pay_request_data(self, data: Dict[str, Any]) -> TokenPayRequestData:
        TokenPayRequestDataSchema = marshmallow_dataclass.class_schema(TokenPayRequestData)
        token_pay_request_data_schema = TokenPayRequestDataSchema()

        try:
            token_pay_request_data = token_pay_request_data_schema.load(data)
        except ValidationError as e:
            error = RequestDataValidateError(service=self.service, exception=e)
            self.logger.error(msg=error.message)
            raise error

        return token_pay_request_data

    def pay_response_data(self, data: Dict[str, Any]) -> TokenPayRequestData:
        PayResponseDataSchema = marshmallow_dataclass.class_schema(PayResponseData)
        pay_response_data_schema = PayResponseDataSchema()

        try:
            pay_response_data = pay_response_data_schema.load(data)
        except ValidationError as e:
            error = ResponseDataValidateError(service=self.service, exception=e)
            self.logger.error(msg=error.message)
            raise error

        return pay_response_data


