from decimal import Decimal

import pandas as pd
import pandas_ta as ta

from hummingbot.data_feed.candles_feed.candles_factory import CandlesFactory
from hummingbot.strategy.directional_strategy_base import DirectionalStrategyBase


class StatisticalArbitrage(DirectionalStrategyBase):
    directional_strategy_name: str = "statistical_arbitrage"
    # Define the trading pair and exchange that we want to use and the csv where we are going to store the entries
    trading_pair_left: str = "ETH-USDT"
    trading_pair: str = "BTC-USDT"
    exchange: str = "binance_perpetual"
    order_amount_usd = Decimal("15")
    leverage = 10
    length = 100

    # Configure the parameters for the position
    zscore_entry: int = -2  #
    zscore_entry_sl: int = -3
    zscore_exit: int = 2
    zscore_exit_sl: int = 3

    candles = [
        CandlesFactory.get_candle(connector=exchange,
                                  trading_pair=trading_pair_left,
                                  interval="1h", max_records=1000),
        CandlesFactory.get_candle(connector=exchange,
                                  trading_pair=trading_pair,
                                  interval="1h", max_records=1000),
    ]
    markets = {exchange: {trading_pair}}

    def get_signal(self):

        candles_df = self.get_processed_df()
        z_score = candles_df.iat[-1, -1]

        if z_score < self.zscore_entry:
            return 0  # short -1
        elif z_score < self.zscore_entry_sl:
            return 0  # stop loss short 1
        elif z_score > self.zscore_exit:
            return 0  # long 1
        elif z_score > self.zscore_exit_sl:
            return 0  # stop loss long -1
        else:
            return 0

    def get_processed_df(self):

        candles_df_1 = self.candles[0].candles_df
        candles_df_2 = self.candles[1].candles_df

        df = pd.merge(candles_df_1, candles_df_2, on="timestamp", how='inner', suffixes=('_left', ''))
        hedge_ratio = df["close_left"].tail(self.length).mean() / df["close"].tail(self.length).mean()

        df["spread"] = df["close_left"] - (df["close"] * hedge_ratio)
        df["z_score"] = ta.zscore(df["spread"], length=self.length)

        return df

    def market_data_extra_info(self):

        lines = []
        columns_to_show = ["timestamp", "open", "low", "high", "close", "volume", "z_score"]
        candles_df = self.get_processed_df()
        lines.extend([f"Candles: {self.candles[0].name} | Interval: {self.candles[0].interval}\n"])
        lines.extend(self.candles_formatted_list(candles_df, columns_to_show))
        return lines
