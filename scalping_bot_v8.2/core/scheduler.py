# core/scheduler.py – Contrôle horaire des sessions de trading

from datetime import datetime
import pytz
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import config


def is_in_trading_hours():
    if getattr(config, "DISABLE_HOUR_FILTER", False):
        return True
    now = datetime.utcnow().strftime('%H:%M')
    return config.TRADING_HOUR_START <= now <= config.TRADING_HOUR_END

