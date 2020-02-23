import sqlite3
import slack

from flask import Flask, request
app = Flask(__name__)


@app.route('/slack/hello', methods=['POST'])
def hello_world():
    info = request.json
    event = info['event']

    if event['type'] == 'team_join':
        user_id = event['id']  # TODO
        store_user()
    elif event['type'] == 'app_home_opened':
        user_id = event['id']
        channel_id = event['channel']
        if not is_user_stored(user_id):
            store_user(user_id, channel_id)
        else:
            pass

    print(str(request.json))
    return ''


def store_user(user_id, channel_id):
    pass


def push_block(block_name):
    pass  # TODO


def is_user_stored(user_id):
    db = sqlite3.connect('teamslot.db')
    c = db.cursor()

    c.execute('''SELECT * FROM users WHERE id=?''', (user_id,))  # singleton tuple
    stored = len(c.fetchall()) > 0
    c.close()  # not 100% sure i have to close after c.fetchall, could just close then return, but idk

    return stored


if __name__ == '__main__':
    app.run(port=3000)