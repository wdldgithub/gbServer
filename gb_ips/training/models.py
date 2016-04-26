from django.db import models

# Create your models here.
class TrainingRawData(models.Model):
    ssid = models.CharField(max_length = 30)
    bssid = models.CharField(max_length = 30)
    rssi = models.CharField(max_length = 10)
    device_id = models.CharField(max_length = 30)
    market_id = models.CharField(max_length = 10)
    floor_id = models.CharField(max_length = 10)
    x = models.CharField(max_length = 30)
    y = models.CharField(max_length = 30)
    createtime = models.DateTimeField(auto_now = True)

    class Meta:
        db_table = 'training_raw_data'

    def __unicode__(self):
        return '%s %s %s' % (self.device_id, self.bssid, self.rssi)

    @classmethod
    def create(cls, **kwargs):
        obj = None
        is_create = False

        try:
            obj = cls()
            for k,v in kwargs.iteritems():
                setattr(obj, k, v)
            is_create = True
        except Exception as e:
            print e
            pass

        return (is_create, obj)

    @classmethod
    def load_all(cls, floor_id):
        objs = cls.objects.filter(floor_id=floor_id).values()

        return objs

