from django.db import models

# Create your models here.


class Category(models.Model):
    slug = models.CharField(default = '', max_length = 300)
    name = models.CharField(default = '', max_length = 300)
    imgsrc = models.ImageField(upload_to="static/images/products", default = None, blank = True )

    def __str__(self):
        return self.slug + self.name
        
class Destination(models.Model):
    name = models.CharField(default = '', max_length = 300)
    category = models.ForeignKey(Category,
    on_delete=models.CASCADE)
    def __str__(self):
        return self.name

        
class Product(models.Model):
    # attributes = models.ManyToManyField(Attributeitem)
    # attributes = models.ManyToManyField(Attribute)
    category = models.ForeignKey(Category,
    on_delete=models.CASCADE, default = None,)
    destination = models.ManyToManyField(Destination)
    
    name = models.CharField(default = '', max_length = 300)
    price = models.IntegerField(default = 0)
    sale_price = models.IntegerField(default = 0)
    description = models.CharField(default = '', max_length = 2000)
    # imgsrc = models.ImageField(upload_to='static/images', blank = True, null = True)
    imgsrc = models.ImageField(upload_to="static/images/products", default = None, blank = True, null = True)
    def __str__(self):
        return self.category.slug + self.name 
    def discount_perc(self):
        return int((self.sale_price / self.price) * 100)
    def discount_val(self):
        return int(self.price - self.sale_price)
    def has_sale(self):
        if self.sale_price > 0:
            return True
        else:
            return False


class Attribute(models.Model):
    name = models.CharField(default = '', max_length = 300) 
    category = models.ForeignKey(Category,
    on_delete=models.CASCADE, default = None,)
    # product = models.ForeignKey(Product,
    #     on_delete=models.CASCADE, default = None,
    # )
    product = models.ManyToManyField(Product)
    def __str__(self):
        return self.name 

class Attributeitem(models.Model):
    name = models.CharField(default = '', max_length = 300)
    attr = models.ForeignKey(
        Attribute, on_delete=models.CASCADE,
    )
    product = models.ManyToManyField(Product)
    def __str__(self):
        return self.name 
    
def deleteall():
    pr = Product.objects.all()
    dest = Destination.objects.all()
    ct = Category.objects.all()
    atr = Attribute.objects.all()

    atr.delete()
    attritem = Attributeitem.objects.all()
    attritem.delete()

    ct.delete()
    dest.delete()
    pr.delete()

    print('all is deleted')