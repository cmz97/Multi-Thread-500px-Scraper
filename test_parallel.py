from selenium import webdriver
import threading
import time


def test_logic():
    driver = webdriver.Firefox()
    url = 'https://www.google.co.in'
    driver.get(url)
    # Implement your test logic
    time.sleep(2)
    driver.quit()

N = 5   # Number of browsers to spawn
thread_list = list()

# Start test
for i in range(N):
    t = threading.Thread(name='Test {}'.format(i), target=test_logic)
    t.start()
    time.sleep(1)
    print(t.name + ' started!')
    thread_list.append(t)

# Wait for all thre<ads to complete
for thread in thread_list:
    thread.join()

print ('Test completed!')
