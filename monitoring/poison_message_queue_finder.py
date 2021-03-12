import argparse
import json
import urllib.parse

import requests
from requests import ConnectionError, HTTPError
from requests.auth import HTTPBasicAuth

from config import Config


def parse_arguments():
    parser = argparse.ArgumentParser(description='Find queues with high redelivery rates etc')
    parser.add_argument('-r', '--redeliver', help='queues which are redelivering only', action='store_true')
    return parser.parse_args()


def main():
    args = parse_arguments()

    get_queue_stats(args)
    get_connection_stats()
    get_churn_stats()
    get_bad_message_counts()


def get_queue_stats(args):
    v_host = urllib.parse.quote(Config.RABBITMQ_VHOST, safe='')

    response = requests.get(f"http://{Config.RABBITMQ_HOST}:{Config.RABBITMQ_HTTP_PORT}/api/queues/",
                            auth=HTTPBasicAuth(Config.RABBITMQ_USER, Config.RABBITMQ_PASSWORD))

    response.raise_for_status()

    all_queues = response.json()

    for queue in all_queues:
        try:
            queue_name = queue['name']
        except [TypeError, KeyError]:
            print(f'Unexpected data for queue: {queue}')
            continue

        queue_details_response = requests.get(
            f'http://{Config.RABBITMQ_HOST}:{Config.RABBITMQ_HTTP_PORT}/api/queues/{v_host}/{queue_name}',
            auth=HTTPBasicAuth(Config.RABBITMQ_USER, Config.RABBITMQ_PASSWORD))

        queue_details_response.raise_for_status()

        queue_details = queue_details_response.json()

        redeliver_rate = queue_details.get('message_stats', {}).get('redeliver_details', {}).get('rate', 0)
        publish_rate = queue_details.get('message_stats', {}).get('publish_details', {}).get('rate', 0)
        ack_rate = queue_details.get('message_stats', {}).get('ack_details', {}).get('rate', 0)
        total_messages = queue_details.get('messages', 0)
        consumer_count = len(queue_details.get('consumer_details', {}))

        ''' We want to alert on percentage rate of change.
        if a queue is sitting at zero messages and any come in,
        that gets evaluated as a massive percentage, wrongly triggering alerts.
        To get around this, we log the total messages plus one
        to get reasonable percentage changes even if the queue is normally empty'''
        adjusted_total_messages = total_messages + 1

        json_to_log = {
            "queue_name": queue_name,
            "redeliver_rate": redeliver_rate,
            "publish_rate": publish_rate,
            "ack_rate": ack_rate,
            "total_messages": total_messages,
            "consumer_count": consumer_count,
            "adjusted_total_messages": adjusted_total_messages,
        }

        if args.redeliver and redeliver_rate > 1 or not args.redeliver:
            print(json.dumps(json_to_log))


def get_churn_stats():
    response = requests.get(f"http://{Config.RABBITMQ_HOST}:{Config.RABBITMQ_HTTP_PORT}/api/overview",
                            auth=HTTPBasicAuth(Config.RABBITMQ_USER, Config.RABBITMQ_PASSWORD))
    response.raise_for_status()

    churn = response.json()['churn_rates']

    churn_output = {'connection_closed_rate': churn["connection_closed_details"]["rate"],
                    'connections_created_rate': churn["connection_created_details"]["rate"],
                    'connection_closed_add_created_rate':
                        churn["connection_closed_details"]["rate"] + churn["connection_created_details"]["rate"],
                    'channel_closed_rate': churn["channel_closed_details"]["rate"],
                    'channel_created_rate': churn["channel_created_details"]["rate"],
                    'channel_closed_add_created_rate':
                        churn["channel_closed_details"]["rate"] + churn["channel_created_details"]["rate"],
                    }

    print(json.dumps(churn_output))


def get_connection_stats():
    response = requests.get(f"http://{Config.RABBITMQ_HOST}:{Config.RABBITMQ_HTTP_PORT}/api/connections/",
                            auth=HTTPBasicAuth(Config.RABBITMQ_USER, Config.RABBITMQ_PASSWORD))

    response.raise_for_status()

    all_connections = response.json()

    node_data = {}

    for connection_details in all_connections:

        node_name = connection_details.get('node')
        user_name = connection_details.get('user')
        num_of_channels = connection_details.get('channels')

        user_details = None
        node_details = node_data.get(node_name)

        if node_details:
            user_details = node_details.get(user_name)
        else:
            node_data[node_name] = {}

        if not user_details:
            user_details = {
                'number_of_connections': 0,
                'number_of_channels': 0
            }

            node_data[node_name][user_name] = user_details

        user_details['number_of_connections'] = user_details['number_of_connections'] + 1
        user_details['number_of_channels'] = user_details['number_of_channels'] + num_of_channels

    for node_key, node_value in node_data.items():
        for user_key, user_value in node_value.items():
            json_to_dump = {
                'node': node_key,
                'user': user_key,
                'number_of_connections': user_value['number_of_connections'],
                'number_of_channels': user_value['number_of_channels']
            }
            print(json.dumps(json_to_dump))


def get_bad_message_counts():
    try:
        response = requests.get(
            f'{Config.EXCEPTIONMANAGER_URL}/badmessages/summary?minimumSeenCount= \
            {Config.BAD_MESSAGE_MINIMUM_SEEN_COUNT}')
        response.raise_for_status()
    except (ConnectionError, HTTPError) as e:
        print(json.dumps({'severity':'ERROR', 'error': f'Error with exception manager, error: {e}'}))
        return

    messages = response.json()
    queue_counts = {}
    for message in messages:
        for affected_queue in message['affectedQueues']:
            if affected_queue not in queue_counts:
                queue_counts[affected_queue] = 1
            else:
                queue_counts[affected_queue] += 1

    for queue, count in queue_counts.items():
        json_to_log = {
            "queue_name": queue,
            "bad_message_count": count
        }
        print(json.dumps(json_to_log))


if __name__ == "__main__":
    main()
