import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.bot import DefaultBotProperties

from handlers import router
import config
from auth import user_manager
import mc_server_manager
import upload_to_remote

async def main():
    #test config
    config.print_config()
    #запуск фоновых процессов
    await user_manager.start_async()
    await mc_server_manager.start_async()
    await upload_to_remote.start_sync_remote()

    bot = Bot(token=config.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    logging.basicConfig(level=logging.ERROR)
    asyncio.run(main())