from datetime import datetime

import pandas as pd
from flask import request, Blueprint, url_for, redirect

from Helpers.middleware import protected_route
from Q2.Trolley.model import TrolleyModel

upload_routes = Blueprint('csvUpload', __name__)


@upload_routes.route('/uploadCsv', methods=['POST'])
@protected_route()
def upload_csv():
    print("i am inside upload csv")
    print(request.files)
    df = pd.read_csv(request.files['file'])
    records = []
    print("reading pandas")
    for row in df.iterrows():
        records.append(TrolleyModel(
            trolley_id=row[1][0],
            recorded_date_time=datetime.strptime(row[1][1], '%Y-%m-%dT%H:%M'),
            temperature=int(row[1][2])
        ))

    TrolleyModel.objects.insert(records)
    return redirect(url_for('trolley.upload'))
