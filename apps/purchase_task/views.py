# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect

from forms import QuantityResponseForm, TripForm


def question_validate(request):
    # method to get here will always be POST
    print "this is the question validate method"
    return redirect('/mock')
    user_form = request.POST or None




# TODO: Change the name of "mock_form" to task_form_view
def mock_form(request):
    print "reached mock form"
    quantity_response_form = QuantityResponseForm(request.POST or None)

    context = {
        'heading':"THIS IS THE FORM",
        'price_level': '1',
        'price_as_dollar': '$100',
        'quantity_response_form': quantity_response_form,
        # 'TripForm': trip_form,
    }
    if request.method=="POST":
        print "checking if the form is valid"
    if quantity_response_form.is_valid():
        quant = quantity_response_form.cleaned_data.get('quantity')

        print "quantity recieved:", quant
        return redirect('/task')
    #
    #     # TODO: add the logic to process the response (maybe in this method, maybe in a different method)
    #     # COULD add the response to their DB and then continue

    return render(request, 'dashboard.html', context)
    # return render(request, 'question.html', context)









# TODO: add ability to call price_levels file OR add ability for price levels to be specified via the researcher page
price_levels = [0, 5, 10, 25, 50, 75, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500]


def get_price_as_dollar():
    price_as_dollar = []
    for level in price_levels:
        price_level.append(float(level) / 100)
        price_as_dollar.append("${:.2f}".format((float(level) / 100)))


# TODO: define consumption data returned from form
# probably a dictionary of some type:
#
# consumption_data could be stored in session, or it could be temporary in the DB, in which case I need to dynamically create my model

# sdfs


# TODO: determine the number of reversals in participant data


# TODO: auto-clean one or two reversals


# TODO: calculate intensity (the consumption when the commodity is FREE ($0.00)
def get_intensity(consumption_data):
    return "Amount consumed when free"


# TODO: calculate Omax (the MAXIMUM spent across all prices
def get_omax(consumption_data):
    print "reached get_omax"
    omax = 0

    return omax


# TODO: calculate Pmax (the FIRST price where Omax was reached


# TODO: calculate Breakpoint (the FIRST price at which consumption becomes ZERO


price_levels_dictionary = {
    '0': '0.00',
    '1': '0.02',
    '2': '0.05',
}


def purchase_task(request):
    pass
