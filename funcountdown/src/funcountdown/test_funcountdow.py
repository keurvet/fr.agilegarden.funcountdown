# -*- coding: utf-8 -*-
'''
Created on 4 févr. 2012

@author: pierrick
'''
import unittest
import time
from funcountdown import SecondNotifier, CountDown

class TestCountDown(unittest.TestCase):    
    def setUp(self):
        self.history = []
        self.historyStr = []
        self.notifier = SecondNotifier(0.000001)
        self.notifier.register(self)
        self.countDown = CountDown(0, self.notifier)
        self.notifier.register(self.countDown)

    def testGiven0SecondsCountDownLaunchedThenOnlyDisplay0(self):
        self.countDown.count = 0
        
        self.notifier.start()
        time.sleep(0.01)
        self.notifier.start()
        time.sleep(0.01)
        self.notifier.stop()
        expected = [0]
        self.assertEquals(expected, self.history)
      
    def testGiven10SecondscountDownLaunchedThencountDownFrom10To0(self):
        self.countDown.count = 10
        
        self.notifier.start()
        time.sleep(0.1)
        self.notifier.stop()
        expected = range(11)
        expected.reverse()
        self.assertEquals(expected, self.history)
      
    def testGiven1h10m0scountDownLaunchedThencountDownFrom1h10m00sTo0m00s(self):
        self.countDown.count = 1 * 3600 + 10 * 60 + 0
        
        self.notifier.start()
        time.sleep(0.1)
        self.notifier.stop()
        expected1 = '1:10:00'
        expected2 = '1:09:02'
        expected3 = '1:00:00'
        expected4 = '0:59:59'
        expected5 = '0:00:00'

        self.assertIn(expected1, self.historyStr)
        self.assertIn(expected2, self.historyStr)
        self.assertIn(expected3, self.historyStr)
        self.assertIn(expected4, self.historyStr)
        self.assertIn(expected5, self.historyStr)
    
    def testGivenSecondThenReturnHourMinuteSecond(self):
        self.countDown.count = 1 * 3600 + 10 * 60 + 21

        self.assertEquals(1, self.countDown.getCountHour())
        self.assertEquals(10, self.countDown.getCountMinute())
        self.assertEquals(21, self.countDown.getCountSecond())
 
    def testGivenRestartedThenSameBehaviour(self):
        self.countDown.count = 1 * 3600 + 10 * 60 + 0
        self.notifier.start()
        time.sleep(0.1)
        self.notifier.stop()
        self.reset()
        self.countDown.count = 10
        self.notifier.start()
        time.sleep(0.1)
        self.notifier.stop()
        expected = range(11)
        expected.reverse()
        self.assertEquals(expected, self.history)
        
    def testGivenEnterDigitsThenDisplayCorrectTime(self):
        self.countDown.count = 0
        self.countDown.enter(3)
        self.assertEquals('0:00:03', self.countDown.getCountStr())
        self.countDown.enter(2)
        self.assertEquals('0:00:32', self.countDown.getCountStr())
        self.countDown.enter(3)
        self.assertEquals('0:03:23', self.countDown.getCountStr())
        self.countDown.enter(4)
        self.assertEquals('0:32:34', self.countDown.getCountStr())
        self.countDown.enter(5)
        self.assertEquals('3:23:45', self.countDown.getCountStr())
        self.countDown.enter(6)
        self.assertEquals('32:34:56', self.countDown.getCountStr())
        self.countDown.enter(2)
        self.assertEquals('0:00:02', self.countDown.getCountStr())
    
    def testGivenEnterDigitsAndDeleteThenDisplayCorrectTime(self):
        self.countDown.count = 0
        self.countDown.enter(3)
        self.countDown.enter(2)
        self.countDown.enter(3)
        self.countDown.enter(4)
        self.countDown.deleteLastEntered()
        self.assertEquals('0:03:23', self.countDown.getCountStr())
    
    def testGivenEnterDigitsAndDeleteMoreThenDisplay0(self):
        self.countDown.count = 0
        self.countDown.enter(3)
        self.countDown.deleteLastEntered()
        self.countDown.deleteLastEntered()
        self.assertEquals('0:00:00', self.countDown.getCountStr())
    
    def testGivenCountThenDisplayCorrectTime(self):
        self.countDown.count = 23*3600+45*60+24
        self.assertEquals('23:45:24', self.countDown.getCountStr())
        
    def reset(self):
        self.history = []
        self.historyStr = []
    
    def update(self):
        if self.countDown.count > 0 or self.history.count(0) == 0 :
            self.history.append(self.countDown.count)
            self.historyStr.append(self.countDown.getCountStr())

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
