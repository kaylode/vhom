import threading
import time

class BackgroundTasks(threading.Thread):
    def __init__(self, api, db, run_every_sec, in_loop=True):
        super().__init__()
        self.in_loop = in_loop
        self.api = api
        self.db = db
        self.run_every_sec = run_every_sec
        
    def run(self,*args,**kwargs):
        print(f'Start crawling every {self.run_every_sec} seconds')
        running_time = 0
        while self.in_loop:
            running_time += 1
            time.sleep(1)

            if running_time % self.run_every_sec == 0:
                self.db._crawl_data_on_daily(
                    camera_ids=['tvmytho', 'tvlongdinh'], 
                    lasted_date = self.db._get_last_date('waterlevel'),
                    api=self.api, step=0.5
                )

    def break_loop(self):
        print("Task killed")
        self.in_loop = False