from django.core.exceptions import ValidationError
import jwt
from django.conf import settings
from datetime import timedelta, datetime,timezone
from .models import User

def generate_token(user):
    current_time = datetime.now(timezone.utc)
    payload = {
        'user_id': user.id,
        'exp': current_time + timedelta(hours=24),
        'iat': current_time - timedelta(seconds=10) 
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return token


def verify_token(token):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        user_id = payload.get('user_id')
        user = User.objects.get(id=user_id)
        return user
    except :
        raise ValidationError('Token has expired')