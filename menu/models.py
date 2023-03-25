from django.db import models


class Menu(models.Model):
    name = models.CharField(max_length=300)

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    title = models.CharField(max_length=300)
    url_is_named = models.BooleanField(default=False)
    url = models.CharField(max_length=300)
    order = models.IntegerField()
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
