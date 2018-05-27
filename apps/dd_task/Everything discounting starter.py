#!/usr/bin/env python

##
## Micky Koffarnus made this (Jan 2014)
##

import os
import sys
from subprocess import call
from random import shuffle

scripts = [1, 2, 3] # make this a list of numbers from 1 to the number of tasks you want to run
programloc = '' #You can have this starter and the program stored in different places put the directory of the program in the quotation marks here
shuffle(scripts) # if you want the scripts to NOT be randomized, put a # at the beginning of this line before shuffle(scripts)

sid = raw_input('Subject ID: ')
exp = raw_input('Session: ')

for i,arr in enumerate(scripts):

    # START of a task instance. Copy from this line through the END line and paste below for another task instance
    if arr==1: # "arr" should be the number of the task in this file. This has nothing to do with the order in which this task will run, that is random.
        probability = "0"   # Put a "0" for delay discounting and a "1" for probability discounting
        losses = "0"    # Put a "0" for gains and a "1" for losses
        past = "0"  # Put a "0" for future and a "1" for past. This should be "0" for probability discounting.
        explicit0 = "0"     # Put a "0" for implicit zero and a "1" for explicit zero
        commodityD = "$"    # Delayed or probabilistic commodity with unit (e.g., "g of cocaine"). Just put $ for money.
        commodityI = "$"    # Immediate or certain commodity with unit (e.g., "g of cocaine"). Just put $ for money.
        amountD = "1000"    # Delayed or probabilistic amount in quotation marks
        amountI = "1000"    # Equivalence value for the immediate/certain commodity. For single-commodity discounting, this should be the same amount as the delayed amount.
        call(['python', programloc + 'AdjAmt discounting everything.py', sid, exp, probability, losses, past, explicit0, commodityD, commodityI, amountD, amountI, os.path.dirname(sys.argv[0]), 'n']) # Don't edit this.
    # END of this task instance. Copy through here to make more task instances, or delete through here to remove this task instance.

    # START of a task instance. Copy from this line through the END line and paste below for another task instance
    if arr==2: # "arr" should be the number of the task in this file. This has nothing to do with the order in which this task will run, that is random.
        probability = "0" # Put a "0" for delay discounting and a "1" for probability discounting
        losses = "0" # Put a "0" for gains and a "1" for losses
        past = "0" # Put a "0" for future and a "1" for past. This should be "0" for probability discounting.
        explicit0 = "0" # Put a "0" for implicit zero and a "1" for explicit zero
        commodityD = "$" # Delayed or probabilistic commodity with unit (e.g., "g of cocaine"). Just put $ for money.
        commodityI = "$" # Immediate or certain commodity with unit (e.g., "g of cocaine"). Just put $ for money.
        amountD = "1000" # Delayed or probabilistic amount in quotation marks
        amountI = "1000" # Equivalence value for the immediate/certain commodity. For single-commodity discounting, this should be the same amount as the delayed amount.
        call(['python', programloc + 'AdjAmt discounting everything.py', sid, exp, probability, losses, past, explicit0, commodityD, commodityI, amountD, amountI, os.path.dirname(sys.argv[0]), 'n']) # Don't edit this.
    # END of this task instance. Copy through here to make more task instances, or delete through here to remove this task instance.

    # START of a task instance. Copy from this line through the END line and paste below for another task instance
    if arr==3: # "arr" should be the number of the task in this file. This has nothing to do with the order in which this task will run, that is random.
        probability = "0" # Put a "0" for delay discounting and a "1" for probability discounting
        losses = "0" # Put a "0" for gains and a "1" for losses
        past = "0" # Put a "0" for future and a "1" for past. This should be "0" for probability discounting.
        explicit0 = "0" # Put a "0" for implicit zero and a "1" for explicit zero
        commodityD = "$" # Delayed or probabilistic commodity with unit (e.g., "g of cocaine"). Just put $ for money.
        commodityI = "$" # Immediate or certain commodity with unit (e.g., "g of cocaine"). Just put $ for money.
        amountD = "1000" # Delayed or probabilistic amount in quotation marks
        amountI = "1000" # Equivalence value for the immediate/certain commodity. For single-commodity discounting, this should be the same amount as the delayed amount.
        call(['python', programloc + 'AdjAmt discounting everything.py', sid, exp, probability, losses, past, explicit0, commodityD, commodityI, amountD, amountI, os.path.dirname(sys.argv[0]), 'n']) # Don't edit this.
    # END of this task instance. Copy through here to make more task instances, or delete through here to remove this task instance.
