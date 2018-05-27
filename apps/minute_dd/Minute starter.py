#!/usr/bin/env python

##
## Micky Koffarnus made this (Jan 2014)
##

import os
from subprocess import call
from random import shuffle

scripts = [1, 2, 3, 4] # make this a list of numbers from 1 to the number of tasks you want to run
shuffle(scripts)

sid = raw_input('Subject ID: ')
exp = raw_input('Session: ')

for i,arr in enumerate(scripts):

    # START of a task instance. Copy from this line through the END line and paste below for another task instance
    if arr==1: # "arr" should be the number of the task in this file. This has nothing to do with the order in which this task will run, that is random.
        commodity = "$" # Commodity with unit in quotation marks (e.g., "g of cocaine"). Just put "$" for money
        amount = "1000" # Delayed or probabilistic amount in quotation marks
        probability = "0" # Put a "0" for delay discounting and a "1" for probability discounting
        losses = "0" # Put a "0" for gains and a "1" for losses
        past = "0" # Put a "0" for future and a "1" for past. This should be "0" for probability discounting.
        explicit0 = "0" # Put a "0" for implicit zero and a "1" for explicit zero
        social = "0" # Put a "0" for Individual (non-social) discounting, a "1" for Me-Me, a "2" for Me-We, a "3" for We-Me, and a "4" for We-We
        call(['python', 'Minute discounting everything.py', sid, exp, commodity, amount, probability, losses, past, explicit0, social]) # Don't edit this.
    # END of this task instance. Copy through here to make more task instances, or delete through here to remove this task instance.
  
    # START of a task instance. Copy from this line through the END line and paste below for another task instance
    if arr==2: # "arr" should be the number of the task in this file. This has nothing to do with the order in which this task will run, that is random.
        commodity = "$" # Commodity with unit in quotation marks (e.g., "g of cocaine"). Just put "$" for money
        amount = "1000" # Delayed or probabilistic amount in quotation marks
        probability = "0" # Put a "0" for delay discounting and a "1" for probability discounting
        losses = "0" # Put a "0" for gains and a "1" for losses
        past = "0" # Put a "0" for future and a "1" for past. This should be "0" for probability discounting.
        explicit0 = "1" # Put a "0" for implicit zero and a "1" for explicit zero
        social = "0" # Put a "0" for Individual (non-social) discounting, a "1" for Me-Me, a "2" for Me-We, a "3" for We-Me, and a "4" for We-We
        call(['python', 'Minute discounting everything.py', sid, exp, commodity, amount, probability, losses, past, explicit0, social]) # Don't edit this.
    # END of this task instance. Copy through here to make more task instances, or delete through here to remove this task instance.
 
    # START of a task instance. Copy from this line through the END line and paste below for another task instance
    if arr==3: # "arr" should be the number of the task in this file. This has nothing to do with the order in which this task will run, that is random.
        commodity = "$" # Commodity with unit in quotation marks (e.g., "g of cocaine"). Just put "$" for money
        amount = "1000" # Delayed or probabilistic amount in quotation marks
        probability = "0" # Put a "0" for delay discounting and a "1" for probability discounting
        losses = "0" # Put a "0" for gains and a "1" for losses
        past = "1" # Put a "0" for future and a "1" for past. This should be "0" for probability discounting.
        explicit0 = "0" # Put a "0" for implicit zero and a "1" for explicit zero
        social = "0" # Put a "0" for Individual (non-social) discounting, a "1" for Me-Me, a "2" for Me-We, a "3" for We-Me, and a "4" for We-We
        call(['python', 'Minute discounting everything.py', sid, exp, commodity, amount, probability, losses, past, explicit0, social]) # Don't edit this.
    # END of this task instance. Copy through here to make more task instances, or delete through here to remove this task instance.
 
    # START of a task instance. Copy from this line through the END line and paste below for another task instance
    if arr==4: # "arr" should be the number of the task in this file. This has nothing to do with the order in which this task will run, that is random.
        commodity = "$" # Commodity with unit in quotation marks (e.g., "g of cocaine"). Just put "$" for money
        amount = "1000" # Delayed or probabilistic amount in quotation marks
        probability = "0" # Put a "0" for delay discounting and a "1" for probability discounting
        losses = "0" # Put a "0" for gains and a "1" for losses
        past = "1" # Put a "0" for future and a "1" for past. This should be "0" for probability discounting.
        explicit0 = "1" # Put a "0" for implicit zero and a "1" for explicit zero
        social = "0" # Put a "0" for Individual (non-social) discounting, a "1" for Me-Me, a "2" for Me-We, a "3" for We-Me, and a "4" for We-We
        call(['python', 'Minute discounting everything.py', sid, exp, commodity, amount, probability, losses, past, explicit0, social]) # Don't edit this.
    # END of this task instance. Copy through here to make more task instances, or delete through here to remove this task instance.

