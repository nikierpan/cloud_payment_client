from dataclasses import dataclass, field
from typing import Union, Optional, Dict, Any

from marshmallow import Schema, fields, validate

from configs import CloudPaymentsConfig as CPConf


@dataclass
class PayerData():
    FirstName: Optional[str] = None
    LastName: Optional[str] = None
    MiddleName: Optional[str] = None
    Birth: Optional[str] = None
    Street: Optional[str] = None
    Address: Optional[str] = None
    City: Optional[str] = None
    Country: Optional[str] = None
    Phone: Optional[str] = None
    Postcode: Optional[str] = None


@dataclass(kw_only=True)
class _BasePayRequestData:
    # The Amount parameter does not accept a transaction amount less than 0.01.
    Amount: float = field(metadata=dict(validate=validate.Range(min=0.01)))

    Currency: Optional[str] = field(metadata=dict(validate=validate.OneOf(CPConf.CURRENCY), load_default='RUB'))
    IpAddress: str = None
    Description: Optional[str] = None
    AccountId: Optional[str] = None
    InvoiceId: Optional[str] = None
    Email: Optional[str] = None
    JsonData: Optional[Dict[str, Any]] = None


@dataclass(kw_only=True)
class CardPayRequestData(_BasePayRequestData):
    """
    Request data for https://api.cloudpayments.ru/payments/cards/... endpoints
    """

    IpAddress: str = field(metadata=dict(required=True))
    CardCryptogramPacket: str = field(metadata=dict(required=True))

    Name: Optional[str] = None
    PaymentUrl: Optional[str] = None
    CultureName: Optional[str] = field(metadata=dict(required=False, validate=validate.OneOf(CPConf.CULTURE_NAME)))
    Payer: Optional[PayerData] = None


@dataclass(kw_only=True)
class TokenPayRequestData(_BasePayRequestData):
    """
    Request data for https://api.cloudpayments.ru/payments/tokens/... endpoints
    """

    Token: str = field(metadata=dict(required=True))
    AccountId: Optional[str] = field(metadata=dict(required=False))


@dataclass
class BasePayResponseData:
    """
    Response data received from https://api.cloudpayments.ru/payments
    """
    Success: bool = field(metadata=dict(required=True))
    Message: Optional[str] = None
    Model: Optional[Dict[str, Any]] = None
