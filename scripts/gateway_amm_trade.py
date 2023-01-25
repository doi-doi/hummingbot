import asyncio

from hummingbot.core.event.events import TradeType
from hummingbot.core.gateway.gateway_http_client import GatewayHttpClient
from hummingbot.core.utils.async_utils import safe_ensure_future
from hummingbot.strategy.script_strategy_base import Decimal, ScriptStrategyBase


class GatewayAmmTrade(ScriptStrategyBase):
    """
    This example shows how to execute a swap on Uniswap and poll for the result
    """
    # params
    connector_chain_network = "uniswap_ethereum_goerli"
    address = "0x9FA3156B802eA7ECFe55173Eafc296f509a28777"
    trading_pair = {"WETH-UNI"}
    order_amount = Decimal("0.1")
    side = "SELL"
    # lower than the current price
    limit_price = "1.3"

    markets = {
        connector_chain_network: trading_pair
    }
    create_timestamp = 0
    on_going_task = False

    def on_tick(self):
        if self.create_timestamp <= self.current_timestamp and not self.on_going_task:
            self.on_going_task = True
            safe_ensure_future(self.async_task())

    async def async_task(self):
        base_asset, quote_asset = list(self.trading_pair)[0].split("-")
        connector, chain, network = self.connector_chain_network.split("_")
        if (self.side == "BUY"):
            trade_type = TradeType.BUY
        else:
            trade_type = TradeType.SELL

        self.logger().info(f"POST /amm/price [ side: {self.side}, base: {base_asset}, quote: {quote_asset}, amount: {self.order_amount}, limitPrice: {self.limit_price} ]")

        data = await GatewayHttpClient.get_instance().amm_trade(
            chain,
            network,
            connector,
            self.address,
            base_asset,
            quote_asset,
            trade_type,
            self.order_amount,
            self.limit_price
        )

        self.logger().info(f"{data}")

        pending: bool = True
        while pending is True:
            self.logger().info(f"POST /network/poll [ txHash: {data['txHash']} ]")
            pollData = await GatewayHttpClient.get_instance().get_transaction_status(
                chain,
                network,
                data['txHash']
            )
            transaction_status = pollData.get("txStatus")
            self.logger().info(f"txStatus: {transaction_status}")
            if transaction_status == 1:
                self.logger().info(f"Trade with transaction hash {data['txHash']} has been executed successfully.")
                pending = False
            elif transaction_status in [-1, 0, 2]:
                self.logger().info(f"Trade is pending confirmation, Transaction hash: {data['txHash']}")
                await asyncio.sleep(2)
            else:
                self.logger().info(f"Unknown txStatus: {transaction_status}")
                self.logger().info(f"{pollData}")
                pending = False

        self.create_timestamp = self.current_timestamp
