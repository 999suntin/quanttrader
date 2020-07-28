#!/usr/bin/env python
# -*- coding: utf-8 -*-
from enum import Enum

class OrderStatus(Enum):
    UNKNOWN = 0
    NEWBORN = 1              # in use
    PENDING_SUBMIT = 2
    SUBMITTED = 3           # in use
    ACKNOWLEDGED = 4        # in use
    PARTIALLY_FILLED = 5
    FILLED = 6              # in use
    PENDING_CANCEL = 7
    CANCELED = 8            # in use
    API_PENDING = 10
    API_CANCELLED = 11
    ERROR = 12
