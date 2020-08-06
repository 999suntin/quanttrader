#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging

_logger = logging.getLogger(__name__)


class StrategyManager(object):
    def __init__(self, config, strat_dict, broker, order_manager, position_manager, data_board):
        """
        current design:
        let position manager to track total positions
        let strategy manager to track strategy position for each strategy
        """
        self._config = config
        self._broker = broker
        self._order_manager = order_manager    # get sid from
        self._position_manager = position_manager
        self._data_board = data_board
        self._strategy_id = 1
        self._strategy_dict = {}            # sid ==> strategy
        self._multiplier_dict = {}          # symbol ==> multiplier
        self._tick_strategy_dict = {}  # sym -> list of strategy

        self.load_strategy(strat_dict)

    def load_strategy(self, strat_dict):
        strategy_id = 1     # 0 is mannual discretionary trade, or not found
        for k, v in strat_dict.items():
            v.id = self._strategy_id
            v.name = k
            self._strategy_dict[strategy_id] = v
            strategy_id += 1

            v.set_params(self._config['strategy'][v.name]['params'])        # dict
            v.set_symbols(self._config['strategy'][v.name]['symbols'])      # list
            v.on_init(self._broker, self._data_board, self._position_manager)
            for sym in v.symbols:
                ss = sym.split(' ')
                if ss[-1].isdigit():  # multiplier
                    sym = ' '.join(ss[:-1])
                    self._multiplier_dict[sym] = int(ss[-1])

                # now sym doesn't have multiplier
                if sym in self._tick_strategy_dict:
                    self._tick_strategy_dict[sym].append(v.id)
                else:
                    self._tick_strategy_dict[sym] = [v.id]
                if sym in self._broker.market_data_subscription_reverse_dict.keys():
                    continue
                else:
                    print(f'add {sym}')
                    self._broker.market_data_subscription_reverse_dict[sym] = -1

            v.active = False
            self._strategy_dict[v.id] = v

    def start_strategy(self, sid):
        self._strategy_dict[sid].on_start()

    def stop_strategy(self, sid):
        self._strategy_dict[sid].on_stop()

    def pause_strategy(self, sid):
        pass

    def flat_strategy(self, sid):
        pass

    def start_all(self):
        pass

    def stop_all(self):
        pass

    def flat_all(self):
        pass

    def cancel_all(self):
        pass

    def on_tick(self, k):
        print(k.full_symbol, k.price, k.size)
        if k.full_symbol in self._tick_strategy_dict:
            # foreach strategy that subscribes to this tick
            s_list = self._tick_strategy_dict[k.full_symbol]
            for sid in s_list:
                if self._strategy_dict[sid].active:
                    self._strategy_dict[sid].on_tick(k)

    def on_position(self, pos):
        pass

    def on_order_status(self, order_event):
        sid = order_event.source
        if sid in self._strategy_dict.keys():
            self._strategy_dict[sid].on_order_status(order_event)
        else:
            _logger.info('strategy manager doesnt hold the oid, possibly from outside of the system')

    def on_cancel(self, oid):
        pass

    def on_fill(self, fill):
        """
        assign fill ordering to order id ==> strategy id
        """
        pass