# - *- coding: utf- 8 - *-
from aiogram import Dispatcher

from .main_start import dp
from .admin_functions import dp
from .users_refills import dp
from .admin_payments import dp
from .admin_products import dp
from .user_products import dp
from .errors import dp

__all__ = ['dp']
