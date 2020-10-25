import json
from datetime import datetime

import pandas as pd
from flask import Blueprint, render_template, request, redirect, url_for, jsonify

from F_MVC.Trolly.model import TrolleyModel
from F_MVC.Trolly.service import get_all_trolleys, get_single_day_graphs_layout
from Helpers.middleware import protected_route

trolley_routes = Blueprint("trolley", __name__)


@trolley_routes.route('/upload')
@protected_route()
def upload():
    all_trolleys = get_all_trolleys()
    return render_template("Upload.html", all_trolleys=all_trolleys)


@trolley_routes.route('/uploadCsv', methods=['POST'])
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


@trolley_routes.route('/singleRecordTrolley', methods=['POST'])
@protected_route()
def single_record_trolley():
    date_time = "{} {}".format(request.form['date'], request.form['time'])
    date_time_fmt = datetime.strptime(date_time, '%Y-%m-%d %H:%M')
    new_trolley_record = TrolleyModel(
        trolley_id=request.form['trolleyId'],
        recorded_date_time=date_time_fmt,
        temperature=int(request.form['temperature'])
    )

    new_trolley_record.save()

    return redirect(url_for('trolley.upload'))


@trolley_routes.route('/graphLayout')
@protected_route()
def graph_layout():
    graph_layout_data = get_single_day_graphs_layout()

    return jsonify({'data': json.dumps(graph_layout_data)})
