import json
from datetime import datetime

from flask import Blueprint, render_template, request, redirect, url_for, jsonify, session

from Helpers.middleware import protected_route
from Q2.Trolley.model import TrolleyModel
from Q2.Trolley.service import get_all_trolleys, get_single_day_graphs_layout

trolley_routes = Blueprint("trolley", __name__)


@trolley_routes.route('/upload')
@protected_route()
def upload():
    all_trolleys = get_all_trolleys()
    email = session['email']
    return render_template("Upload.html", all_trolleys=all_trolleys, email=email)


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
