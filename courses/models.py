from django.db import models


class Course(models.Model):
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Step(models.Model):

    title = models.CharField(max_length=200)
    description = models.TextField()
    content = models.TextField(blank=True, default='')
    order = models.IntegerField(default=0)
    course = models.ForeignKey(Course, on_delete='models.CASCADE')

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title
