import sqlite3


class Datastore:
    def __init__(self):
        self.connection = sqlite3.connect('downloaded_videos.db')
        self.c = self.connection.cursor()
        self.c.execute("""CREATE TABLE IF NOT EXISTS videos (
                    title  text,
                    id text,
                    channel text,
                    thumbnailurl text
                    )""")

    def commit(self):
        self.connection.commit()

    def close(self):
        self.connection.commit()
        self.connection.close()

    def insert_video(self, title, id, channel, thumbnailurl):
        self.c.execute("INSERT INTO videos(title,id,channel,thumbnailurl) VALUES (?, ?, ?, ?)",
                       (title, id, channel, thumbnailurl))
        self.commit()
