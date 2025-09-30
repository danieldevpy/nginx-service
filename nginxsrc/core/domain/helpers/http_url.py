from pydantic import AnyHttpUrl
from typing import Any


class PreservedHttpUrl(AnyHttpUrl):
    """
    Subclasse de AnyHttpUrl que preserva a barra final.
    """
    @classmethod
    def __get_validators__(cls):
        yield from super().__get_validators__()
        yield cls.preserve_trailing_slash

    @classmethod
    def preserve_trailing_slash(cls, value: Any) -> str:
        # transforma para string se não forq
        url_str = str(value)
        # mantém barra final se existir no input original
        if value.endswith("/") and not url_str.endswith("/"):
            url_str += "/"
        return url_str
