import pika


class RabbitMQConnection:
    def __init__(self, host = 'localhost', port = 5672, username = 'guest', password = 'guest'):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.connection = None

    def connect(self):
        credentials = pika.PlainCredentials(self.username, self.password)
        parameters = pika.ConnectionParameters(host = self.host, port = self.port, credentials = credentials)
        self.connection = pika.BlockingConnection(parameters)

    def get_connection(self):
        if not self.connection or self.connection.is_closed:
            self.connect()
        return self.connection
