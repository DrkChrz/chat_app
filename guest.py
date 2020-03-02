class Guest:
    """
    Represents a new user joining the server. Holds socket client, IP address, name and date of joining the server.
    """

    def __init__(self, conn, addr, when_joined):
        self.conn = conn
        self.addr = addr
        self.when_joined = when_joined
        self.name = ""

    def set_name(self, name):
        """
        Sets a name for a new user.
        :param name: name of a new user
        :type name: str
        :return: None
        """
        self.name = name

    def get_connection(self):
        """
        Retrieves socket client.
        :return: socket
        """
        return self.conn

    def get_name(self):
        """
        Retrieves name a user.
        :return: str
        """
        return self.name
