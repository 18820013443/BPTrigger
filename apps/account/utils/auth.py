
from account.models import Account
from account.serializers import AccountSerializer
from rest_framework.authentication import BaseAuthentication
# from account.models import UserInfo, UserToken
from rest_framework import exceptions
from account.utils.jwt_auth import parse_payload


class UserAuthentication(BaseAuthentication):
    def authenticate(self, request):
        # token = request.query_params.get('token')
        token = request._request.headers['authorization'] if 'authorization' in request._request.headers.keys() else ''
        payload = parse_payload(token)
        if not payload['status']:
            raise exceptions.AuthenticationFailed(payload)
        email = payload['data']['email']
        user = Account.objects.get(email=email)
        roleList = [item.name for item in user.role.all()]
        serializer = AccountSerializer(instance=user)
        payload['user'] = serializer.data
        payload['roles'] = roleList
        payload['avatar'] = 'https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif'
        # 如果想要request.user等于用户对象，此处可以根据payload去数据库中获取用户对象。
        return (payload, token)