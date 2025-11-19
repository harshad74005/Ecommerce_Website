from django.db import models
from .customer import Customer

# These are the choices for your order status
STATUS_CHOICE = (
    ('Accepted', 'Accepted'),
    ('Packed', 'Packed'),
    ('On The Way', 'On The Way'),
    ('Deliverd', 'Deliverd'),
    ('Cancel', 'Cancel'),
    ('Pending', 'Pending'),  # Added Pending to your choices
)


class OrderDetail(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=100)
    qty = models.IntegerField(default=1)
    price = models.IntegerField()
    image = models.ImageField(upload_to='orders/')

    #
    # FIX: Using your STATUS_CHOICE variable here
    #
    # status = models.CharField(max_length=50, choices=STATUS_CHOICE, default='Confirmed')

    # Corrected (Use a value from STATUS_CHOICE)
    status = models.CharField(max_length=50, choices=STATUS_CHOICE, default='Pending')
    ordered_date = models.DateTimeField(auto_now_add=True)
    address = models.CharField(max_length=255, default='')
    phone = models.CharField(max_length=15, default='')