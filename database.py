from peewee import (CharField, ForeignKeyField, Model, PrimaryKeyField,
                    SqliteDatabase, TextField)

from config import DATABASE_NAME

db = SqliteDatabase(DATABASE_NAME)


class Song(Model):
    id = PrimaryKeyField(unique=True)
    author = CharField()
    title = CharField()

    class Meta:
        database = db
        db_table = 'songs'


class Order(Model):
    id = PrimaryKeyField(unique=True)
    song_id = ForeignKeyField(Song)
    congratulation = TextField()

    class Meta:
        database = db
        db_table = 'orders'

    @staticmethod
    def make_order(title, congratulation):
        Order.insert(title=title, congratulation=congratulation).execute()


db.create_tables([Song, Order])
