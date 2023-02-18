"""Forms for playlist app."""

from wtforms import SelectField, StringField
from wtforms.validators import InputRequired, Length
from flask_wtf import FlaskForm


class PlaylistForm(FlaskForm):
    """Form for adding playlists."""
    name = StringField('name', validators=[InputRequired(message='Please name your playlist'), Length(max=30)])
    description = StringField('description', validators=[InputRequired(message='Please enter a description'), Length(max=50)])

class SongForm(FlaskForm):
    """Form for adding songs."""

    # Add the necessary code to use this form


# DO NOT MODIFY THIS FORM - EVERYTHING YOU NEED IS HERE
class NewSongForPlaylistForm(FlaskForm):
    """Form for adding a song to playlist."""

    song = SelectField('Song To Add', coerce=int)
