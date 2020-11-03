from django.db import models

class User(models.Model):
    objects    = models.Manager()
    account    = models.CharField(max_length = 64, unique = True)
    password   = models.CharField(max_length = 64)
    created_at = models.DateTimeField(auto_now_add = True)
    deleted_at = models.DateTimeField(blank = True)
    is_deleted = models.BooleanField(default = False)

    class Meta:
        db_table = 'users'