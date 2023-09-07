import peewee as orm
import os
from dotenv import load_dotenv
import pandas as pd

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

    @classmethod
    def get_as_dicts(cls):
        return (
            cls.select(
                Station,
                StationName.name,
                StationLocation.latitude,
                StationLocation.longitude,
                StationLocation.altitude,
            )
            .join(
                StationName,
                on=(
                    (StationName.station_id == Station.id)
                    & StationName.to_date.is_null()
                ),
            )
            .join(
                StationLocation,
                on=(
                    (StationLocation.station_id == Station.id)
                    & StationLocation.to_date.is_null()
                ),
            )
            .dicts()
        )


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

    @classmethod
    def get_timeseries_by_station_name(
        cls, station_name, start_date=None, end_date=None, as_dataframe=True
    ):
        if not end_date:
            end_date = pd.Timestamp.now().date()
        if not start_date:
            start_date = end_date - pd.Timedelta(days=365)

        join_predicates = (Wind10Minutes.station == StationLocation.station) & (
            (
                (StationLocation.from_date <= Wind10Minutes.timestamp)
                & (Wind10Minutes.timestamp <= StationLocation.to_date)
            )
            | (
                (StationLocation.to_date is None)
                & (StationLocation.from_date <= Wind10Minutes.timestamp)
            )
        )

        query = (
            cls.select(
                Wind10Minutes.timestamp,
                StationLocation.latitude,
                StationLocation.longitude,
                Wind10Minutes.avg_speed,
                Wind10Minutes.avg_direction,
            )
            .join(StationLocation, on=join_predicates)
            .join(StationName, on=(Wind10Minutes.station == StationName.station))
            .where(
                (StationName.name == station_name)
                & (start_date <= Wind10Minutes.timestamp)
                & (Wind10Minutes.timestamp <= end_date)
            )
            .order_by(Wind10Minutes.timestamp)
            .dicts()
        )

        if as_dataframe:
            return pd.DataFrame(list(query))
        else:
            return list(query)


def model_init():
    tables = [Station, StationName, StationLocation, Wind10Minutes]
    db.drop_tables(tables)
    db.create_tables(tables)
