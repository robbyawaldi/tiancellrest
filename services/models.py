from django.db import models


class Service(models.Model):
    brand = models.CharField(max_length=10)
    type = models.CharField(max_length=10)
    desc = models.TextField()
    cost = models.FloatField()
    price = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s / %s %s / cost:%s / price:%s' % (
            self.date.strftime('%Y-%m-%d %H:%M'),
            self.brand,
            self.type,
            self.cost,
            self.price,
        )
