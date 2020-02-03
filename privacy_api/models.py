"""Data models."""
from attr import attrib, attrs


@attrs
class Card:
    """Card.

    created	An ISO 8601 timestamp for when the card was created
    cvv	        Three digit cvv printed on the back of the card
    funding	See FundingAccount
    exp_month	Two digit (MM) expiry month
    exp_year	Four digit (YYYY) expiry year
    hostname	Hostname of card’s locked merchant (will be empty if not applicable)
    last_four	Last four digits of the card number
    memo	Friendly name to identify the card
    pan	        Sixteen digit card number
    spend_limit	Amount (in cents) to limit approved authorizations.
                Transaction requests above the spend limit will be declined
    spend_limit_duration    TRANSACTION, MONTHLY, ANNUALLY, FOREVER
    state	OPEN, PAUSED, CLOSED
    token	Globally unique identifier
    type	SINGLE_USE, MERCHANT_LOCKED, UNLOCKED
    """

    created = attrib()
    cvv = attrib()
    funding = attrib()
    exp_month = attrib()
    exp_year = attrib()
    hostname = attrib()
    last_four = attrib()
    memo = attrib()
    pan = attrib()
    spend_limit = attrib()
    spend_limit_duration = attrib()
    state = attrib()
    token = attrib()
    type = attrib()


@attrs
class Event:
    """Event.

    A single card transaction may include multiple events that affect the
    transaction state and lifecycle.

    amount  Amount of the transaction event
    created Date and time this event entered the system
    result  APPROVED or decline reason. See below for full enumeration
    token   Globally unique identifier
    type    AUTHORIZATION, AUTHORIZATION_ADVICE, CLEARING, VOID, RETURN
    """

    amount = attrib()
    created = attrib()
    result = attrib()
    token = attrib()
    type = attrib()


@attrs
class FundingAccount:
    """Funding Account.

    account_name    Account name identifying the funding source. In some cases
                    this may be the last four digits of the account number
    token	    Globally unique identifier
    type	    Type of funding source, see enumerations for list
    """

    account_name = attrib()
    token = attrib()
    type = attrib()


@attrs
class Merchant:
    """Merchant.

    acceptor_id Unique identifier to identify the payment card acceptor
    city	City of card acceptor
    country	Country of card acceptor
    descriptor	Short description of card acceptor
    mcc	        Merchant category code
    state	Geographic state of card acceptor
    """

    acceptor_id = attrib()
    city = attrib()
    country = attrib()
    descriptor = attrib()
    mcc = attrib()
    state = attrib()


@attrs
class Funding:
    """Funding.

    funding	A list of objects that describe how this transaction was funded,
                with the amount represented in cents. A reference to the funding
                account for the card that made this transaction may appear here
                and the token will match the token for the funding account in
                the card field. If any promotional credit was used in paying for
                this transaction, its type will be PROMO.
    """

    amount = attrib()
    token = attrib()
    type = attrib()


@attrs
class Transaction:
    """Transaction.

    amount	Authorization amount (in cents) of the transaction. This may change
                over time
    card	See Card schema definition
    created	Date and time when the transaction first occurred
    events	A list of all events that have modified this transaction
    funding     See Funding schema definition
    merchant	See Merchant schema definition
    result	APPROVED or decline reason. See below for full enumeration
    settled_amount	Amount (in cents) of the transaction that has been settled.
                        This may change over time
    status	PENDING, VOIDED, SETTLING, SETTLED, BOUNCED
    token	Globally unique identifier
    """

    amount = attrib()
    card = attrib()
    created = attrib()
    events = attrib()
    funding = attrib()
    merchant = attrib()
    result = attrib()
    settled_amount = attrib()
    status = attrib()
    token = attrib()
