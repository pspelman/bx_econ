# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect

from forms import *

def mock_form(request):
    context = {
        'id': '',
        'price_as_dollar': '$100'

    }
    return render(request,'dashboard.html', context)



# TODO: add ability to call price_levels file OR add ability for price levels to be specified via the researcher page
price_levels = [0,5,10,25,50,75,100,200,300,400,500,600,700,800,900,1000,1100,1200,1300,1400,1500]


def get_price_as_dollar():
    price_as_dollar = []
    for level in price_levels:
        price_level.append(float(level)/100)
        price_as_dollar.append("${:.2f}".format((float(level)/100)))




#TODO: define consumption data returned from form
# probably a dictionary of some type:
#
# consumption_data could be stored in session, or it could be temporary in the DB, in which case I need to dynamically create my model

# sdfs


#TODO: determine the number of reversals in participant data


#TODO: auto-clean one or two reversals


#TODO: calculate intensity (the consumption when the commodity is FREE ($0.00)
def get_intensity(consumption_data):


    return "Amount consumed when free"



#TODO: calculate Omax (the MAXIMUM spent across all prices
def get_omax(consumption_data):
    print "reached get_omax"
    omax = 0



    return omax


#TODO: calculate Pmax (the FIRST price where Omax was reached


#TODO: calculate Breakpoint (the FIRST price at which consumption becomes ZERO



price_levels_dictionary = {
    '0': '0.00',
    '1': '0.02',
    '2': '0.05',
}

def purchase_task(request):
    pass
