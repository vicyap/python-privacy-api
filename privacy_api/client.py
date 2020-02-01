"""Client module for privacy.com API."""
from typing import Any, Dict, Optional

import requests


class Privacy:
    """privacy.com API client."""

    def __init__(self, api_key: str, base_url: str):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {"Authorization": f"api-key {self.api_key}"}

    def list_cards(
        self,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        begin: Optional[str] = None,
        end: Optional[str] = None,
        card_token: Optional[str] = None,
    ) -> Dict[str, Any]:
        """List Cards.

        Args:
            page: For pagination. The default is one.
            page_size: For pagination. The default value page size is 50 and
                the maximum is 1,000.
            begin:  Date string in the form YYYY-MM-DD, only cards created
                after the specified date will be included.
            end: Date string in the form YYYY-MM-DD, only cards created before
                the specified date will be included.
            card_token: Returns a specific card.

        Returns:
            The JSON response.
        """
        params = {
            "page": page,
            "page_size": page_size,
            "begin": begin,
            "end": end,
            "card_token": card_token,
        }
        url = self.base_url + "/v1/card"
        resp = requests.get(url, headers=self.headers, params=params)
        resp.raise_for_status()
        return resp.json()

    def list_transactions(
        self,
        approval_status: str = "all",
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        begin: Optional[str] = None,
        end: Optional[str] = None,
        card_token: Optional[str] = None,
        transaction_token: Optional[str] = None,
    ) -> Dict[str, Any]:
        """List Transactions.

        Args:
            approval_status: Can be approvals, declines or all.
            page: For pagination. The default is one.
            page_size: For pagination. The default value page size is 50 and
                the maximum is 1,000.
            begin:  Date string in the form YYYY-MM-DD, only cards created
                after the specified date will be included.
            end: Date string in the form YYYY-MM-DD, only cards created before
                the specified date will be included.
            card_token: Filters transactions associated with a specific card.
            transaction_token: Returns a specific transaction.

        Returns:
            The JSON response.
        """
        allowed_approval_statuses = {"approvals", "declines", "all"}
        if approval_status not in allowed_approval_statuses:
            raise ValueError(
                f"approval_status='{approval_status}' must be in {allowed_approval_statuses}"
            )

        params = {
            "page": page,
            "page_size": page_size,
            "begin": begin,
            "end": end,
            "card_token": card_token,
            "transaction_token": transaction_token,
        }
        url = self.base_url + f"/v1/transaction/{approval_status}"
        resp = requests.get(url, headers=self.headers, params=params)
        resp.raise_for_status()
        return resp.json()

    def create_card(
        self,
        card_type: str,
        memo: Optional[str] = None,
        spend_limit: Optional[str] = None,
        spend_limit_duration: Optional[str] = None,
        state: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Create Card.

        Args:
            memo: Friendly name to identify the card.
            card_type: SINGLE_USE, MERCHANT_LOCKED, UNLOCKED.
            spend_limit: Amount (in cents) to limit approved authorizations.
                Transaction requests above the spend limit will be declined.
            spend_limit_duration: TRANSACTION, MONTHLY, ANNUALLY, FOREVER.
            state: OPEN, PAUSED.

        Returns:
            The JSON response.
        """

        allowed_card_types = {"SINGLE_USE", "MERCHANT_LOCKED", "UNLOCKED"}
        if card_type not in allowed_card_types:
            raise ValueError(f"card_type='{card_type}' must be in {allowed_card_types}")

        allowed_spend_limit_durations = {"TRANSACTION", "MONTHLY", "ANNUALLY", "FOREVER"}
        if spend_limit_duration is not None and spend_limit_duration not in allowed_spend_limit_durations:
            raise ValueError(
                f"spend_limit_duration='{spend_limit_duration}' must be in {allowed_spend_limit_durations}"
            )

        allowed_states = {"OPEN", "PAUSED"}
        if state is not None and state not in allowed_states:
            raise ValueError(f"state='{state}' must be in {allowed_states}")

        data = {"type": card_type}
        if memo:
            data["memo"] = memo
        if spend_limit:
            data["spend_limit"] = spend_limit
        if spend_limit_duration:
            data["spend_limit_duration"] = spend_limit_duration
        if state:
            data["state"] = state

        url = self.base_url + "/v1/card"
        resp = requests.post(url, headers=self.headers, json=data)
        resp.raise_for_status()
        return resp.json()

    def update_card(
        self,
        card_token: str,
        state: Optional[str] = None,
        memo: Optional[str] = None,
        spend_limit: Optional[str] = None,
        spend_limit_duration: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Update Card.

        Updates the specified properties of the card. Unsupplied properties
        will remain unchanged.
        Note: setting a card to a CLOSED state is a final action that cannot be
        undone.

        Args:
            card_token: The unique token of the card to update.
            state: OPEN, PAUSED, CLOSED.
            memo: Friendly name to identify the card.
            spend_limit: Amount (in cents) to limit approved authorizations.
                Transaction requests above the spend limit will be declined.
            spend_limit_duration: TRANSACTION, MONTHLY, ANNUALLY, FOREVER.

        Returns:
            The JSON response.
        """
        allowed_states = {"OPEN", "PAUSED", "CLOSED"}
        if state is not None and state not in allowed_states:
            raise ValueError(f"state='{state}' must be in {allowed_states}")

        allowed_spend_limit_durations = {"TRANSACTION", "MONTHLY", "ANNUALLY", "FOREVER"}
        if spend_limit_duration is not None and spend_limit_duration not in allowed_spend_limit_durations:
            raise ValueError(
                f"spend_limit_duration='{spend_limit_duration}' must be in {allowed_spend_limit_durations}"
            )

        data = {"card_token": card_token}
        if state:
            data["state"] = state
        if memo:
            data["memo"] = memo
        if spend_limit:
            data["spend_limit"] = spend_limit
        if spend_limit_duration:
            data["spend_limit_duration"] = spend_limit_duration

        url = self.base_url + "/v1/card"
        resp = requests.put(url, headers=self.headers, json=data)
        resp.raise_for_status()
        return resp.json()

    def simulate_authorization(self, descriptor: str, pan: str, amount: int) -> str:
        """Simulate Authorization (Sandbox Only).

        Simulates an authorization request from the payment network as if it
        came from a merchant acquirer.

        Args:
            descriptor: Merchant descriptor.
            pan: 16 digit card number.
            amount: Amount (in cents) to authorize.

        Returns:
            A unique token to reference this transaction with later calls to
            void or clear the authorization.
        """
        data = {"descriptor": descriptor, "pan": pan, "amount": amount}
        url = self.base_url + "/v1/simulate/authorize"
        resp = requests.post(url, headers=self.headers, json=data).json()
        resp.raise_for_status()
        return resp.json()["token"]

    def simulate_void(self, token: str, amount: int) -> None:
        """Simulate Void (Sandbox Only).

        Voids an existing, uncleared (aka pending) authorization.

        Args:
            token: The transaction token returned from the
                /v1/simulate/authorize response.
            amount: Amount (in cents) to void. Typically this will match the
                original authorization, but may be less.
        """
        data = {"token": token, "amount": amount}
        url = self.base_url + "/v1/simulate/void"
        resp = requests.post(url, headers=self.headers, json=data)
        resp.raise_for_status()

    def simulate_clearing(self, token: str, amount: int) -> None:
        """Simulate Clearing (Sandbox Only).

        Clears an existing authorization. After this event, the transaction is
        no longer pending.

        Args:
            token: The transaction token returned from the
                /v1/simulate/authorize response
            amount: Amount (in cents) to void. Typically this will match the
                original authorization, but may be less.
        """
        data = {"token": token, "amount": amount}
        url = self.base_url + "/v1/simulate/clearing"
        resp = requests.post(url, headers=self.headers, json=data)
        resp.raise_for_status()

    def simulate_return(self, descriptor: str, pan: str, amount: int) -> str:
        """Simulate Return (Sandbox Only).

        Returns (aka refunds) an amount back to a card. Returns are cleared
        immediately and do not spend time in a "pending" state.

        Args:
            descriptor: Merchant descriptor.
            pan: 16 digit card number.
            amount: Amount (in cents) to return to the card.

        Returns:
            A unique token to reference this transaction.
        """
        data = {"descriptor": descriptor, "pan": pan, "amount": amount}
        url = self.base_url + "/v1/simulate/return"
        resp = requests.post(url, headers=self.headers, json=data)
        resp.raise_for_status()
        return resp.json()["token"]
