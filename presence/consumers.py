import json

from channels.generic.websocket import WebsocketConsumer


class PresenceConsumer(WebsocketConsumer):

    connections = []

    def connect(self):
        self.accept()
        self.user = self.scope["user"]
        self.connections.append(self)
        self.update_indicator(msg="Connected")

    def disconnect(self, code):
        self.update_indicator(msg="Disconnected")
        self.connections.remove(self)
        return super().disconnect(code)

    def update_indicator(self, msg):
        for connection in self.connections:
            connection.send(
                text_data=json.dumps(
                    {
                        "msg": f"{self.user} {msg}",
                        "online": f"{len(self.connections)}",
                        "users": [f"{user.scope['user']}" for user in self.connections],                        
                    }
                )
            )

    def receive(self, text_data=None, bytes_data=None):
        for connection in self.connections:
            connection.send(
                text_data=json.dumps(
                    {
                        "msg": f"{self.user}: {text_data}",
                        "online": f"{len(self.connections)}",
                        "users": [user.scope["user"].username or "Anon" for user in self.connections],
                    }
                )
            )
