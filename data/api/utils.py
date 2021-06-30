from threading import Thread


class UpdateThread(Thread):
    def __init__(self, market):
        super(UpdateThread, self).__init__()
        self.market = market

    def run(self):
        self.market.update_data()