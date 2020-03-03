import time
# import my_code.menu.progress_bar as pb


def print_progress_bar(iteration, total, prefix='', suffix='', decimals=2, length=100, fill='█', printEnd=""):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))

    filled_length = int(length * iteration // total)

    bar = fill * filled_length + '-' * (length - filled_length)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end=printEnd)
    # Print New Line on Complete
    if iteration == total:
        print()


class Stopwatch:
    results = []

    def __init__(self, start=None):
        if start is None:
            start = 0
        self.start = start
        self.total = 0

    def start_watch(self):
        self.start = time.time()
        # print(self.start)

    def stop_watch(self):
        self.total = time.time() - self.start
        self.results.append(self.total)
        # print(self.total)
        return self.total


def timer(timeout):
    watch = Stopwatch()
    passed_time = 0
    tik = 0
    print_progress_bar(passed_time, timeout, length=80, prefix='%.2f/%s' % (passed_time, timeout))
    while (timeout-passed_time) > 0:
        watch.start_watch()
        tik += 1
        time.sleep(1)
        real_sleep = watch.stop_watch() - 1
        passed_time = round(passed_time + 1 + real_sleep, 3)
        print_progress_bar(passed_time, timeout, length=80, prefix='%.2f/%s' % (passed_time, timeout))
    print(f'\nтиков было:{tik}')


# print(" ---------- Проверка таймера---------- \n\n\n\n\n\n\n\n")
timer(3600)
input()
