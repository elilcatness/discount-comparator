import time

from data.parsers.dixy import Dixy
from data.db import db_session
from threading import Thread


class UpdateThread(Thread):
    def __init__(self, market):
        super(UpdateThread, self).__init__()
        self.market = market

    def run(self):
        self.market.update_data()


def main():
    session = db_session.create_session()
    for market in session.query(Dixy).all():
        print(f'market: {market}')
        print(f'Started initializing ...', end='\r')
        market.__init__()
        print(' Finished')
        thread = UpdateThread(market)
        thread.start()
    start_time = time.time()
    while time.time() - start_time <= 120:
        print('I AM GOING')
        time.sleep(1)


if __name__ == '__main__':
    db_session.global_init('data/db/base.db')
    main()