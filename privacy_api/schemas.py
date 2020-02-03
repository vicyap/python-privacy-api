"""Schemas."""
from marshmallow import Schema, fields, post_load
from privacy_api import models

# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=no-self-use
# pylint: disable=unused-argument


class FundingAccountSchema(Schema):
    account_name = fields.Str()
    token = fields.Str()
    type = fields.Str()

    @post_load
    def make(self, data, **kwargs):
        return models.FundingAccount(**data)


class FundingSchema(Schema):
    amount = fields.Integer()
    token = fields.Str()
    type = fields.Str()

    @post_load
    def make(self, data, **kwargs):
        return models.Funding(**data)


class CardSchema(Schema):
    created = fields.Str()
    cvv = fields.Str()
    funding = fields.Nested(FundingAccountSchema())
    exp_month = fields.Str()
    exp_year = fields.Str()
    hostname = fields.Str()
    last_four = fields.Str()
    memo = fields.Str()
    pan = fields.Str()
    spend_limit = fields.Integer()
    spend_limit_duration = fields.Str()
    state = fields.Str()
    token = fields.Str()
    type = fields.Str()

    @post_load
    def make(self, data, **kwargs):
        return models.Card(**data)


class EventSchema(Schema):
    amount = fields.Integer()
    created = fields.Str()
    result = fields.Str()
    token = fields.Str()
    type = fields.Str()

    @post_load
    def make(self, data, **kwargs):
        return models.Event(**data)


class MerchantSchema(Schema):
    acceptor_id = fields.Str()
    city = fields.Str()
    country = fields.Str()
    descriptor = fields.Str()
    mcc = fields.Str()
    state = fields.Str()

    @post_load
    def make(self, data, **kwargs):
        return models.Merchant(**data)


class TransactionSchema(Schema):
    amount = fields.Integer()
    card = fields.Nested(CardSchema())
    created = fields.Str()
    events = fields.List(fields.Nested(EventSchema()))
    funding = fields.List(fields.Nested(FundingSchema()))
    merchant = fields.Nested(MerchantSchema())
    result = fields.Str()
    settled_amount = fields.Integer()
    status = fields.Str()
    token = fields.Str()

    @post_load
    def make(self, data, **kwargs):
        return models.Transaction(**data)
