import os
from slack_sdk import WebClient
import pprint
import dataset

pp = pprint.PrettyPrinter(indent=4)
client = WebClient(token=os.environ["SLACK_BOT_TOKEN"])
#response = client.conversations_open(users=["U01J96P0NGG"])

#print(response)
db = dataset.connect('sqlite:///slackback.db')

################################################ USERS ####################################################################
def save_users(users_array):
    for user in users_array:
        user_id = user["id"]
        user_name = user["name"]
        user_real_name = user["real_name"]
        user_display_name = user["profile"]["display_name"]

        user_entity = dict(slack_id=user_id, name=user_name, real_name=user_real_name, display_name=user_display_name)

        table_user = db['user']
        table_user.upsert(user_entity, ["slack_id"])

        print("Saved user: ")
        print(user_entity)


def get_and_save_all_users():
    try:
        result = client.users_list()
    except SlackApiError as e:
        logger.error("Error fetching users: {}".format(e))
    save_users(result["members"])

################################################### CHANNELS ########################################################################    

def save_channels(channels):
    for channel in channels:
        channel_id = channel["id"]
        channel_name = channel["name"]

        channel_entity = dict(slack_id=channel_id, name=channel_name)

        table_channel = db['channel']
        table_channel.upsert(channel_entity, ["slack_id"])

        print("Saved channel: ")
        print(channel_entity)
        
def get_and_save_all_channels():
    try:
        result = client.conversations_list()
    except SlackApiError as e:
        logger.error("Error fetching channels: {}".format(e))
    save_channels(result["channels"])


################################################### CONVERSATIONS - DIRECT ############################################################
def save_direct_messages(messages):
    for message in messages:
        message_id = message["client_msg_id"]
        message_text = message["text"]
        message_user_id = message["user"]
        message_ts = message["ts"]

        message_entity = dict(slack_id=message_id, text=message_text, user_id=message_user_id, ts=message_ts)

        table_message = db['message_direct']
        table_message.upsert(message_entity, ["slack_id"])

        print("Saved message: ")
        print(message_entity)


def get_and_save_all_direct_conversations():
    user_ids_result = db.query('SELECT slack_id FROM user')
    user_ids = [x['slack_id'] for x in user_ids_result]

    for user_id in user_ids:
        results = client.conversations_open(users=[user_id])
        print(results)

        for result in results:
            direct_conversations = get_conversations_for_channel(result["channel"]["id"])
            messages = direct_conversations["messages"]
            save_direct_messages(messages)


################################################### CONVERSATIONS - CHANNELS ############################################################


def get_conversations_for_channel(channel):
    return client.conversations_history(channel=channel)


def save_channel_messages(messages):
    for message in messages:
        print(message)
        try:
            message_id = message["client_msg_id"]
        except KeyError:
            pass
        message_text = message["text"]
        message_user_id = message["user"]
        message_ts = message["ts"]

        message_entity = dict(slack_id=message_id, text=message_text, user_id=message_user_id, ts=message_ts)

        table_message = db['message_channel']
        table_message.upsert(message_entity, ["slack_id"])

        print("Saved message: ")
        print(message_entity)

def get_and_save_all_channel_conversations():
    channel_ids_result = db.query('SELECT slack_id FROM channel')
    channel_ids = [x['slack_id'] for x in channel_ids_result]
    print(channel_ids)

    for channel_id in channel_ids:
        channel_conversations = get_conversations_for_channel(channel_id)
        print(channel_conversations)
        messages = channel_conversations["messages"]

        save_channel_messages(messages)
    

get_and_save_all_users()
get_and_save_all_channels()
get_and_save_all_direct_conversations()
get_and_save_all_channel_conversations()
