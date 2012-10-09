'''import threading
import time
class timer(threading.Thread): #The timer class is derived from the class threading.Thread
    def __init__(self, num, interval):
        threading.Thread.__init__(self)
        self.thread_num = num
        self.interval = interval
        self.thread_stop = False

    def run(self): #Overwrite run() method, put what you want the thread do here
        while not self.thread_stop:
            print 'Thread Object(%d), Time:%s\n' %(self.thread_num, time.ctime())
            time.sleep(self.interval)
    def stop(self):
        self.thread_stop = True


def test():
    thread1 = timer(1, 1)
    thread2 = timer(2, 2)
    thread1.start()
    thread2.start()
    time.sleep(10)
    thread1.stop()
    thread2.stop()
    return

if __name__ == '__main__':
    test()'''
'''import threading
mylock = threading.RLock()
num=0

class myThread(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.t_name = name

    def run(self):
        global num
        while True:
            mylock.acquire()
            print '\nThread(%s) locked, Number: %d'%(self.t_name, num)
            if num>=4:
                mylock.release()
                print '\nThread(%s) released, Number: %d'%(self.t_name, num)
                break
            num+=1
            print '\nThread(%s) released, Number: %d'%(self.t_name, num)
            mylock.release()

def test():
    thread1 = myThread('A')
    thread2 = myThread('B')
    thread1.start()
    thread2.start()

if __name__== '__main__':
    test()'''
import thread
mylock = thread.allocate_lock()  #Allocate a lock
num=0  #Shared resource

def add_num(name):
    global num
    while True:
        mylock.acquire() #Get the lock
        # Do something to the shared resource
        print 'Thread %s locked! num=%s'%(name,str(num))
        if num >= 5:
            print 'Thread %s released! num=%s'%(name,str(num))
            mylock.release()
            thread.exit_thread()
        num+=1
        print 'Thread %s released! num=%s'%(name,str(num))
        mylock.release()  #Release the lock.

def test():
    thread.start_new_thread(add_num, ('A',))
    thread.start_new_thread(add_num, ('B',))

if __name__== '__main__':
    test()

