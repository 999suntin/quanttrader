#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import decimal
import pandas as pd
import json
from datetime import datetime


def retrieve_multiplier_from_full_symbol(full_symbol):
    return 1.0


def read_ohlcv_csv(filepath, adjust=True):
    df = pd.read_csv(filepath, header=0, parse_dates=True, sep=',', index_col=0)
    # df.index = pd.to_datetime(df.index)
    if adjust:
        df['Open'] = df['Adj Close'] / df['Close'] * df['Open']
        df['High'] = df['Adj Close'] / df['Close'] * df['High']
        df['Low'] = df['Adj Close'] / df['Close'] * df['Low']
        df['Volume'] = df['Adj Close'] / df['Close'] * df['Volume']
        df['Close'] = df['Adj Close']

    df = df[['Open', 'High', 'Low', 'Close', 'Volume']]
    return df