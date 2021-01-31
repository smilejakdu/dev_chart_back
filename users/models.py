from django.db import models

class User(models.Model):
    email      = models.EmailField(max_length = 200)
    nickname   = models.CharField(max_length = 200)
    password   = models.CharField(max_length = 200)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    class Meta:
        db_table="users"

