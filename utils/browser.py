import asyncio
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError


async def check_site() -> tuple[bool, str]:
    """
    Выполняет проверку сайта.

    :return: Кортеж (успех: bool, сообщение: str)
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        try:
            # 1. Открываем сайт и ждем загрузки
            await page.goto("https://xn--b1adekn9bg8fe.xn--p1ai/", timeout=30000)
            # Ждем 3 секунды, как было запрошено
            await page.wait_for_timeout(3000)

            # 2. Ищем и закрываем модальное окно выбора региона, если оно есть
            # Используем более надежный селектор для кнопки закрытия
            close_button_selector = 'button[aria-label="Закрыть"]'
            booking_frame = page.frame_locator('#widgetBookingReservations')
            target_button = booking_frame.locator('.booking-form-primary-button')
            try:
                # Ждем появления кнопки не более 5 секунд и нажимаем
                await page.locator(close_button_selector).click(timeout=5000)
            except PlaywrightTimeoutError:
                # Если кнопка не появилась за 5 секунд, это не ошибка.
                # Просто логируем это и продолжаем.
                print("Модальное окно с не появилось, идем дальше.")

            # 3. Ищем кнопку "Подобрать номер" и нажимаем на нее
            # get_by_role - более надежный способ, чем поиск по тексту
            try:
                await target_button.wait_for(state="visible", timeout=15000)
                await target_button.click()
                
                print("Кнопка во фрейме успешно нажата!")

            except PlaywrightTimeoutError:
                return False, "❗️❗️❗️ Ошибка: Не удалось найти кнопку внутри фрейма виджета."

            # 4. Нажимаем на первую доступную кнопку "Выбрать".
            # Playwright автоматически дождется появления этой кнопки.
            await booking_frame.get_by_role("button", name="Выбрать").first.click()

            # 5. Ждем появления кнопки "Забронировать" и проверяем ее видимость.
            try:
                # Ждем до 10 секунд, пока кнопка не станет видимой.
                await booking_frame.get_by_role("button", name="Забронировать").first.wait_for(state="visible", timeout=10000)
                await browser.close()
                return True, "Проверка прошла успешно! Кнопка 'Забронировать' найдена."
            except PlaywrightTimeoutError:
                await browser.close()
                return False, "❗️❗️❗️ Ошибка: Кнопка 'Забронировать' не найдена после нажатия на 'Выбрать'."

        except Exception as e:
            await browser.close()
            # Возвращаем понятное сообщение об ошибке
            error_message = f"❗️❗️❗️На одном из этапов произошла ошибка: {type(e).__name__}\n{str(e)}"
            return False, error_message