from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=30)
    price = models.FloatField()

    def stock(self):
        queryset = Purchase.objects.filter(item=self)
        return sum(p.qty - p.sold() for p in queryset if not p.stock_out())

    def __str__(self):
        return self.name


class Purchase(models.Model):
    item = models.ForeignKey(
        Item,
        related_name='purchases',
        on_delete=models.CASCADE
    )
    cost = models.FloatField()
    qty = models.IntegerField()
    date = models.DateField(auto_now_add=True)

    def sold(self):
        sales = Sale.objects.filter(purchase__id=self.id)
        return sum(sale.qty for sale in sales)

    def stock_out(self):
        return self.sold() >= self.qty

    def __str__(self):
        return '%s: %s' % (
            self.date.strftime('%d-%m-%Y'),
            self.item
        )


class Sale(models.Model):
    purchase = models.ForeignKey(
        Purchase,
        related_name='sales',
        on_delete=models.CASCADE
    )
    price = models.FloatField()
    qty = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s: %s, purchase_id:%d, price:%d, qty:%d' % (
            self.date.strftime('%Y-%m-%d %H:%M'),
            self.purchase.item,
            self.purchase.id,
            self.price, self.qty
        )
