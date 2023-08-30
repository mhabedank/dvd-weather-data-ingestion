import peewee as orm
import os
from dotenv import load_dotenv
from datetime import date

load_dotenv("../.env", override=True)

DB_USER = os.getenv("AWS_RDS_USER")
DB_PASSWORD = os.getenv("AWS_RDS_PASSWORD")
DB_HOST = os.getenv("AWS_RDS_HOST")
DB_NAME = os.getenv("AWS_RDS_DB")

db = orm.PostgresqlDatabase(DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)


class Station(orm.Model):
    id = orm.AutoField()

    class Meta:
        table_name = "station"
        database = db


class StationName(orm.Model):
    id = orm.AutoField()
    station = orm.ForeignKeyField(Station, backref="names")
    name = orm.CharField()
    from_date = orm.DateField()
    to_date = orm.DateField(null=True)

    class Meta:
        table_name = "station_name"
        database = db


class StationLocation(orm.Model):
    id = orm.AutoField()
    station = orm.ForeignKeyField(Station, backref="locations")
    latitude = orm.FloatField()
    longitude = orm.FloatField()
    altitude = orm.FloatField()
    from_date = orm.DateField()
    to_date = orm.DateField(null=True)

    class Meta:
        table_name = "station_location"
        database = db

    # TODO: Berlin Brandenburg Query.
    # TODO: Business Rule Check (From To Date)
    # TODO: check for consistency with great expectations


class Wind10Minutes(orm.Model):
    QUALITY_CHOICE = [
        (1, "Formal test only"),
        (2, "Tested according to individual criteria"),
        (3, "Automatic check and correction"),
    ]

    id = orm.AutoField()
    station = orm.ForeignKeyField(Station, backref="wind_10_minutes")
    timestamp = orm.DateTimeField()
    quality = orm.IntegerField(choices=QUALITY_CHOICE)
    avg_speed = orm.FloatField()
    avg_direction = orm.IntegerField()

    class Meta:
        table_name = "wind_10_minutes"
        database = db


def model_init():
    tables = [Station, StationName, StationLocation, Wind10Minutes]
    db.drop_tables(tables)
    db.create_tables(tables)
