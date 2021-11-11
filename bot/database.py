import re

from config import DATABASE_NAME
from peewee import (CharField, ForeignKeyField, Model, PrimaryKeyField,
                    SqliteDatabase, TextField)

db = SqliteDatabase(DATABASE_NAME)


class Song(Model):
    id = PrimaryKeyField(unique=True)
    author = CharField()
    title = CharField()

    class Meta:
        database = db
        db_table = 'songs'

    @staticmethod
    def load_tracklist_from_file(filename: str):
        """Load new tracklist from file to DB.

        :param filename: tracklist filename
        """
        sep, tracklist = ' - ', []
        with open(filename, encoding='utf-8-sig') as f:
            for line in f:
                line = re.sub(r'\d+\. ', '', line)
                author_song = line.rstrip().split(sep=sep)
                # read pair "author - song title"
                tracklist.append(tuple(author_song))
        Song.truncate_table()
        Song.insert_many(
            tracklist, fields=[Song.author, Song.title]).execute()

    @staticmethod
    def show_tracklist() -> str:
        """Return tracklist as string from DB."""
        tracklist = ''
        for song in Song.select():
            tracklist = f"{tracklist}\n{song.id}. {song.author} - {song.title}"
        return tracklist


class Order(Model):
    id = PrimaryKeyField(unique=True)
    song_id = ForeignKeyField(Song)
    congratulation = TextField()

    class Meta:
        database = db
        db_table = 'orders'

    @staticmethod
    def make_order(song_id, congratulation):
        Order.insert(song_id=song_id, congratulation=congratulation).execute()


db.create_tables([Song, Order])
