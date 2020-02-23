import json
import os
import sqlite3
import slack
import datetime

from flask import Flask, request

from ScheduleCore import ScheduleCore

app = Flask(__name__)


@app.route('/slack/commands', methods=['POST'])
def handle_commands():
    info = request.form
    trigger_id = info['trigger_id']
    command = info['command']

    if command == '/ts' or command == '/ts-help':
        push_block('help', info['user'])
    elif command == '/ts-start':
        open_modal('setup', trigger_id)
    elif command == '/ts-select':
        open_modal('request', trigger_id)
    elif command == '/ts-confirm':
        open_modal('confirm_request', trigger_id)
    elif command == '/ts-config':
        open_modal('config', trigger_id)
    return ''


@app.route('/slack/events', methods=['POST'])
def handle_events():
    info = request.json
    event = info['event']
    event_type = event['type']
    user_id = event['user']

    if event_type == 'team_join':
        push_block('intro', user_id)
    elif event_type == 'app_home_opened':
        if not is_user_stored(user_id):
            push_block('intro', user_id)
        else:
            pass

    return ''


@app.route('/slack/requests', methods=['POST'])
def handle_requests():
    info = json.loads(request.form['payload'])

    if 'type' in info and info['type'] == 'view_submission':
        title = info['view']['title']['text']
        user_id = info['user']['id']
        values = info['view']['state']['values']

        if title == 'Configuration':
            store_user(user_id, values['calendar']['calendar_input']['value'])
            push_block('start', user_id)
        elif title == 'Plan Meeting':
            users = values['participants']['participants_list']['selected_users']
            start_date = values['start_date']['start']['selected_date']
            start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
            end_date = values['end_date']['end']['selected_date']
            end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
            date_range = (start_date, end_date)
            min_time = values['min_time']['min_time_menu']['selected_option']['text']['text']
            min_time = datetime.datetime.strptime(min_time, '%H:%M').time()
            max_time = values['max_time']['max_time_menu']['selected_option']['text']['text']
            max_time = datetime.datetime.strptime(max_time, '%H:%M').time()
            working_hours = (min_time, max_time)
            time_duration = values['duration']['time_duration']['selected_option']['value']
            time_duration = datetime.timedelta(hours=int(int(time_duration[-1]) * 0.5))
            description = values['description']['description_field']['value']
            sc = ScheduleCore()
            sc.processRequest(users, date_range, working_hours, time_duration, description)
        elif title == 'Meeting Request':
            print()
    return ''


def store_user(user_id, ical_link):
    db = sqlite3.connect('teamslot.db')
    c = db.cursor()

    c.execute('''INSERT OR REPLACE INTO users
                 VALUES(?, ?)''', (user_id, ical_link))

    db.commit()
    db.close()


def open_modal(file, trigger_id):
    client = slack.WebClient(token=os.environ['SLACK_API_TOKEN'])

    client.views_open(trigger_id=trigger_id, view=get_view(file))


def get_view(file):
    with open('JSON/{}.json'.format(file)) as json_file:
        data = json.load(json_file)
        return data


def get_blocks(file):
    with open('JSON/{}.json'.format(file)) as json_file:
        data = json.load(json_file)
        return data['blocks']


def push_block(block_name, user_id):
    client = slack.WebClient(token=os.environ['SLACK_API_TOKEN'])

    client.chat_postMessage(
        channel=user_id,
        blocks=get_blocks(block_name)
    )


def is_user_stored(user_id):
    db = sqlite3.connect('teamslot.db')
    c = db.cursor()

    c.execute('''SELECT * FROM users WHERE id=?''', (user_id,))  # singleton tuple
    stored = len(c.fetchall()) > 0
    db.close()  # not 100% sure i have to close after c.fetchall, could just close then return, but idk

    return stored


if __name__ == '__main__':
    app.run(port=3000)
