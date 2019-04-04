"""
自定义的异常
"""
from builtins import Exception


class LongUrlFormatException(Exception):
    """
    当长链接不合法时抛出
    """
    def __init__(self, message, code):
        self.message = message
        self.code = code

    def __str__(self):
        return self.message


class CharSetTimeOut(Exception):
    """
    当尝试生成短链接key次数超过限制时抛出
    """
    def __init__(self, message, code):
        self.message = message
        self.code = code

    def __str__(self):
        return self.message


class ShortUrlAlreadyExist(Exception):
    """
    当短链接已存在时抛出
    """
    def __init__(self, message, code):
        self.message = message
        self.code = code

    def __str__(self):
        return self.message


class InputShortUrlError(Exception):
    """
    当用户输入的短链接key不合法时抛出
    """
    def __init__(self, message, code):
        self.message = message
        self.code = code

    def __str__(self):
        return self.message


class ShortUrlTooLongError(Exception):
    """
        短链接key超出最大长度时抛出
    """
    def __init__(self, message, code):
        self.message = message
        self.code = code

    def __str__(self):
        return self.message


class LongUrlTooLongError(Exception):
    """
        长链接超出最大长度时抛出
    """
    def __init__(self, message, code):
        self.message = message
        self.code = code

    def __str__(self):
        return self.message