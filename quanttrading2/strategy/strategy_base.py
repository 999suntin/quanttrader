#!/usr/bin/env python
# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod
from datetime import datetime
from ..order.order_event import OrderEvent
from ..order.order_type import OrderType

class StrategyBase(metaclass=ABCMeta):
    """
    Base strategy class
    """
    def __init__(self, events_engine, data_board=None):
        """
        initialize trategy
        :param symbols:
        :param events_engine:backtest_event_engine or live_event engine that provides queue_.put()
        """
        self.symbols = []
        self._events_engine = events_engine
        self._data_board = data_board
        self.id = -1
        self.name = ''
        self.author = ''
        self.capital = 0.0
        self.cash = 0.0
        self.initialized = False
        self.active = False

    def set_capital(self, capital):
        self.capital = capital
        self.cash = capital

    def set_symbols(self, symbols):
        self.symbols = symbols

    def on_init(self, params_dict=None):
        self.initialized = True

        # set params
        if params_dict is not None:
            for key, value in params_dict.items():
                try:
                    self.__setattr__(key, value)
                except:
                    pass

    def on_start(self):
        self.active = True

    def on_stop(self):
        self.active = False

    def on_tick(self, event):
        """
        Respond to tick
        """
        pass

    def on_bar(self, event):
        """
        Respond to bar
        """
        pass

    def on_order_status(self):
        """
        on order acknowledged
        :return:
        """
        #raise NotImplementedError("Should implement on_order()")
        pass

    def on_cancel(self):
        """
        on order canceled
        :return:
        """
        pass

    def on_fill(self):
        """
        on order filled
        :return:
        """
        pass

    def place_order(self, o):
        o.source = self.id         # identify source
        o.create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        if (self.active):
            self._events_engine.put(o)

    def adjust_position(self, sym, size_from, size_to):
        o = OrderEvent()
        o.full_symbol = sym
        o.order_type = OrderType.MARKET
        o.order_size = size_to - size_from
        self.place_order(o)

    def cancel_order(self, oid):
        pass

    def cancel_all(self):
        """
        cancel all standing orders from this strategy id
        :return:
        """
        pass

class Strategies(StrategyBase):
    """
    Strategies is a collection of strategy
    Usage e.g.: strategy = Strategies(strategyA, DisplayStrategy())
    """
    def __init__(self, *strategies):
        self._strategies_collection = strategies

    def on_tick(self, event):
        for strategy in self._strategies_collection:
            strategy.on_tick(event)
