from django.db import models

class Posting(models.Model):
    objects    = models.Manager()
    user       = models.ForeignKey('user.User', on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)
    content    = models.CharField(max_length = 1024)
    deleted_at = models.DateTimeField(null = True, blank = True)
    is_deleted = models.BooleanField(default = False)

    class Meta:
        db_table = 'postings'