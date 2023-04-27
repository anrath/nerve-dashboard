from wtforms import Form, StringField, SubmitField
from wtforms.validators import DataRequired

class SearchForm(Form):
  search = StringField('Enter a Mac Address to search up its details', [DataRequired()])
  submit = SubmitField('Search',
                       render_kw={'class': 'btn btn-success btn-block'})