#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtWidgets, QtGui
from ..position.position_event import PositionEvent
from ..order.fill_event import FillEvent

class PositionWindow(QtWidgets.QTableWidget):
    position_signal = QtCore.pyqtSignal(type(PositionEvent()))

    def __init__(self, parent=None):
        super(PositionWindow, self).__init__(parent)

        self.header = ['Symbol',
                       'Name',
                       'Security_Type',
                       'Direction',
                       'Quantity',
                       'Yesterday_Quantity',
                       'Freezed',
                       'Average_Price',
                       'Open_PnL',
                       'Closed_PnL',
                       'Account',
                       'Source',
                       'Time']

        self.init_table()
        self._symbols = []
        self.position_signal.connect(self.update_table)

    def init_table(self):
        col = len(self.header)
        self.setColumnCount(col)

        self.setHorizontalHeaderLabels(self.header)
        self.setEditTriggers(self.NoEditTriggers)
        self.verticalHeader().setVisible(False)
        self.setAlternatingRowColors(True)
        self.setSortingEnabled(False)

    def update_table(self,position_event):
        if position_event.full_symbol in self._symbols:
            row = self._symbols.index(position_event.full_symbol)
            self.setItem(row, 3, QtWidgets.QTableWidgetItem('Long' if position_event.size > 0 else 'Short'))
            self.setItem(row, 4, QtWidgets.QTableWidgetItem(str(abs(position_event.size))))
            self.setItem(row, 5, QtWidgets.QTableWidgetItem(str(position_event.pre_size)))
            self.setItem(row, 6, QtWidgets.QTableWidgetItem(str(position_event.freezed_size)))
            self.setItem(row, 7, QtWidgets.QTableWidgetItem(str(position_event.average_cost)))
            self.setItem(row, 8, QtWidgets.QTableWidgetItem(str(position_event.unrealized_pnl)))
            self.setItem(row, 9, QtWidgets.QTableWidgetItem(str(position_event.realized_pnl)))
            self.setItem(row, 10, QtWidgets.QTableWidgetItem(position_event.account))
            self.setItem(row, 11, QtWidgets.QTableWidgetItem(position_event.api))
            self.setItem(row, 12, QtWidgets.QTableWidgetItem(position_event.timestamp))
        else:
            self._symbols.insert(0, str(position_event.full_symbol))
            self.insertRow(0)
            self.setItem(0, 0, QtWidgets.QTableWidgetItem(position_event.full_symbol))
            self.setItem(0, 3, QtWidgets.QTableWidgetItem('Long' if position_event.size > 0 else 'Short'))
            self.setItem(0, 4, QtWidgets.QTableWidgetItem(str(abs(position_event.size))))
            self.setItem(0, 5, QtWidgets.QTableWidgetItem(str(position_event.pre_size)))
            self.setItem(0, 6, QtWidgets.QTableWidgetItem(str(position_event.freezed_size)))
            self.setItem(0, 7, QtWidgets.QTableWidgetItem(str(position_event.average_cost)))
            self.setItem(0, 8, QtWidgets.QTableWidgetItem(str(position_event.unrealized_pnl)))
            self.setItem(0, 9, QtWidgets.QTableWidgetItem(str(position_event.realized_pnl)))
            self.setItem(0, 10, QtWidgets.QTableWidgetItem(position_event.account))
            self.setItem(0, 11, QtWidgets.QTableWidgetItem(position_event.api))
            self.setItem(0, 12, QtWidgets.QTableWidgetItem(position_event.timestamp))

    def on_fill(self, fill_evnet):
        pass

