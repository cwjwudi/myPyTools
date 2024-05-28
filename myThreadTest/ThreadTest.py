import threading
import time
import queue

# 创建一个共享的队列
shared_queue = queue.Queue()

# 生产者线程
def producer():
    for i in range(50):
        shared_queue.put(i)
        print(f"Produced {i}")
        time.sleep(1)

# 消费者线程
def consumer():
    while True:
        item = shared_queue.get()
        if item is None:
            break
        print(f"Consumed {item}")
        shared_queue.task_done()

# 创建生产者和消费者线程
producer_thread = threading.Thread(target=producer)
consumer_thread = threading.Thread(target=consumer)

# 启动线程
producer_thread.start()
consumer_thread.start()

# 等待生产者线程完成
producer_thread.join()

# 停止消费者线程
shared_queue.put(None)
consumer_thread.join()

