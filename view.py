import json
import os
import sqlite3
import slack

from flask import Flask, request
app = Flask(__name__)


@app.route('/slack/commands', methods=['POST'])
def handle_commands():
    info = request.form
    trigger_id = info['trigger_id']
    command = info['command']

    if command == '/ts' or command == '/ts-help':
        pass
    elif command == '/ts-start':
        open_modal(trigger_id, 'setup')
    elif command == '/ts-select':
        open_modal(trigger_id, 'select')
    elif command == '/ts-confirm':
        open_modal(trigger_id, 'confirm')
    elif command == '/ts-config':
        open_modal(trigger_id, 'config')
    return ''


@app.route('/slack/events', methods=['POST'])
def handle_events():
    info = request.json
    event = info['event']
    event_type = event['type']

    if event_type == 'team_join':
        user_id = event['user']  # TODO
        prompt_for_ical(user_id)
    elif event_type == 'app_home_opened':
        print('hey')
        user_id = event['user']
        if not is_user_stored(user_id):
            prompt_for_ical(user_id)
        else:
            pass
    elif event_type == 'message' and event['channel_type'] == 'im' and 'client_msg_id' in event:
        print('heyo')  # will become modal so change

    print(str(request.json))
    return ''


def prompt_for_ical(user_id):
    client = slack.WebClient(token=os.environ['SLACK_API_TOKEN'])

    client.chat_postMessage(
        channel=user_id,
        blocks=[get_blocks('intro')]
        )


def store_user(user_id, ical_link):
    db = sqlite3.connect('teamslot.db')
    c = db.cursor()

    c.execute('''INSERT OR REPLACE INTO users
                 VALUES(?, ?)''', (user_id, ical_link))

    db.close()


def open_modal(trigger_id, file):
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



def push_block(block_name):
    pass  # TODO


def is_user_stored(user_id):
    db = sqlite3.connect('teamslot.db')
    c = db.cursor()

    c.execute('''SELECT * FROM users WHERE id=?''', (user_id,))  # singleton tuple
    stored = len(c.fetchall()) > 0
    db.close()  # not 100% sure i have to close after c.fetchall, could just close then return, but idk

    return stored


if __name__ == '__main__':
    app.run(port=3000)