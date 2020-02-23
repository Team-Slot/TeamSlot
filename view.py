import json
import os
import sqlite3
from threading import Thread

import slack
import datetime

from flask import Flask, request

from ScheduleCore import ScheduleCore
import re

app = Flask(__name__)


@app.route('/slack/commands', methods=['POST'])
def handle_commands():
    info = request.form
    trigger_id = info['trigger_id']
    command = info['command']

    user_id = info['user_id']
    if command == '/ts' or command == '/ts-help':
        push_block('help', user_id)
    elif command == '/ts-start':
        text = fill_block('setup', [('Master_ID', [user_id])])
        open_modal_str(text, trigger_id)
    elif command == '/ts-select':
        options = options_from_db()
        filled = fill_block('request', [('Meeting', options)])
        open_modal_str(filled, trigger_id)
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
            thread = Thread(target=calculate_options_to_db, args=(users, date_range, working_hours, time_duration, description, user_id))
            thread.start()
        elif title == 'Meeting Request':
            selected = values['meetings']['meeting']['selected_options']
            allValues = info['view']['blocks'][0]['element']['options']
            if len([s for s in selected if s['value'] == 'allMeetings']) > 0:
                write_options([v['text']['text'] for v in allValues if v != 'All options are fine'], user_id)
            else:
                options = list()
                for s in selected:
                    options.append(s['text']['text'])
                write_options(options, user_id)
            db = sqlite3.connect('teamslot.db')
            c = db.cursor()
            c.execute('''SELECT COUNT(*) FROM availables
                        GROUP BY option''')
            max = c.execute('''SELECT * from user_number''')
            uers = max.fetchone()[0]
            for t in c.fetchall():
                if uers == t[0]:
                    text = fill_block('confirm', [('User',[user_id]), ('Master', [user_id]), ('TimeSlot', [t[0]])])
                    push_block_str(text, user_id)
                    break
    return ''


def write_options(options, user_id):
    db = sqlite3.connect('teamslot.db')
    c = db.cursor()
    for option in options:
        c.execute('''INSERT INTO availables
                     VALUES(?, ?)''', (option, user_id))

    db.commit()
    db.close()


def options_from_db():
    db = sqlite3.connect('teamslot.db')
    c = db.cursor()
    options = list()

    c.execute('''SELECT * FROM options''')
    for start, end in c.fetchall():
        start_time = datetime.datetime.strptime(start, '%Y-%m-%d %H:%M:%S')
        end_time = datetime.datetime.strptime(end, '%Y-%m-%d %H:%M:%S')
        options.append(range_str(start_time, end_time))

    db.commit()
    db.close()
    return options


def range_str(start, end):
    return start.strftime('%H:%M - ') + end.strftime('%H:%M   %d/%m/%Y')


def calculate_options_to_db(users, date_range, working_hours, time_duration, description, master):
    sc = ScheduleCore()
    options = sc.processRequest(users, date_range, working_hours, time_duration, description)
    db = sqlite3.connect('teamslot.db')
    c = db.cursor()

    for begin, end in options:
        c.execute('''INSERT OR REPLACE INTO options
                 VALUES(?, ?)''', (begin, end))

    c.execute('''INSERT INTO user_number
                 VALUES(?)''', (len(users),))

    db.commit()
    db.close()
    for user in users:
        text = fill_block('request_intro', [('User',['@' + get_user_name(user)]), ('Master',['@' + get_user_name(master)]), ('Description', [description])])
        push_block_str(text, user)


def fill_block(file, replacements): # replacements is a list of tuples of word and list
    with open('JSON/{}.json'.format(file)) as json_file:
        text = json_file.read()
    for (word, repls) in replacements:
        i = 0
        sindex = 0
        rindex = 0
        leng = len(text)
        while rindex < leng:
            char = text[rindex]
            if char == '<':
                sindex = text.index('<')
            if char == '>':
                eindex = text.index('>') + 1
                if word in text[sindex:eindex]:
                    text = text[:sindex] + repls[i] + text[eindex:]
                    rindex = 0
                    leng = len(text)
                    i += 1
                    i %= len(repls)
            rindex += 1

    return text


def get_user_name(user_id):
    client = slack.WebClient(token=os.environ['SLACK_API_TOKEN'])

    return client.users_info(user=user_id)['user']['name']


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


def open_modal_str(text, trigger_id):
    client = slack.WebClient(token=os.environ['SLACK_API_TOKEN'])

    client.views_open(trigger_id=trigger_id, view=json.loads(text))


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


def push_block_str(str, user_id):
    client = slack.WebClient(token=os.environ['SLACK_API_TOKEN'])

    client.chat_postMessage(
        channel=user_id,
        blocks=json.loads(str)['blocks']
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
