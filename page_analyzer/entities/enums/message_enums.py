from enum import Enum


class ErrorsEnum(Enum):
    MISSING_URL =  "Данные отсутствуют"
    INCORRECT_LENGTH_OF_URL = "Длина превышает допустимый лимит в 255 символов"
    INCORRECT_URL = "Ссылка некорректна"
    EXISTING_URL = 'Ссылка уже существует'
    
class MessageEnum(Enum):
    CONFIRM_ADD_URL = "URL успешно добавлен!"