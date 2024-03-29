from django.db import models


class Provider(models.Model):
    name = models.CharField(max_length=15)

    def __str__(self):
        return self.name


class Nominal(models.Model):
    provider = models.ForeignKey(
        Provider,
        related_name='nominals',
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=15)
    cost = models.FloatField()
    price = models.FloatField()

    def provider_name(self):
        return self.provider.name

    def __str__(self):
        return '%s %s / cost:%d / price:%d' % (
            self.provider,
            self.name,
            self.cost,
            self.price,
        )


class Transaction(models.Model):
    number = models.CharField(max_length=15, default='000')
    nominal = models.ForeignKey(
        Nominal,
        on_delete=models.CASCADE
    )
    cost = models.FloatField(blank=True)
    price = models.FloatField(blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.cost = self.nominal.cost
        self.price = self.nominal.price
        super(Transaction, self).save(*args, **kwargs)

    def __str__(self):
        return '%s / %s' % (self.number, self.nominal)
