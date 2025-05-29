import re
import urllib


def test_success(page, base_url):
    correct = {
        "code": "200",
        "title": "Хекслет — онлайн-школа программирования, онлайн-обучение "
        "ИТ-профессиям",
        "h1": "Помогли стать программистами 4500+ выпускникам",
        "description": "Хекслет — лучшая школа программирования по версии"
        " пользователей Хабра. Авторские программы обучения с "
        "практикой и готовыми проектами в резюме. Помощь в "
        "трудоустройстве после успешного окончания обучения",
    }

    page.goto(base_url)
    page.locator('input[name="url"]').type("https://ru.hexlet.io")
    page.locator('input[type="submit"]').click()
    assert page.locator("text=Страница успешно добавлена").is_visible()

    print("After submit, current URL:", page.url)
    print(page.content())

    if page.locator("text=Запустить проверку").is_visible():
        page.locator("text=Запустить проверку").click()
        print("After check, current URL:", page.url)
        print(page.content())
    else:
        raise AssertionError("Кнопка 'Запустить проверку' не найдена")

    assert page.locator("text=Страница успешно проверена").is_visible()

    code_selector = 'table[data-test="checks"] > tbody > tr > td:nth-child(2)'
    h1_selector = 'table[data-test="checks"] > tbody > tr > td:nth-child(3)'
    title_selector = 'table[data-test="checks"] > tbody > tr > td:nth-child(4)'
    description_selector = (
        'table[data-test="checks"] > tbody > tr > td:nth-child(5)'
    )

    assert correct["code"] in page.locator(code_selector).text_content()
    assert correct["h1"] in page.locator(h1_selector).text_content()
    assert correct["title"] in page.locator(title_selector).text_content()
    assert (
        correct["description"]
        in page.locator(description_selector).text_content()
    )

    # assert url ends with '/urls/<int:id>'
    u = urllib.parse.urlparse(base_url)
    r = re.escape(u.scheme) + r":\/\/" + re.escape(u.netloc) + r"\/urls\/\d+"
    assert re.search(r, page.url)

    page.goto("/urls")
    status_selector = 'table[data-test="urls"] > tbody > tr > td:nth-child(4)'
    assert "200" in page.locator(status_selector).text_content()


def test_normalize_url(page, base_url):
    page.goto(base_url)
    page.locator('input[name="url"]').type("http://page.com/blog/")
    page.locator('input[type="submit"]').click()
    print(page.content())
    page.wait_for_selector("div.alert-success", timeout=5000)
    assert (
        "Страница успешно добавлена"
        in page.locator("div.alert-success").text_content()
    )

    page.goto(base_url)
    page.locator('input[name="url"]').type("http://page.com/users/1")
    page.locator('input[type="submit"]').click()
    print(page.content())
    page.wait_for_selector("div.alert-danger", timeout=5000)
    assert (
        "Страница уже существует"
        in page.locator("div.alert-danger").text_content()
    )


def test_url_exists_already(page, base_url):
    page.goto(base_url)
    page.locator('input[name="url"]').type("https://www.google.com/")
    page.locator('input[type="submit"]').click()
    assert page.locator("text=Страница успешно добавлена").is_visible()

    page.goto(base_url)
    page.locator('input[name="url"]').type("https://www.google.com/")
    page.locator('input[type="submit"]').click()
    assert page.locator("text=Страница уже существует").is_visible()

    # assert redirect to url '/urls/<int:id>'
    u = urllib.parse.urlparse(base_url)
    r = re.escape(u.scheme) + r":\/\/" + re.escape(u.netloc) + r"\/urls\/\d+"
    assert re.search(r, page.url)

    page.goto("/urls")
    urls_table = 'table[data-test="urls"]'
    assert page.locator(urls_table).count() == 1


def test_url_is_invalid(page, base_url):
    page.goto(base_url)
    page.locator('input[name="url"]').type("httpsss://abcabca@test.ru")
    with page.expect_response("/urls") as response_info:
        page.locator('input[type="submit"]').click()

    resp = response_info.value
    assert resp.status == 422
    assert page.locator("text=Некорректный URL").is_visible()
    assert page.url == urllib.parse.urljoin(base_url, "/urls")


def test_site_is_invalid(page, base_url):
    page.goto(base_url)
    page.locator('input[name="url"]').type("http://wrong.com")
    page.locator('input[type="submit"]').click()
    assert page.locator("text=Страница успешно добавлена").is_visible()

    page.locator("text=Запустить проверку").click()
    assert page.locator("text=Произошла ошибка при проверке").is_visible()
    assert (
        "Im wrong site, you shouldnt have my header"
        not in page.locator('table[data-test="checks"]').text_content()
    )

    page.goto("/urls")
    assert page.locator("text=http://wrong.com").is_visible()
