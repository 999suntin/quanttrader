#!/usr/bin/env python
# -*- coding: utf-8 -*-
from quanttrading2.strategy.strategy_base import StrategyBase
from quanttrading2.data.tick_event import TickType
from quanttrading2.order.order_event import OrderEvent
from quanttrading2.order.order_status import OrderStatus
from quanttrading2.order.order_type import OrderType
import numpy as np
import logging

_logger = logging.getLogger(__name__)


class MovingAverageCrossStrategy(StrategyBase):
    """
    EMA
    """
    def __init__(self):
        super(MovingAverageCrossStrategy, self).__init__()
        self.last_bid = -1
        self.last_ask = -1
        self.last_trade = -1
        self.ema = -1
        self.last_time = -1
        self.G = 20
        _logger.info('MovingAverageCrossStrategy initiated')

    def on_tick(self, k):
        symbol = self.symbols[0]
        if k.tick_type == TickType.BID:
            self.last_bid = k.bid_price_L1
        if k.tick_type == TickType.ASK:
            self.last_bid = k.ask_price_L1
        elif k.tick_type == TickType.TRADE:
            self.last_trade = k.price
            if self.ema == -1:
                self.ema = self.last_trade
                self.last_time = k.timestamp
            else:
                time_elapsed = (k.timestamp - self.last_time).total_seconds()
                alpha = 1- np.exp(-time_elapsed/self.G)
                self.ema += alpha * (self.last_trade - self.ema)
                self.last_time = k.timestamp

            if k.price > self.ema:    # buy at bid
                if self._position_manager.get_position_size(symbol) == 0:
                    if self._order_manager.has_standing_order():
                        return
                    else:
                        o = OrderEvent()
                        o.full_symbol = symbol
                        o.order_type = OrderType.LIMIT
                        o.limit_price = self.last_bid
                        o.order_size = 1
                        _logger.info('MovingAverageCrossStrategy long order placed')
                        self.place_order(o)
            else:   # exit long position
                if (self._position_manager.get_position_size(symbol) == 1):
                    if self._order_manager.has_standing_order():
                        return
                    else:
                        o = OrderEvent()
                        o.full_symbol = symbol
                        o.order_type = OrderType.LIMIT
                        o.limit_price = self.last_ask
                        o.order_size = -1
                        _logger.info('MovingAverageCrossStrategy flat order placed')
                        self.place_order(o)
