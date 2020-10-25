import datetime
import functools
from datetime import timedelta

from Q2.Trolley.model import TrolleyModel


def get_all_trolley_data_by_date():
    current_day_states = TrolleyModel.objects.aggregate([
        {"$match": {"recorded_date_time": {'$lte': datetime.datetime.now(),
                                           "$gte": datetime.datetime.now() - timedelta(hours=24)}}}
    ])
    return list(current_day_states)


def get_states():
    current_day_states = get_all_trolley_data_by_date()

    active_trolleys = len(current_day_states) or 0
    max_temperature = max([t['temperature'] for t in current_day_states]) if len(current_day_states) else 0
    min_temperature = min(t['temperature'] for t in current_day_states) if len(current_day_states) else 0
    total_trolleys = TrolleyModel.objects.count()

    return active_trolleys, max_temperature, min_temperature, total_trolleys


def get_all_trolleys():
    all_objects = TrolleyModel.objects.aggregate([
        {"$sort": {"recorded_date_time": -1}}
    ])
    return list(all_objects)


def get_single_day_graphs_layout():
    current_day_states = get_all_trolley_data_by_date()

    states_modified = {}
    for state in current_day_states:
        if state['trolley_id'] not in states_modified.keys():
            states_modified[state['trolley_id']] = {
                'type': "scatter",
                'mode': "lines",
                'name': state['trolley_id'],
                'x': [],
                'y': [],
                # 'line': {'color': '#7F7F7F'}
            }

        states_modified[state['trolley_id']]['x'].append(str(state['recorded_date_time']))
        states_modified[state['trolley_id']]['y'].append(state['temperature'])

    return list(states_modified.values())
