# ТЕСТ 1. Успешная регистрация нового пользователя

from test_data import (
    TEST_NAME, TEST_SURNAME, TEST_PHONE, TEST_EMAIL,
    TEST_PASSWORD, TEST_BIRTHDAY, TEST_COUNTRY, TEST_CITY, TEST_SMS
)

# 1. Аргумент "browser" приходит из фикстуры
def test_open_registration_page(browser):
    browser.goto("https://upjet.dev.sandakov.space/auth/sign-in")
    browser.locator("button:has-text('Регистрация')").click()
    browser.wait_for_timeout(3000)
# 2. Заполнение полей
    inputs = browser.locator("input.Input_Input__7YFaq")
    inputs.nth(0).fill(TEST_NAME)      # Имя
    inputs.nth(1).fill(TEST_SURNAME)   # Фамилия
    inputs.nth(2).fill(TEST_PHONE)     # Телефон
    inputs.nth(3).fill(TEST_EMAIL)     # Email
    inputs.nth(4).fill(TEST_PASSWORD)  # Пароль
    inputs.nth(5).fill(TEST_PASSWORD)  # Подтверждение пароля

    browser.wait_for_timeout(1000)

# 3. Клик по чекбоксу "Я даю согласие"
    browser.locator("div.CheckboxPoint_CheckboxPoint__uR6Ur").click()

# 4. Клик по кнопке "Продолжить"
    browser.locator("span:has-text('Продолжить')").click()

# 5. Ждём появления новой формы (заголовок "Подтверждение номера")
    browser.locator("h2:has-text('Подтверждение номера')").wait_for(state="visible", timeout=10000)

# 6. Поле ввода СМС-кода
    sms_input = browser.locator("input.Input_Input__7YFaq")
    sms_input.wait_for(state="visible", timeout=10000)
    sms_input.fill(TEST_SMS)  # используем переменную

    browser.wait_for_timeout(1000)
    browser.locator("button:has-text('Подтвердить')").click()

# 7. Ожидаем переход на шаг завершения регистрации
    browser.locator("h2:has-text('Завершить регистрацию')").wait_for(state="visible", timeout=15000)

# 8. Ждём появления формы "Завершить регистрацию"
    browser.locator("h2:has-text('Завершить регистрацию')").wait_for(state="visible", timeout=15000)

# 9. Получаем инпут рядом с текстом "Дата рождения"
    dob_input = browser.locator("text=Дата рождения").locator("..").locator("input")
# 10. Заполняем дату рождения
    dob_input.fill(TEST_BIRTHDAY)

# 11. Женский пол
    browser.locator("div.CheckInputLayout_CheckInputLayout__Boiom >> text=Женский").click()

# 12. Клик по полю "Страна проживания"
    browser.locator(
        "span:has-text('Страна проживания')"
    ).locator("..").locator(
        "div.InputLayout_InputLayout__InputContainer__KiXjW"
    ).click()

# 13. Ожидание появления поля поиска в выпадающем списке стран
    browser.locator("span:has-text('Поиск')").wait_for(state="visible", timeout=5000)

# 14. Ввод названия страны
    search_input = browser.locator("span:has-text('Поиск')").locator("..").locator("input")
    search_input.fill(TEST_COUNTRY)
    browser.locator(f"div.DropdownItem_DropdownItem__Name__Pk_l8:has-text('{TEST_COUNTRY}')").click()

# 15. Клик по полю "Город проживания"
    browser.locator(
        "span:has-text('Город проживания')"
    ).locator("..").locator(
        "div.InputLayout_InputLayout__InputContainer__KiXjW"
    ).click()

# 16. Вводим город
    browser.locator("input.Input_Input__7YFaq").last.fill(TEST_CITY)
    browser.locator(f"div.DropdownItem_DropdownItem__Name__Pk_l8:has-text('{TEST_CITY}')").click()

# 17. Клик по кнопке "Завершить регистрацию"
    browser.locator(
        "button.Button_Button__qQTgU.Button_Button_size-spacing-cosy-XL__k7QFT.Button_Button_view-fill-black___LyHX:has-text('Завершить регистрацию')"
    ).click()

# 18. ждём появления дашборда/главной страницы после регистрации
    browser.locator("h1:has-text('Мои проекты')").wait_for(state="visible", timeout=10000)


# ТЕСТ 2. Повторная регистрация с существующими номером и email — отображение ошибок 

# 1. аргумент "browser" приходит из фикстуры
def test_registration_with_existing_data(browser): 
    browser.goto("https://upjet.dev.sandakov.space/auth/sign-in")
    browser.locator("button:has-text('Регистрация')").click()
    browser.wait_for_timeout(3000)
# 2. Заполнение полей
    inputs = browser.locator("input.Input_Input__7YFaq")
    inputs.nth(0).fill(TEST_NAME)           # Имя
    inputs.nth(1).fill(TEST_SURNAME)        # Фамилия
    inputs.nth(2).fill(TEST_PHONE)          # Телефон (существующий!)
    inputs.nth(3).fill(TEST_EMAIL)          # Email (существующий!)
    inputs.nth(4).fill(TEST_PASSWORD)       # Пароль
    inputs.nth(5).fill(TEST_PASSWORD)       # Подтверждение пароля

    browser.wait_for_timeout(1000)

# 3. Клик по чекбоксу "Я даю согласие"
    browser.locator("div.CheckboxPoint_CheckboxPoint__uR6Ur").click()

# 4. Клик по кнопке "Продолжить"
    browser.locator("span:has-text('Продолжить')").click()

# 5. Проверяем появление ошибок (ожидаем, что оба сообщения появятся)
    phone_error = browser.locator("span:has-text('Такое значение поля \"номер телефона\" уже существует.')")
    email_error = browser.locator("span:has-text('Такое значение поля \"E-Mail адрес\" уже существует.')")

    phone_error.wait_for(state="visible", timeout=5000)
    email_error.wait_for(state="visible", timeout=5000)

    assert phone_error.is_visible(), "Нет ошибки про существующий номер телефона"
    assert email_error.is_visible(), "Нет ошибки про существующий E-Mail адрес"

# ТЕСТ 3. Успешная авторизация зарегистрированного пользователя

# 1. аргумент "browser" приходит из фикстуры
def test_success_login(browser):
    browser.goto("https://upjet.dev.sandakov.space/auth/sign-in")
    inputs = browser.locator("input.Input_Input__7YFaq")
    inputs.nth(0).fill(TEST_PHONE)         # Телефон — зарегистрированный в первом тесте!
    inputs.nth(1).fill(TEST_PASSWORD)      # Пароль
    browser.locator("button:has-text('Войти в личный кабинет')").click()
# 2. Ждем появления дашборда — значит, логин успешен
    browser.locator("h1:has-text('Мои проекты')").wait_for(state="visible", timeout=10000)


# ТЕСТ 4. Ошибка при авторизации с некорректным логином или паролем
def test_login_with_invalid_credentials(browser):
    browser.goto("https://upjet.dev.sandakov.space/auth/sign-in")
    inputs = browser.locator("input.Input_Input__7YFaq")
    inputs.nth(0).fill("79999567344")       # Некорректный (несуществующий) телефон
    inputs.nth(1).fill("WRONGpassword21!")   # Неверный пароль
    browser.locator("button:has-text('Войти в личный кабинет')").click()

# Ждем появления ошибки "Неверный логин или пароль"
    error = browser.locator("div.UpjetToastContent_UpjetToastContent__Title__euWHj:has-text('Неверный логин или пароль')")
    error.wait_for(state="visible", timeout=5000)
    assert error.is_visible(), "Не появилось сообщение 'Неверный логин или пароль'"

