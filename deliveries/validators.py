from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


@deconstructible
class FileSizeValidator:
    message = _("The maximum allowed size is %(max_mb_size)sMB.")
    code = "invalid_size"

    def __init__(self, max_mb_size: int):
        if max_mb_size <= 0:
            raise ValueError("The max MB size must be greater than 0")
        self.max_mb_size = max_mb_size

    def __call__(self, value):
        filesize = value.size

        if filesize > self.max_mb_size * 1024 * 1024:
            raise ValidationError(
                self.message,
                code=self.code,
                params={"max_mb_size": self.max_mb_size},
            )

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__)
            and self.max_mb_size == other.max_mb_size
        )
