import pytest


import requests

import privacy_api


@pytest.fixture
def mock_requests(mocker):
    mocker.patch("requests.get")
    mocker.patch("requests.post")
    mocker.patch("requests.put")


@pytest.fixture
def client(mock_requests):
    api_key = ""
    base_url = "https://fake.privacy.com"
    return privacy_api.Privacy(api_key, base_url)


def test_list_cards(client):
    client.list_cards()


def test_list_transactions(client):
    client.list_transactions("all")


def test_list_transactions_raises(client):
    with pytest.raises(ValueError):
        client.list_transactions("")


def test_create_card(client):
    client.create_card("SINGLE_USE")


def test_create_card_raises(client):
    with pytest.raises(ValueError):
        client.create_card("")

    with pytest.raises(ValueError):
        client.create_card("SINGLE_USE", spend_limit_duration="")

    with pytest.raises(ValueError):
        client.create_card("SINGLE_USE", spend_limit_duration="TRANSACTION", state="")


def test_update_card(client):
    client.update_card("")


def test_update_card_raises(client):
    with pytest.raises(ValueError):
        client.update_card("", state="")

    with pytest.raises(ValueError):
        client.update_card("", state="OPEN", spend_limit_duration="")



def test_simulate_authorization(client):
    descriptor = ""
    pan = ""
    amount = 0
    client.simulate_authorization(descriptor, pan, amount)


def test_simulate_void(client):
    token = ""
    amount = 0
    client.simulate_void(token, amount)


def test_simulate_clearing(client):
    token = ""
    amount = 0
    client.simulate_clearing(token, amount)


def test_simulate_return(client):
    descriptor = ""
    pan = ""
    amount = 0
    client.simulate_return(descriptor, pan, amount)
