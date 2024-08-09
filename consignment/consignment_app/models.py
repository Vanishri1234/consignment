from django.db import models
from django.contrib.auth.models import AbstractBaseUser

# Create your models here.

class Login(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    utype = models.CharField(max_length=50)

class AddTrack(models.Model):
    track_id = models.CharField(max_length=50, null=True)
    date = models.CharField(max_length=30, null=True)
    description = models.CharField(max_length=30, null=True)
    payment = models.CharField(max_length=100, default='Not Paid')  # or whatever field type you're using


class AddConsignment(models.Model):
    track_id = models.CharField(max_length=50, null=True)
    sender_name = models.CharField(max_length=50, null=True)
    sender_mobile = models.CharField(max_length=50, null=True)
    sender_email = models.CharField(max_length=50, null=True)
    sender_address = models.CharField(max_length=50, null=True)
    sender_company=models.CharField(max_length=50,null=True)
    sender_GST=models.CharField(max_length=50,null=True)
    receiver_name = models.CharField(max_length=50, null=True)
    receiver_mobile = models.CharField(max_length=50, null=True)
    receiver_email = models.CharField(max_length=50, null=True)
    receiver_address = models.CharField(max_length=50, null=True)
    receiver_company = models.CharField(max_length=50, null=True)
    total_cost = models.IntegerField(max_length=50, null=True)
    date = models.CharField(max_length=30, null=True)
    pay_status = models.CharField(max_length=30, null=True)
    route_from = models.CharField(max_length=30, null=True)
    route_to = models.CharField(max_length=30, null=True)
    desc_product = models.CharField(max_length=150,null=True)
    pieces = models.CharField(max_length=50,null=True)
    dimension = models.CharField(max_length=50,null=True)
    packing = models.CharField(max_length=50,null=True)
    actual_weight = models.CharField(max_length=50,null=True)
    prod_gst = models.CharField(max_length=50,null=True)
    prod_invoice = models.CharField(max_length=50,null=True)
    prod_price = models.CharField(max_length=50,null=True)
    qty = models.IntegerField(max_length=30, null=True)
    weight = models.IntegerField(max_length=30, null=True)
    gst=models.IntegerField(max_length=50,null=True)
    cgst=models.CharField(max_length=50,null=True)
    sgst=models.CharField(max_length=50,null=True)
    freight = models.IntegerField(max_length=30, null=True)
    hamali = models.IntegerField(max_length=30, null=True)
    door_charge = models.IntegerField(max_length=30, null=True)
    st_charge = models.IntegerField(max_length=30, null=True)
    Consignment_id=models.IntegerField(max_length=50,null=True)


    def __str__(self):
        return self.track_id


class FeedBack(models.Model):
    username=models.CharField(max_length=50,null=True)
    feedback=models.CharField(max_length=200,null=True)
    def __str__(self):
        return self.username

