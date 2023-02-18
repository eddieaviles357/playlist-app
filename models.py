"""Models for Playlist app."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Playlist(db.Model):
    """Playlist."""
    __tablename__ = 'playlists'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30), nullable=False)
    description = db.Column(db.String(50), nullable=False)

    user_songs = db.relationship('Song', secondary='playlists_songs', backref='playlists')

    def __repr__(self):
        return f'Playlist( id={self.id}, name={self.name}, description={self.description} )'



class Song(db.Model):
    """Song."""
    __tablename__ = 'songs'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(30), nullable=False)
    artist = db.Column(db.String(30), nullable=False)

    user_playlists = db.relationship('Playlist', secondary='playlists_songs', backref='songs')

    def __repr__(self):
        return f"Song( id={self.id}, title={self.title}, artist={self.artist} )"
    


class PlaylistSong(db.Model):
    """Mapping of a playlist to a song."""
    __tablename__ = 'playlists_songs'
    playlist_id = db.Column(db.ForeignKey('playlists.id'), primary_key=True)
    
    song_id = db.Column(db.ForeignKey('songs.id'), primary_key=True)



def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)