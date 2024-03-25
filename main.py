import threading
import random
import time

# The values for the constants
LOWER_NUM = 1
UPPER_NUM = 10000
BUFFER_SIZE = 100
MAX_COUNT = 10000

buffer = []
lock = threading.Lock()
producer_done = threading.Event()

even_batch = []
odd_batch = []

def producer():
    generated_numbers = set()
    for _ in range(MAX_COUNT):
        while True:
            num = random.randint(LOWER_NUM, UPPER_NUM)
            if num not in generated_numbers:
                break
        generated_numbers.add(num)
        with lock:
            buffer.append(num)
            if len(buffer) > BUFFER_SIZE:
                buffer.pop(0)
    producer_done.set()

def consumer_even():
    while not producer_done.is_set() or buffer:
        with lock:
            if buffer and buffer[-1] % 2 == 0:
                num = buffer.pop()
                even_batch.append(num)
                if len(even_batch) >= BUFFER_SIZE:
                    with open("even.txt", "a") as f:
                        f.write("\n".join(map(str, even_batch)) + "\n")
                    even_batch.clear()

def consumer_odd():
    while not producer_done.is_set() or buffer:
        with lock:
            if buffer and buffer[-1] % 2 != 0:
                num = buffer.pop()
                odd_batch.append(num)
                if len(odd_batch) >= BUFFER_SIZE:
                    with open("odd.txt", "a") as f:
                        f.write("\n".join(map(str, odd_batch)) + "\n")
                    odd_batch.clear()

if __name__ == "__main__":
    start_time = time.time()

    print("Starting Producer thread...")
    producer_thread = threading.Thread(target=producer)
    print("Starting Even Consumer thread...")
    consumer_even_thread = threading.Thread(target=consumer_even)
    print("Starting Odd Consumer thread...")
    consumer_odd_thread = threading.Thread(target=consumer_odd)

    producer_thread.start()
    consumer_even_thread.start()
    consumer_odd_thread.start()

    producer_thread.join()
    consumer_even_thread.join()
    consumer_odd_thread.join()

    end_time = time.time()

    print("Execution time:", end_time - start_time, "seconds")
