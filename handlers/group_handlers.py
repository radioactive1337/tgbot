from aiogram import F, types, Router
from aiogram.filters import Command, or_f

from filters.chat_types import ChatType

group_router = Router()
group_router.message.filter(ChatType(['group', 'supergroup']))
# user_group_router.edited_message.filter(ChatTypeFilter(['group', 'supergroup']))


@group_router.message(or_f(Command('stats'), (F.text.lower().contains('stat') | F.text.lower().contains('стат'))))
async def menu_cmd(message: types.Message):
    await message.answer("here is...statistics!")


@group_router.message(~(F.text.lower().contains('test')) | F.text.lower().contains('group'))
async def message(message: types.Message):
    await message.answer('xd')
