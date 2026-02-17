from django.db import models

# Create your models here.
class Professor(models.Model):
    professor_id = models.AutoField(primary_key=True)
    f_name = models.CharField(blank=False, max_length=32)
    l_name = models.CharField(blank=False, max_length=32)
    m_name = models.CharField(blank=True, max_length=32)
    email = models.EmailField(null=True, blank=True)

    def __str__(self):
        return f"{self.l_name}, {self.email}"
    