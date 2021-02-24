from listingParser import parseListing
from search import search
import threading
import queue


if __name__ == "__main__":
  hrefs = search()
  que = queue.Queue()
  thread_list = []

  for href in hrefs:
    t = threading.Thread(target=lambda que, href: que.put(parseListing(href)), args=(que, href))
    t.start()
    thread_list.append(t)
  
  for thread in thread_list:
    thread.join()

  while not que.empty():
    result = que.get()
    print(result)