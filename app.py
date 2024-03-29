# flask --debug run
from flask import Flask, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, Playlist, Song, PlaylistSong
from forms import NewSongForPlaylistForm, SongForm, PlaylistForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///playlist_app'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
# db.create_all()

app.config['SECRET_KEY'] = "I'LL NEVER TELL!!"

# Having the Debug Toolbar show redirects explicitly is often useful;
# however, if you want to turn it off, you can uncomment this line:
#
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)


@app.route("/")
def root():
    """Homepage: redirect to /playlists."""

    return redirect("/playlists")


# ##############################################################################
# # Playlist routes


@app.route("/playlists")
def show_all_playlists():
    """Return a list of playlists."""

    play_lists = Playlist.query.all()
    return render_template("playlists.html", playlists=play_lists)


@app.route("/playlists/<int:playlist_id>")
def show_playlist(playlist_id):
    """Show detail on specific playlist."""
    play_list = Playlist.query.get_or_404(playlist_id)
    return render_template('playlist.html', playlist=play_list)


@app.route("/playlists/add", methods=["GET", "POST"])
def add_playlist():
    """Handle add-playlist form """
    form = PlaylistForm()
    if form.validate_on_submit():
        db.session.add(Playlist(name=form.data['name'], description=form.data['description']))
        db.session.commit()
        return redirect('/playlists')
    return render_template('new_playlist.html', form=form)


# ##############################################################################
# # Song routes


@app.route("/songs")
def show_all_songs():
    """Show list of songs."""

    songs = Song.query.all()
    return render_template("songs.html", songs=songs)


@app.route("/songs/<int:song_id>")
def show_song(song_id):
    """return a specific song"""
    song = Song.query.get_or_404(song_id)
    return render_template('song.html', song=song)


@app.route("/songs/add", methods=["GET", "POST"])
def add_song():
    """Handle add-song form  """
    form = SongForm()
    if form.validate_on_submit():
        db.session.add(Song(title=form.data['title'], artist=form.data['artist']))
        db.session.commit()
        return redirect('/songs')
    return render_template('new_song.html', form=form)


@app.route("/playlists/<int:playlist_id>/add-song", methods=["GET", "POST"])
def add_song_to_playlist(playlist_id):
    """Add a playlist and redirect to list."""

    playlist = Playlist.query.get_or_404(playlist_id)
    form = NewSongForPlaylistForm()

    # Restrict form to songs not already on this playlist
    curr_on_playlist = [s.id for s in playlist.songs]
    # dynamically add form choices
    form.song.choices = [(int(song.id), song.title ) for song in db.session.query(Song.id, Song.title).filter(Song.id.notin_(curr_on_playlist)).all()]
    if form.validate_on_submit():
        # add song to playlist
        db.session.add(PlaylistSong(playlist_id=playlist.id,song_id=form.data['song']))
        db.session.commit()
        return redirect(f"/playlists/{playlist_id}")
    return render_template("add_song_to_playlist.html",
                             playlist=playlist,
                             form=form)
