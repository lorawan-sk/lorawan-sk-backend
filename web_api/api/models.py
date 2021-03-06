import random
import string
import uuid

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

def generate_api_key():
    api_key = ''.join(random.SystemRandom().choice(string.ascii_lowercase + string.digits) for _ in range(32))
    return str(api_key)

def generate_mqtt_password(length = 16):
    api_key = ''.join(random.SystemRandom().choice(string.ascii_lowercase + string.digits) for _ in range(length))
    return str(api_key)

def generate_gw_serial():
    serial = ''.join("{:02x}".format(ord(c)) for c in ''.join(random.SystemRandom().choice(string.ascii_lowercase + string.digits) for _ in range(8)))
    return str(serial)

class Gateway(models.Model):
    def __unicode__(self):
         return str(self.mac) + "-" + str(self.serial)
    description = models.TextField(null=True, blank=True)
    owner = models.ForeignKey(User)
    location = models.CharField(max_length=512, default="", blank=True)
    gps_lon = models.FloatField(default=0.0, blank=True)
    gps_lat = models.FloatField(default=0.0, blank=True)
    serial = models.CharField(max_length=16, default=generate_gw_serial, blank=True)
    mqtt_password = models.CharField(max_length=16, default=generate_mqtt_password, blank=True, null=True)
    mac = models.CharField(max_length=64, null=False, blank=False, unique=True)
    lorawan_band = models.IntegerField(choices=((0, 'EU863-870'), (1, 'US902-928'), (2, 'CN779-787'), (3, 'EU433')), null=True, blank=True)
    last_seen = models.DateTimeField(null=True, blank=True)
    last_seen_ip = models.CharField(max_length=200, blank=True, null=True)

class Key(models.Model):
    def __unicode__(self):
         return str(self.numeric) + " ~ " + self.key + " ~ " + self.unit
    numeric = models.IntegerField(primary_key=True)
    key = models.CharField(max_length=256, default="?")
    unit = models.CharField(max_length=256, default="?")

class NodeType(models.Model):
    def __unicode__(self):
         return self.name
    name = models.CharField(max_length=128, default="")
    keys = models.ManyToManyField(Key)

class LoRaWANApplication(models.Model):
    def __unicode__(self):
         return self.name + " (" + self.AppEUI + ")"
    name = models.CharField(max_length=128)
    AppEUI = models.CharField(max_length=128, null=False, blank=False)
    AppKey   = models.CharField(max_length=128, null=False, blank=False)
    api_key = models.UUIDField(default=uuid.uuid4, unique=True) 

class Node(models.Model):
    def __unicode__(self):
         return str(self.node_id) + "-" + str(self.api_key)
    id = models.AutoField(primary_key = True)
    node_id = models.CharField(max_length=255, null=True, unique=True)
    api_key = models.CharField(max_length=20, null=False, blank=False, unique=True, default=generate_api_key)
    name = models.CharField(max_length=128, null=False, blank=False)
    location = models.CharField(max_length=512, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    owner = models.ForeignKey(User, related_name='+')
    users = models.ManyToManyField(User, blank=True)
    nodetype = models.ForeignKey(NodeType, null=False, blank=False)
    gps_lon = models.FloatField(default=0.0)
    gps_lat = models.FloatField(default=0.0)
    last_rawpoint = models.DateTimeField(null=True, blank=True)
    lorawan_application = models.ForeignKey(LoRaWANApplication, null=True, blank=True)

class ABP(models.Model):
    def __unicode__(self):
         return self.DevAddr
    node = models.ForeignKey(Node)
    DevAddr = models.CharField(max_length=8, null=True, blank=True)
    NwkSKey = models.CharField(max_length=32, null=True, blank=True)
    AppSKey = models.CharField(max_length=32, null=True, blank=True)

class Rawpoint(models.Model):
    def __unicode__(self):
         return str(self.id)
    id = models.IntegerField(primary_key = True)
    payload = models.CharField(max_length=128)
    gateway_serial = models.CharField(max_length=128, null=True)
    gw = models.ForeignKey(Gateway, db_column = 'gw_serial', null=True, blank=True)
    rssi = models.IntegerField(null=True, blank=True)
    snr = models.IntegerField(null=True, blank=True)
    timestamp = models.DateTimeField(db_column = 'gw_timestamp')
    node = models.ForeignKey(Node)
    state = models.IntegerField(choices=((0, 'new'), (1, 'processed'), (2, 'failed to process')), default=0)
    seq_number = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = 'raw_data'

class LoRaWANRawPoint(models.Model):
    def __unicode__(self):
         return str(self.id)
    chan = models.IntegerField(null=True, blank=True)
    codr = models.CharField(max_length=16, null=True, blank=True)
    data = models.CharField(max_length=1024, null=True, blank=True)
    datr = models.CharField(max_length=16, null=True, blank=True)
    freq = models.FloatField(null=True, blank=True)
    lsnr = models.FloatField(null=True, blank=True)
    rssi = models.IntegerField(null=True, blank=True)
    time = models.DateTimeField(null=True, blank=True)
    tmst = models.IntegerField(null=True, blank=True)
    DevAddr = models.CharField(max_length=32, null=True, blank=True)
    FCtrl   = models.CharField(max_length=10, null=True, blank=True)
    FCnt    = models.IntegerField(null=True, blank=True)
    FOpts   = models.CharField(max_length=40, null=True, blank=True)
    MType = models.IntegerField(null=True, blank=True)
    FPort = models.IntegerField(null=True, blank=True)
    FRMPayload = models.CharField(max_length=1024, null=True, blank=True)
    PHYPayload = models.CharField(max_length=1024, null=True, blank=True)
    MIC = models.CharField(max_length=16, null=True, blank=True)
    gateway_serial = models.CharField(max_length=128, null=True, blank=True)
    gw   = models.ForeignKey(Gateway, null=True, blank=True)
    node = models.ForeignKey(Node, null=True, blank=True)

class Point(models.Model):
    def __unicode__(self):
         return str(self.id)
    id = models.IntegerField(primary_key = True)
    key = models.ForeignKey(Key, db_column = '_key', db_constraint=False, null=False, blank=False)
    node = models.ForeignKey(Node, db_column = 'serial', db_constraint=False, null=True, blank=True)
    value = models.FloatField()
    rssi = models.FloatField(null=True, blank=True)
    snr = models.FloatField(null=True, blank=True)
    timestamp = models.DateTimeField(null=True, blank=True)
    gw = models.ForeignKey(Gateway, db_constraint=False, null=True, blank=True)
    rawpoint = models.ForeignKey(Rawpoint, db_constraint=False, null=True, blank=True)
    raw_packet = models.CharField(max_length=256, null=True, blank=True)
    class Meta:
        db_table = 'parsed_data'
        unique_together = (("key", "node", "timestamp", "gw"))

class Profile(models.Model):
    def __unicode__(self):
        return str(self.user_api_key)
    phone_regex = RegexValidator(regex=r'^\+\d{8,15}$', message="Phone number must be entered in the format: '+12345678'. With 8 to 15 digits.")
    phone_number = models.CharField(max_length=16, validators=[phone_regex], null=True, blank=True)
    user = models.OneToOneField(User) 
    user_api_key = models.CharField(
        max_length=256,
        null=False,
        blank=False,
        default = generate_api_key,
    )
