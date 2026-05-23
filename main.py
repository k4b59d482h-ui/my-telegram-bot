async def main():
    scheduler = AsyncIOScheduler()
    
    # ТЕСТ: Бот надішле опитування ВІДРАЗУ, як тільки увімкнеться на Render
    await send_daily_poll()
    
    # Твій звичайний розклад (поки залишаємо як є)
    scheduler.add_job(send_daily_poll, "cron", hour=13, minute=45)
    
    scheduler.start()
    logging.info("Планувальк успішно запущено.")
    
    # Піднімаємо сервер для Render
    app = web.Application()
    app.router.add_get('/', handle)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 10000)
    await site.start()
    
    # Запуск бота
    await dp.start_polling(bot)
