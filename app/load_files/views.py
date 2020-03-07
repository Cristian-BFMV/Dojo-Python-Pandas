from datetime import datetime, timedelta

from flask import redirect, url_for, flash, request, render_template, make_response
from werkzeug.datastructures import CombinedMultiDict

from app import global_data
from . import load_files
from .forms import UploadForm
from . import utils as load_files_utils


@load_files.route('/load_account_files', methods=['GET', 'POST'])
def load_account_files():
    accounts_data_load_form = UploadForm(CombinedMultiDict((request.files, request.form)))

    if request.method == 'POST':
        event_metadata = {}
        if accounts_data_load_form.validate_on_submit():
            upload_type = request.form.get('upload_type')
            f = accounts_data_load_form.upload.data

            balances_df = load_files_utils.process_balances_file(f, upload_type)

            global_data.load_accounts_data('accounting', balances_df)
            return redirect(url_for('dashboard.homepage'))

        else:
            result_message = "El archivo no es válido. Debe ser un archivo de texto separado por algún caracter " \
                             "o un archivo de Excel"
            flash(result_message)

        event_metadata['result_message'] = result_message

    show_loading = False
    current_date = datetime.now()
    current_date = current_date.replace(hour=0, minute=0, second=0, microsecond=0)
    current_date = current_date - timedelta(days=1)
    return render_template('load_files/load_account_files.html',
                           title="Dojo Python Panda",
                           active_page='daily_load',
                           daily_load_form=accounts_data_load_form,
                           show_loading=show_loading,
                           current_date=datetime.strftime(current_date, '%d/%m/%Y'))


