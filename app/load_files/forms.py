from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import SubmitField


class UploadForm(FlaskForm):

    upload = FileField('Seleccionar archivo', validators=[FileRequired(),
                                                          FileAllowed(['txt', 'TXT', 'csv', 'CSV', 'xlsx', 'XLSX',
                                                                       'xls', 'XLS'], 'Sólo archivos de texto')])
    submit = SubmitField('Cargar')
