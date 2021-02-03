from django.db import models
from django_jsonfield_backport.models import JSONField

class User(models.Model):
    email      = models.EmailField(max_length = 200)
    nickname   = models.CharField(max_length = 200)
    password   = models.CharField(max_length = 200)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    python     = models.BooleanField(default = False , null=True)
    javascript = models.BooleanField(default = False , null=True)
    java       = models.BooleanField(default = False , null=True)
    php        = models.BooleanField(default = False , null=True)
    c          = models.BooleanField(default = False , null=True)
    c_plus     = models.BooleanField(default = False , null=True)
    spring     = models.BooleanField(default = False , null=True)
    django     = models.BooleanField(default = False , null=True)
    flask      = models.BooleanField(default = False , null=True)
    express    = models.BooleanField(default = False , null=True)
    react      = models.BooleanField(default = False , null=True)
    vue        = models.BooleanField(default = False , null=True)
    laravel    = models.BooleanField(default = False , null=True)

    class Meta:
        db_table = "users"

