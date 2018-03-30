# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect

from forms import QuantityResponseForm, TripForm
from methods import *

from django import template

register = template.Library()

@register.filter(name='replace_linebr')
def replace_linebr(value):
    """
    Replaces all values of line break from the given string with a line space.
    example call in template:    {{ education_detail.education_details_institution_name|replace_linebr }}
    """
    return value.replace("<br />", ' ')



def question_validate(request):
    # method to get here will always be POST
    print "this is the question validate method"
    return redirect('/mock')
    user_form = request.POST or None


# TODO: add ability to call price_levels file OR add ability for price levels to be specified via the researcher page


def get_task_instructions():
    instruction_head = "Instructions"

    acute_instructions = ("Imagine that you could drink alcohol RIGHT NOW.\n\n"
                          "How many alcoholic drinks would you consume at the following prices?\n")

    state_based_instructions = "Imagine you're going to go to a bar with friends this Friday night. ... get the rest of those instructions"

    # put together the instructions
    scenario_instructions = acute_instructions
    available_amounts_header = "The available drinks are:"
    drink_amounts_list = ['standard size domestic beer (12 oz.)',
                            'wine (5 oz.',
                            'shots of hard liquor (1.5 oz.)',
                            'mixed drinks containing one shot of liquor',
                            ]
    assumption_instructions = "Please assume that you would consume every drink you request; that is, you cannot stockpile drinks for a later date or bring drinks home with you."
    how_to_respond_instructions = "Please use the number pad to enter numbers"

    instruction_dictionary = {
        'task_title': instruction_head,
        'instruction_head': instruction_head,
        'scenario_instructions': scenario_instructions,
        'drink_amounts_list': drink_amounts_list,
        'available_amounts_header': available_amounts_header,
        'post_instructions': assumption_instructions,
        'how_to_respond_instructions': how_to_respond_instructions,


        }

    return instruction_dictionary






# price_levels = [0, 5, 10, 25, 50, 75, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500]
PRICES = [0, 25, 50, 75, 100, 200, 300, 400, 500, 1000]


def task_form_view(request):
    print "reached form view"

    # to delete keys but keep the user logged in
    for key in request.session.keys():
        del request.session[key]

    # to start a new session


    if not 'initiated' in request.session:
        print "initaite was not in session...initiate session!"
        request.session.modified = True
    elif request.session['initiated'] == False:
        print "initaite was false...initiate session!"
        request.session.modified = True

    #     print "initiated was not in session...initiating new session"
    #     request.session['initiated'] = True
    #     price_strings_array = get_price_as_dollar_string(PRICES)
    #     print "original price array", price_strings_array
    #
    #     # TODO: put the reversal in a function, it should probably be defaulted to a lowest-to-highest presentation
    #     price_strings_array.reverse()
    #     print "Reversed price array", price_strings_array
    #
    #     request.session['price_levels'] = price_strings_array
    #
    #     current_item_string = price_strings_array.pop()
    #     print "current item initially set to: ", current_item_string
    #
    #     request.session['current_item'] = current_item_string
    #     # should probably reverse the prices and the POP from the back for each price level
    #
    #
    #
    #
    #
    # #
    # #
    # # price_numbers = get_price_as_float(PRICES)
    # # price_strings = get_price_as_dollar_string(PRICES)
    # #
    # # price_dictionary = get_price_dictionary(PRICES)
    # # print "dictionary: ", price_dictionary
    # #
    #
    # # TODO: when the session runs out of items, set it to false and the page will go to the results or something
    # if request.session['current_item_string']:
    #     print "there are more prices"

    #     request.session['next_item'] = 1
    #
    #
    # for price in price_dictionary:
    #     print price[0]

    # prices dictionary
    # question text (e.g., $5.00 / drink)
    # response from the user
    # current question number

    # TODO: start with the first question_dictionary item
    # TODO: get the response from the user and save it in session
    # TODO: move to the NEXT item in the dictionary

    task_instructions = get_task_instructions()

    quantity_response_form = QuantityResponseForm(request.POST or None)

    context = {
        'heading': "THIS IS THE FORM",
        'price_level': '1',
        'price_as_dollar': '$100',
        'quantity_response_form': quantity_response_form,
        'task': task_instructions,
        # 'TripForm': trip_form,
    }

    if quantity_response_form.is_valid():
        print "quantity form was valid"
        quant = quantity_response_form.cleaned_data.get('quantity')
        print "quantity recieved:", quant

        return redirect('/task')

     # TODO: add the logic to process the response (maybe in this method, maybe in a different method)
     # COULD add the response to their DB and then continue

    return render(request, 'dashboard.html', context)
    # return render(request, 'question.html', context)










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

def clear_session(request):
    print "clearing the session data"
    request.session.flush()
    request.session['initiated'] = False
    return redirect('/')