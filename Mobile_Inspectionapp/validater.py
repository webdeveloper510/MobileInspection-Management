from django.core.exceptions import ValidationError
  
def validate_mail(value):
    if value==None:
        return value
    else:
        raise ValidationError("This field accepts mail id of google only")