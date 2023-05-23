import time

def countdown(num_of_secs):
    while num_of_secs:
        m, s = divmod(num_of_secs, 60)
        min_sec_format = 'Подождите, пожалуйста, {:02d}:{:02d}\r'.format(m, s)
        print(min_sec_format)
        time.sleep(1)
        num_of_secs -= 1


if __name__ == '__main__':
    countdown(2)