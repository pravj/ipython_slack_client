import time
from slackclient import SlackClient
from kernel_client import KernelClient

slack_token = os.environ["SLACK_API_TOKEN"]
sc = SlackClient(slack_token)

kc = KernelClient()

if sc.rtm_connect():
    while sc.server.connected is True:
        # collect event payloads from real-time API stream
        event_payloads = sc.rtm_read()

        # ignore empty events
        if len(event_payloads) != 0:
            event_payload = event_payloads[0]

            # subscribe to new message events
            # ignore message edit events
            # ignore new message as a bot response
            if event_payload.get('type', '') == 'message' and\
            event_payload.get('subtype', '') != 'message_changed' and\
            'bot_id' not in event_payload:
                print('message', event_payload)

                # execute the message string in kernel as code
                execute_reply = kc.execute(event_payload.get('text', ''))

                # update the parent message with result using formatting
                sc.api_call(
                    "chat.update",
                    channel=event_payload['channel'],
                    ts=event_payload['ts'],
                    attachments=[{"color": "#87ceeb", "pretext": "", "text": event_payload['text']}]
                )

                if execute_reply != '':
                    # add new message for result using formatting
                    print('waiting')
                    time.sleep(1)
                    print("RESULT", execute_reply)

                    sc.api_call(
                        "chat.postMessage",
                        channel=event_payload['channel'],
                        attachments=[{"color": "#36a64f", "pretext": "", "text": execute_reply}],
                        as_user=True
                    )
            else:
                print(event_payload, 'failed')

        # set polling period as 1 second
        time.sleep(1)
else:
    print("Connection Failed")