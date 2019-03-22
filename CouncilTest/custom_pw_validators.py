from django.contrib.auth.password_validation import (
    CommonPasswordValidator, NumericPasswordValidator, UserAttributeSimilarityValidator, MinimumLengthValidator
)
import os
import re
from difflib import SequenceMatcher

from django.core.exceptions import (
    FieldDoesNotExist, ValidationError,
)
from django.utils.translation import gettext as _, ngettext

#'password_mismatch': _("두 비밀번호가 일치하지 않습니다. 다시 확인해 주세요"),
#        'password_too_short' : _("비밀번호는 8글자 이상으로 설정해야 합니다"),
#        'password_too_common': _("비밀번호가 너무 단순합니다"),
#        'password_entirely_numeric': _("숫자만으로 비밀번호를 설정하실 수 없습니다"),

class CommonPasswordValid(CommonPasswordValidator):
    def validate(self, password, user=None):
        if password.lower().strip() in self.passwords:
            raise ValidationError(
                _("비밀번호가 너무 단순합니다."),
                code='password_too_common',
            )

    def get_help_text(self):
        return _("문자와 숫자를 조합하세요.")


class NumericPasswordValid(NumericPasswordValidator):
    def validate(self, password, user=None):
        if password.isdigit():
            raise ValidationError(
                _("숫자만으로 비밀번호를 설정하실 수 없습니다."),
                code='password_entirely_numeric',
            )

    def get_help_text(self):
        return _("문자와 숫자를 조합하세요.")


class UserAttributeSimilarityValid(UserAttributeSimilarityValidator):

    def validate(self, password, user=None):
        if not user:
            return

        for attribute_name in self.user_attributes:
            value = getattr(user, attribute_name, None)
            if not value or not isinstance(value, str):
                continue
            value_parts = re.split(r'\W+', value) + [value]
            for value_part in value_parts:
                if SequenceMatcher(a=password.lower(), b=value_part.lower()).quick_ratio() >= self.max_similarity:
                    try:
                        verbose_name = str(user._meta.get_field(attribute_name).verbose_name)
                    except FieldDoesNotExist:
                        verbose_name = attribute_name
                    raise ValidationError(
                        _("비밀번호가 %(verbose_name)s와 너무 유사합니다."),
                        code='password_too_similar',
                        params={'verbose_name': verbose_name},
                    )

    def get_help_text(self):
        return _("비밀번호는 다른 정보와 유사하게 설정할 수 없습니다.")


class MinimumLengthValid(MinimumLengthValidator):
    def validate(self, password, user=None):
        if len(password) < self.min_length:
            raise ValidationError(
                ngettext(
                    "비밀번호가 너무 짧습니다. %(min_length)d 글자 이상으로 설정하세요.",
                    "비밀번호가 너무 짧습니다. %(min_length)d 글자 이상으로 설정하세요.",
                    self.min_length
                ),
                code='password_too_short',
                params={'min_length': self.min_length},
            )

    def get_help_text(self):
        return ngettext(
            "비밀번호는 최소 %(min_length)d 글자 이상이어야 합니다.",
            "비밀번호는 최소 %(min_length)d 글자 이상이어야 합니다.",
            self.min_length
        ) % {'min_length': self.min_length}