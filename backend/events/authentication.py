from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError
from .models import EventUser


class EventUserJWTAuthentication(BaseAuthentication):
    """
    Кастомная JWT-аутентификация для модели EventUser.
    Читает заголовок Authorization: Bearer <token>,
    декодирует токен и возвращает экземпляр EventUser.
    """

    def authenticate_header(self, request):
        return 'Bearer realm="api"'

    def authenticate(self, request):
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return None  # анонимный запрос, не ошибка

        token_str = auth_header.split(' ', 1)[1]
        try:
            token = AccessToken(token_str)
            user_id = token['user_id']
            user = EventUser.objects.get(id=user_id)
            return (user, token)
        except (TokenError, KeyError):
            raise AuthenticationFailed('Токен недействителен или истёк.')
        except EventUser.DoesNotExist:
            raise AuthenticationFailed('Пользователь из токена не найден.')
