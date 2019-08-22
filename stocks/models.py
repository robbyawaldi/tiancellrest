import uuid
from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=25)
    price = models.FloatField()

    def purchases(self):
        queryset = Purchase.objects.filter(item=self)
        purchases = [p for p in queryset if not p.stock_out()]
        return purchases

    def stock(self):
        return sum(p.qty - p.sold() for p in self.purchases())

    def currentpurchase(self):
        return self.purchases()[0].id if self.stock() else None

    def __str__(self):
        return '%s / price:%d / stock:%d' % (self.name, self.price, self.stock())

    class Meta:
        ordering = ['name']


class Purchase(models.Model):
    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE
    )
    cost = models.FloatField()
    qty = models.IntegerField()
    date = models.DateField(auto_now_add=True)

    def item_name(self):
        return self.item.name

    def sold(self):
        sales = Sale.objects.filter(purchase=self)
        return sum(sale.qty for sale in sales)

    def remaining(self):
        return self.qty - self.sold()

    def stock_out(self):
        return self.sold() >= self.qty

    def __str__(self):
        return '%s / %s / cost:%d / qty:%d' % (
            self.date.strftime('%d-%m-%Y'),
            self.item.name,
            self.cost,
            self.qty,
        )


class Sale(models.Model):
    purchase = models.ForeignKey(
        Purchase,
        on_delete=models.CASCADE
    )
    price = models.FloatField()
    qty = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

    def cost(self):
        return self.purchase.cost

    def gross_profit(self):
        return self.price * self.qty

    def net_profit(self):
        return self.gross_profit() - (self.cost() * self.qty)

    def __str__(self):
        return '%s / %s / price:%d / qty:%d' % (
            self.date.strftime('%Y-%m-%d %H:%M'),
            self.purchase.item.name,
            self.price,
            self.qty
        )
