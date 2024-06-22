from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ValidationError


def generate_token(user):
    return default_token_generator.make_token(user)


def verify_token(user,token):
    if default_token_generator.check_token(user,token):
        return user
    else:
        raise ValidationError('Invalid token')
    
