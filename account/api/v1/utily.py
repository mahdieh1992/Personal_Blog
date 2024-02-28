from threading import Thread
from time import sleep


class ThreadEmail(Thread):
    """
    thread for Send email quickly
    """

    def __init__(self, Email):
        super().__init__()
        self.email = Email

    def run(self):  # thread is active
        sleep(2)
        self.email.send()
