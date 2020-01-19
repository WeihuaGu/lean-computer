# -*- coding: utf-8 -*-

"""Using a Semaphore to synchronize threads"""
import threading
import time
import numpy as np
mutex = threading.Semaphore(1)
semempty = threading.Semaphore(1)
semodd = threading.Semaphore(0)
semeven = threading.Semaphore(0)

def oddConsumer():
	while(True):
		semodd.acquire()
		print("奇数消费者执行");
		mutex.acquire()
		oddnum = intnum
		#intnum = 0
		mutex.release()
		print("消费奇数: %s" %oddnum)
		print("\n")
		semempty.release()

def evenConsumer():
	while(True):
		semeven.acquire()
		print("偶数消费者执行");
		mutex.acquire()
		evennum = intnum
		#intnum = 0
		mutex.release()
		print("消费奇数: %s" % evennum)
		print("\n")
		time.sleep(15)
		semempty.release()

def numProducer():
	global intnum
	while(True):
		print("生产者执行")
		semempty.acquire()
		randomnum=np.random.randint(1,100)
		print("产生整数: %s" % randomnum)
		print("\n")
		mutex.acquire()
		intnum = randomnum
		if(intnum%2==0):
			semeven.release()
		else:
			semodd.release()
		mutex.release()
		time.sleep(5)

t1=threading.Thread(target=oddConsumer);
t1.start();
t2=threading.Thread(target=evenConsumer);
t2.start();
t3=threading.Thread(target=numProducer);
t3.start();



