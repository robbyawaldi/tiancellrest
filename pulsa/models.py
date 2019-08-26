from django.db import models


class Provider(models.Model):
    name = models.CharField(max_length=15)

    def __str__(self):
        return self.name


class Nominal(models.Model):
    provider = models.ForeignKey(
        Provider,
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=15)
    cost = models.FloatField()
    price = models.FloatField()

    def __str__(self):
        return '%s %s / cost:%d / price:%d' % (
            self.provider,
            self.name,
            self.cost,
            self.price,
        )


class Transaction(models.Model):
    nominal = models.ForeignKey(
        Nominal,
        on_delete=models.CASCADE
    )
    cost = models.FloatField()
    price = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s / %s %s / cost:%d / price:%d' % (
            self.date.strftime('%d-%m-%Y %H:%M'),
            self.nominal.provider,
            self.nominal.name,
            self.cost,
            self.price,
        )
