import peewee

proxy = peewee.Proxy()


class myModel(peewee.Model):
    class Meta:
        database = proxy


class VarModel(myModel):
    id = peewee.AutoField()
    sig_name = peewee.CharField(max_length=128, index=True, help_text='变量名')
    type = peewee.CharField(max_length=255, help_text='I/O Type')
    cabinets = peewee.CharField(max_length=255, help_text='机柜号')
    channel = peewee.CharField(max_length=255, help_text='通道号')
    carID = peewee.IntegerField(null=True, help_text='cardID')
    size = peewee.IntegerField(null=True, help_text='size')
    PlaceNumber = peewee.IntegerField(null=True, help_text='位号')
    minValue = peewee.IntegerField(null=True, help_text='最小值')
    maxValue = peewee.IntegerField(null=True, help_text='最大值')


def init_database(database: peewee.Database):
    proxy.initialize(database)
    database.create_tables([VarModel], safe=True)
