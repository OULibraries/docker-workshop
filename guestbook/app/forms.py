from wtforms import Form, StringField, validators, SubmitField
from wtforms.validators import DataRequired

class GuestbookForm(Form):
    """Guestbook Signing Form"""

    # Name Form Field
    name = StringField('Name', [
        validators.DataRequired(message=("Enter your name."))
    ])

    # Submit Form Field.
    submit = SubmitField("Sign the Guestbook")