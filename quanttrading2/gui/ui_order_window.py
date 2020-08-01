#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtWidgets, QtGui
from ..order.order_event import OrderEvent

class OrderWindow(QtWidgets.QTableWidget):
    '''
    Order Monitor
    '''
    order_status_signal = QtCore.pyqtSignal(type(OrderEvent()))

    def __init__(self, order_manager, broker, parent=None):
        super(OrderWindow, self).__init__(parent)

        self.header = ['OrderID',
                       'Symbol',
                       'Name',
                       'Security_Type',
                       'Direction',
                       'Order_Flag',
                       'Price',
                       'Quantity',
                       'Filled',
                       'Status',
                       'Order_Time',
                       'Cancel_Time',
                       'Exchange',
                       'Account',
                       'Source']

        self.init_table()

        self._orderids = []
        self._order_manager = order_manager
        self._broker = broker
        self.order_status_signal.connect(self.update_table)

    def init_table(self):
        col = len(self.header)
        self.setColumnCount(col)

        self.setHorizontalHeaderLabels(self.header)
        self.setEditTriggers(self.NoEditTriggers)
        self.verticalHeader().setVisible(False)
        self.setAlternatingRowColors(True)
        self.setSortingEnabled(False)

        self.itemDoubleClicked.connect(self.cancel_order)

    def update_table(self, order_status_event):
        '''
        If order id exist, update status
        else append one row
        '''
        update = self._order_manager.on_order_status(order_status_event)

        if (update):
            if order_status_event.client_order_id in self._orderids:
                row = self._orderids.index(order_status_event.client_order_id)
                self.item(row, 9).setText(order_status_event.order_status.name)
            else:  # including empty
                self._orderids.insert(0, order_status_event.client_order_id)
                self.insertRow(0)
                self.setItem(0, 0, QtWidgets.QTableWidgetItem(str(order_status_event.client_order_id)))
                self.setItem(0, 1, QtWidgets.QTableWidgetItem(order_status_event.full_symbol))
                self.setItem(0, 2, QtWidgets.QTableWidgetItem(""))
                self.setItem(0, 3, QtWidgets.QTableWidgetItem(""))
                self.setItem(0, 4, QtWidgets.QTableWidgetItem(str(self._lang_dict['Long'] if self._order_manager.order_dict[order_status_event.client_order_id].order_size > 0 else self._lang_dict['Short'])))
                self.setItem(0, 5, QtWidgets.QTableWidgetItem(self._order_manager.order_dict[order_status_event.client_order_id].order_flag.name))
                self.setItem(0, 6, QtWidgets.QTableWidgetItem(str(self._order_manager.order_dict[order_status_event.client_order_id].limit_price)))
                self.setItem(0, 7, QtWidgets.QTableWidgetItem(str(self._order_manager.order_dict[order_status_event.client_order_id].order_size)))
                self.setItem(0, 8, QtWidgets.QTableWidgetItem(str(self._order_manager.order_dict[order_status_event.client_order_id].fill_size)))
                self.setItem(0, 9, QtWidgets.QTableWidgetItem(self._order_manager.order_dict[order_status_event.client_order_id].order_status.name))
                self.setItem(0, 10, QtWidgets.QTableWidgetItem(self._order_manager.order_dict[order_status_event.client_order_id].create_time))
                self.setItem(0, 11, QtWidgets.QTableWidgetItem(self._order_manager.order_dict[order_status_event.client_order_id].cancel_time))
                self.setItem(0, 12, QtWidgets.QTableWidgetItem(''))
                self.setItem(0, 13, QtWidgets.QTableWidgetItem(self._order_manager.order_dict[order_status_event.client_order_id].account))
                self.setItem(0, 14, QtWidgets.QTableWidgetItem(self._order_manager.order_dict[order_status_event.client_order_id].source))

    def update_order_status(self, client_order_id, order_status):
        row = self._orderids.index(client_order_id)
        self.item(row, 9).setText(order_status.name)

    def cancel_order(self,mi):
        row = mi.row()
        order_id = self.item(row, 0).text()
        self._broker.cancel_order(order_id)

