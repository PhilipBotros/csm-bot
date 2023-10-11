from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler

from slack_bolt.oauth.oauth_settings import OAuthSettings
from slack_sdk.oauth.installation_store import FileInstallationStore
from slack_sdk.oauth.state_store import FileOAuthStateStore

import config
from src.langmodel import ChatWithContext

oauth_settings = OAuthSettings(
    client_id=config.SLACK_CLIENT_ID,
    client_secret=config.SLACK_CLIENT_SECRET,
    scopes=["chat:write", "app_mentions:read", "im:history", "im:read"],
    installation_store=FileInstallationStore(base_dir=config.SLACK_FILE_INSTALLATION_STORE_BASEDIR),
    state_store=FileOAuthStateStore(expiration_seconds=600, base_dir=config.SLACK_OAUTH_STATE_STORE_BASEDIR)
)

slack_app = App(
    signing_secret=config.SLACK_SIGNING_SECRET,
    oauth_settings=oauth_settings
)
slack_handler = SlackRequestHandler(slack_app)

chat_service = ChatWithContext()


@slack_app.event("app_mention")
def event_test(body, say, logger):
    question = body["event"]["text"]
    answer = chat_service.talk(question)

    logger.info("<{}> {}".format(body, answer))

    say(answer)


@slack_app.event("app_home_opened")
def update_home_tab(client, event, logger):
    logger.info("<{}> {}".format(event, event["user"]))
    client.views_publish(
            # Use the user ID associated with the event
            user_id=event["user"],
            # Home tabs must be enabled in your app configuration
            view={
                "type": "home",
                "blocks": [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "*Welcome home, <@" + event["user"] + "> :house:*"
                        }
                    },
                    {
                        "type": "section",
                        "text": {
                          "type": "mrkdwn",
                          "text": "Learn how home tabs can be more useful and interactive <https://api.slack.com/surfaces/tabs/using|*in the documentation*>."
                        }
                    }
                ]
            }
        )
