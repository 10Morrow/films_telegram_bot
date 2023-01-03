from aiogram import Dispatcher

from .admin_filter import IsAdmin
from .client_filter import SubClient
from .moderator_filter import IsModerator

def setup(dp:Dispatcher):
    dp.filters_factory.bind(IsAdmin)
    dp.filters_factory.bind(SubClient)
    dp.filters_factory.bind(IsModerator)