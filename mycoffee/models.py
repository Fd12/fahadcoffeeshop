from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal
from django.db.models.signals import pre_save, post_save, post_delete


class Bean(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=5, decimal_places=3)

    def __str__(self):
        return self.name


class Roast(models.Model):
    name = models.CharField(max_length=150)
    price = models.DecimalField(max_digits=5, decimal_places=3)

    def __str__(self):
        return self.name


class Syrup(models.Model):
    name = models.CharField(max_length=150)
    price = models.DecimalField(max_digits=5, decimal_places=3)

    def __str__(self):
        return self.name

class Powder(models.Model):
    name = models.CharField(max_length=150)
    price = models.DecimalField(max_digits=5, decimal_places=3)

class Coffee (models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    name = models.CharField(max_length=100)
    espresso_shots = models.PositiveIntegerField(default=1)
    bean = models.ForeignKey(Bean, on_delete=models.PROTECT)
    roast = models.ForeignKey(Roast, on_delete=models.PROTECT)
    syrups = models.ManyToManyField(Syrup, blank=True)
    powders = models.ManyToManyField(Powder, blank=True)
    water = models.FloatField()
    steamedmilk = models.BooleanField(default=False)
    foam = models.FloatField()
    extra_instructions = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=3, null = True)
        
    def __str__(self):
        return self.name


class CartItem(models.Model):
    cart = models.ForeignKey("Cart" ,on_delete=models.PROTECT)
    item = models.ForeignKey(Coffee, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    line_item_total = models.DecimalField(decimal_places = 3, max_digits = 20)
    def __str__(self):
        return self.item.title

def cart_item_pre_save_receiver(sender, instance, *args, **kwargs):
    qty = instance.quantity
    if qty>=1:
        price = instance.item.price
        line_item_total = Decimal(qty)*Decimal(price)
        instance.line_item_total = line_item_total

pre_save.connect(cart_item_pre_save_receiver, sender=CartItem)

def cart_item_post_save_receiver(sender, instance, *args, **kwargs):
    instance.cart.update_subtotal()

post_save.connect(cart_item_post_save_receiver, sender=CartItem)
post_delete.connect(cart_item_post_save_receiver, sender=CartItem)


class Cart(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.PROTECT)
    items = models.ManyToManyField(Coffee, through=CartItem)
    subtotal = models.DecimalField(decimal_places = 3, max_digits = 50, default=2.000)
    delivery_total = models.DecimalField(decimal_places = 3, max_digits = 50, default=2.000)
    total = models.DecimalField(decimal_places = 3, max_digits = 50, default=2.000)

    def __str__(self):
        return str(self.id)



    def update_subtotal(self):
        subtotal = 0
        items = self.cartitem_set.all()
        for item in items:
            subtotal += items.line_items_total
        self.subtotal = "%.3f"%subtotal
        self.save()




def do_delivery_and_total(sender, instance, *args, **kwargs):
    subtotal = Decimal(instance.subtotal)
    delivery_total = Decimal(2.000)
    total = subtotal + delivery_total
    instance.delivery_total = "%.3f"%delivery_total
    instance.total = "%.3f"%total

pre_save.connect(do_delivery_and_total, sender=Cart)

