import json
import os

from privacy_api import schemas


def test_transaction_schema():
    test_data_dir = os.path.join(os.path.dirname(__file__), "data")
    with open(os.path.join(test_data_dir, "example_transaction.json")) as f:
        json_data = json.loads(f.read())
    t = schemas.TransactionSchema().load(json_data)
    expected_token = "00000000-0000-0000-0000-000000000000"
    assert t.token == expected_token
    assert t.funding[0].token == expected_token
    assert t.events[0].token == expected_token
    assert t.card.funding.token == expected_token
    assert t.card.token == expected_token
    assert t.merchant.descriptor == "merchant"
