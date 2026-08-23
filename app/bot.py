from slack_bolt import App

from app.commands.vasudown import handle_vasudown


def create_app(token):
    app = App(token=token)

    app.command("/vasudown")(handle_vasudown)

    return app