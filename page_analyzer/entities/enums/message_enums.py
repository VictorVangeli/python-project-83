from enum import Enum


class ErrorsEnum(Enum):
    MISSING_URL = "Данные отсутствуют"
    INCORRECT_LENGTH_OF_URL = "Длина превышает допустимый лимит в 255 символов"
    INCORRECT_URL = "Некорректный URL"
    EXISTING_URL = 'Страница уже существует'
    ERROR_CHECK = 'Произошла ошибка при проверке'
    

class MessageEnum(Enum):
    CONFIRM_ADD_URL = "Страница успешно добавлена"
    SUCCESS_CHECK = "Страница успешно проверена"