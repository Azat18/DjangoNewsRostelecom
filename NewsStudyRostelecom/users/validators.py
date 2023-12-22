from django.core.validators import ValidationError
from django.utils.translation import gettext_lazy as _

def russian_email(email):
    allowed_domains = ['@mail.ru',
                       '@bk.ru',
                       '@yandex.ru']
    if not any(domain in email for domain in allowed_domains):
        raise ValidationError(
            _("%(email) has not allowed domain"),params={'email':email}
        )