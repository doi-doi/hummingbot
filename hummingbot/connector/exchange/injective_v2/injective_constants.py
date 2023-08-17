import sys

from hummingbot.core.api_throttler.data_types import RateLimit
from hummingbot.core.data_type.in_flight_order import OrderState

EXCHANGE_NAME = "injective_v2"

DEFAULT_DOMAIN = ""
TESTNET_DOMAIN = "testnet"

DEFAULT_SUBACCOUNT_INDEX = 0
EXTRA_TRANSACTION_GAS = 20000
DEFAULT_GAS_PRICE = 500000000

EXPECTED_BLOCK_TIME = 1.5
TRANSACTIONS_CHECK_INTERVAL = 3 * EXPECTED_BLOCK_TIME

# Public limit ids
ORDERBOOK_LIMIT_ID = "OrderBookSnapshot"
GET_TRANSACTION_LIMIT_ID = "GetTransaction"
GET_CHAIN_TRANSACTION_LIMIT_ID = "GetChainTransaction"

# Private limit ids
PORTFOLIO_BALANCES_LIMIT_ID = "AccountPortfolio"
SPOT_ORDERS_HISTORY_LIMIT_ID = "SpotOrdersHistory"
SPOT_TRADES_LIMIT_ID = "SpotTrades"
SIMULATE_TRANSACTION_LIMIT_ID = "SimulateTransaction"
SEND_TRANSACTION = "SendTransaction"

NO_LIMIT = sys.maxsize
ONE_SECOND = 1

RATE_LIMITS = [
    RateLimit(limit_id=ORDERBOOK_LIMIT_ID, limit=NO_LIMIT, time_interval=ONE_SECOND),
    RateLimit(limit_id=GET_TRANSACTION_LIMIT_ID, limit=NO_LIMIT, time_interval=ONE_SECOND),
    RateLimit(limit_id=GET_CHAIN_TRANSACTION_LIMIT_ID, limit=NO_LIMIT, time_interval=ONE_SECOND),
    RateLimit(limit_id=PORTFOLIO_BALANCES_LIMIT_ID, limit=NO_LIMIT, time_interval=ONE_SECOND),
    RateLimit(limit_id=SPOT_ORDERS_HISTORY_LIMIT_ID, limit=NO_LIMIT, time_interval=ONE_SECOND),
    RateLimit(limit_id=SPOT_TRADES_LIMIT_ID, limit=NO_LIMIT, time_interval=ONE_SECOND),
    RateLimit(limit_id=SIMULATE_TRANSACTION_LIMIT_ID, limit=NO_LIMIT, time_interval=ONE_SECOND),
    RateLimit(limit_id=SEND_TRANSACTION, limit=NO_LIMIT, time_interval=ONE_SECOND),
]

ORDER_STATE_MAP = {
    "booked": OrderState.OPEN,
    "partial_filled": OrderState.PARTIALLY_FILLED,
    "filled": OrderState.FILLED,
    "canceled": OrderState.CANCELED,
}

ORDER_NOT_FOUND_ERROR_MESSAGE = "order not found"
ACCOUNT_SEQUENCE_MISMATCH_ERROR = "account sequence mismatch"
