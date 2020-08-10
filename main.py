import os
import random
import requests
import threading
from time import strftime, gmtime, time, sleep


class TikTok:
    def __init__(self):
        self.added = 0
        self.lock = threading.Lock()

        try:
            self.amount = int(input('> Desired Amount of Shares: '))
        except ValueError:
            self.close('Integer expected.')

        try:
            self.video_id = input('> TikTok Video URL: ').split('/')[5]
        except IndexError:
            self.close(
                'Invalid TikTok URL format.\nFormat expected: https://www.tiktok.com/@username/vide'
                'o/1234567891234567891'
            )
        else:
            if not self.video_id.isdigit():
                self.close(
                    'Invalid TikTok URL format.\nFormat expected: https://www.tiktok.com/@username/'
                    'video/1234567891234567891'
                )
            else:
                print()

    def close(self, message):
        print(f'\n{message}')
        os.system('title [TikTok Shares Botter] - Restart required')
        os.system('pause >NUL')
        os.system('title [TikTok Shares Botter] - Exiting...')
        sleep(3)
        os._exit(0)

    def status(self, code, intention):
        if code == 200:
            self.added += 1
        else:
            self.lock.acquire()
            print(f'Error: {intention} | Status Code: {code}')
            self.lock.release()
            self.bot()

    def update_title(self):
        # Avoid ZeroDivisionError
        while self.added == 0:
            sleep(0.2)

        while self.added < self.amount:
            # Elapsed Time / Added * Remaining
            time_remaining = strftime(
                '%H:%M:%S', gmtime(
                    (time() - self.start_time) / self.added * (self.amount - self.added)
                )
            )
            os.system(
                f'title [TikTok Shares Botter] - Added: {self.added}/{self.amount} '
                f'({round(((self.added / self.amount) * 100), 3)}%) ^| Active Threads: '
                f'{threading.active_count()} ^| Time Remaining: {time_remaining}'
            )
            sleep(0.2)
        os.system(
            f'title [TikTok Shares Botter] - Added: {self.added}/{self.amount} '
            f'({round(((self.added / self.amount) * 100), 3)}%) ^| Active Threads: '
            f'{threading.active_count()} ^| Time Remaining: 00:00:00'
        )

    def bot(self):
        action_time = round(time())
        device_id = ''.join(random.choice('0123456789') for _ in range(19))

        data = (
            f'aweme_type=0&item_id={self.video_id}&share_delta=1'
        )
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'x-common-params-v2': 'version_code=16.6.1&app_name=musical_ly&channel=App%20Store&devi'
                                  f'ce_id={device_id}&aid=1233&os_version=13.5&device_platform=ip'
                                  'hone&device_type=iPhone8,1',
            'User-Agent': 'TikTok 16.6.1 rv:166103 (iPhone; iOS 13.5; es_US) Cronet'
        }

        try:
            response = requests.post(
                'https://api2.musical.ly/aweme/v1/aweme/stats/?ac=WIFI&op_region=US&app_skin=white&', data=data, headers=headers, verify=False
            )
        except Exception as e:
            print(f'Error: {e}')
            self.bot()
        else:
            if all(i not in response.text for i in ['Service Unavailable', 'Gateway Timeout']):
                self.status(response.status_code, response.text)
            else:
                self.bot()

    def start(self):
        self.start_time = time()
        threading.Thread(target=self.update_title).start()

        for _ in range(self.amount):
            while True:
                if threading.active_count() <= 300:
                    threading.Thread(target=self.bot).start()
                    break

        os.system('pause >NUL')
        os.system('title [TikTok Shares Botter] - Exiting...')
        sleep(3)


if __name__ == '__main__':
    os.system('cls && title [TikTok Shares Botter]')
    main = TikTok()
    main.start()
