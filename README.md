### Hexlet tests and linter status:

[![Actions Status](https://github.com/VictorVangeli/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/VictorVangeli/python-project-83/actions)

Ссылка на ресурс: https://page-analyzer.pupsidian.ru

## Для локального запуска проекта:
1. Создайте `.env` из `.env.example` (сделайте дубликат и в названии оставьте `.env`). Раскомментируйте строку с локальным доменом;
2. В `.env` замените значение переменной SECRET_KEY;
3. Создайте `settings.yaml` из `settings.example.yaml` (сделайте дубликат и в названии оставьте `settings.yaml`). Файл находится по пути `/config/settings.example.yaml`;
4. В `settings.yaml` по необходимости скорректируйте значения полей `DOMAIN` и `DATABASE_URL`;
5. Убедитесь, что у вас на устройстве установлен и запущен `Docker`. Подробную информацию по установке и запуску вы можете найти [тут](https://docs.docker.com/engine/install/)
5. В `docker-compose-dev.yaml` приведите в соответствие значение поля `port` для контейнера `pa_db`, если вы изменяли его в `settings.yaml`;
6. В `pytest.ini` приведите в соответствие значение поля `addopts`, в `settings.yaml`;
7. Выполните команду в терминале `make install_dev`, чтобы установить все зависимости;
8. Откройте `docker-compose-dev.yaml` и запустите контейнер `pa_db`, чтобы запустить БД и получить к ней доступ;
9. Выполните команду в терминале `make run_dev` (`make start` тоже сработает), чтобы запустить приложение;
10. Выполните команду в терминале `make test_dev`, чтобы запустить тестирование.

## Как проводить тестирование:
1. Проконтролируйте, что файл `10_application_test.py` находится по пути `/tests/10_application_test.py` - при необходимости создайте соответствующую директорию и поместите его туда:
2. Откройте файл `10_application_test.py`;
3. Выберите интересующую вас функцию для тестирования и раскомментируйте ее. Обратите внимание, что в случае, если будет раскомментированно более 1-й функции - они могут поломаться, из-за того, что каждая функция требует, чтобы в БД не было данных, которые могли быть получены из других функций.
4. Выполните команду в терминале `make test_dev`
5. После выполнения функции - закомментируйте ее;
6. Повторите этот цикл необходимое количество раз.
