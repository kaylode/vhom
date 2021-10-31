import threading
import time

class BackgroundTasks(threading.Thread):
    """
    Background task that starts another thread to run
    This is used to crawl data on every timestamp
    """
    def __init__(self, api, db, run_every_sec, in_loop=True):
        super().__init__()
        self.in_loop = in_loop
        self.api = api
        self.db = db
        self.run_every_sec = run_every_sec
        
    def run(self,*args,**kwargs):
        print(f'Start crawling every {self.run_every_sec} seconds')
        running_time = 0

        # Start loop
        while self.in_loop:

            # This is instead of sleep(run_every_sec), for capability to break at anytime
            running_time += 1
            time.sleep(1)

            # Crawl all new data based on date in database
            if running_time % self.run_every_sec == 0:
                self.db._crawl_data_on_daily(
                    camera_ids=['tvmytho', 'tvlongdinh'], 
                    lasted_date = self.db._get_last_date('waterlevel'),
                    api=self.api, step=0.5
                )

    def break_loop(self):
        print("Task killed")
        self.in_loop = False