import threading
import time

def run_in_thread(func):
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=func, args=args, kwargs=kwargs)
        thread.start()
        return thread
    return wrapper

@run_in_thread
def timer(name, delay, repeat):
    print(f"Timer: {name} started")
    while repeat > 0:
        time.sleep(delay)
        print(f"{name}: {time.ctime(time.time())}")
        repeat -= 1
    print(f"Timer: {name} completed")

# 创建两个计时器任务
timer("Timer1", 1, 5)
timer("Timer2", 2, 3)
