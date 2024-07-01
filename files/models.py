from django.db import models
from users.models import User

class File(models.Model):
    filename = models.CharField(max_length=255)
    file = models.FileField(upload_to='uploads/%Y/%m/%d/')  
    user = models.ForeignKey(User, on_delete=models.CASCADE)  

    def __str__(self):
        return self.filename
