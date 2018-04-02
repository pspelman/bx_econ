# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect

from forms import QuantityResponseForm, TripForm
from methods import *

from django import template



# TODO: add ability to call price_levels file OR add ability for price levels to be specified via the researcher page


# price_levels = [0, 5, 10, 25, 50, 75, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500]
PRICES = [0, 25, 50, 75, 100, 200, 300, 400, 500, 1000]



def welcome_vew(request):
    print "reached welcome_view"
    return render(request, 'welcome.html')


def instructions_view(request):
    print "reached instructions_view"
    if 'in_progress' not in request.session:
        print "needs to start new session...calling initiate_task_session(rq)"
        initiate_task_session(request)
    #reqeust.session['in_progress'] WILL be false, so this will display the directions page AS INTENDED

    if request.session['in_progress']:
        print "task is already in progress...return to next item"
        return HttpResponse("task is already in progress. Placeholder to return to next unanswered item: {}".format(get_next_unanswered_question(request.session)))

    context = {
        'task': get_task_instructions(),
    }
    request.session.modified = True

    return render(request, 'instructions.html', context)


def initiate_task_session(request):
    print "reached initiate_task_session... checking if new session is needed"
    # if the session is empty, start a new task
    if 'initiated' not in request.session:
        request.session.flush()
        print "initiating NEW session"
        initiate_new_session_vars(request.session, PRICES)
        request.session['initiated'] = True
        request.session.modified = True
        return

    elif request.session['initiated'] == False:
        print "initiated was false, starting new session!"
        request.session['initiated'] = True
        initiate_new_session_vars(request.session, PRICES)
        request.session.modified = True
        return

    print "unexpected event: something in initiate_task_session went wrong"
    print "session task status:", request.session['task_status']



def task_view(request):
    #TODO: initiate new session / clear out old session, including set the question list

    print "attempting to set sesion..."
    initiate_task_session(request)
    print "session:", request.session

    next_unanswered_question = get_next_unanswered_question(request.session)

    print "trial_number: ", next_unanswered_question
    if next_unanswered_question == "DONE":
        print "Task is done...redirect to completion"
        return HttpResponse("Placeholder for ALL DONE")

    # should probably use get_context or something to assign the context variables and question logic
    return redirect(instructions_view)

""" this will return the variables to send to the template
    based on the next question that needs to be answered """
    
def get_task_question_context(request):
    print "next unanswered question: ", get_next_unanswered_question(request.session)

    
    # TODO: current item number (whether new or resuming)

    # TODO: get the price associated with the current item (string price)
    quantity_response_form = QuantityResponseForm(request.POST or None)
    print "quant form set"

    context = {
        'price_level': '1',
        'price_as_dollar': '$100',
        'quantity_response_form': quantity_response_form,
        'task': get_task_instructions(),
    }

    # FIXME: the page to render is the
    return "placeholder for the CONTEXT"
    pass


def begin_task(request):
    print "reached begin task...test to see if task was already started"
    if request.session['in_progress']:
        print " the task was already started, do the code to get the right context vars"
        context = get_task_question_context(request)

    print "beginning purchase task"
    request.session['in_progress'] = True
    request.session.modified = True
    return redirect(task_view)


def render_question_page_view(request):
    # TODO: determine which question needs to be answered next

    # TODO: prepare the appropriate context variables for the item

    return HttpRequest("this is a placeholder to render a question page")


def task_complete_view(request):
    print "task complete_view reached"
    return render(request, 'task_complete.html')


def task_form_view(request):
    print "reached form view"
    quantity_response_form = QuantityResponseForm(request.POST or None)
    print "quant form set"


    if 'initiated' not in request.session:
        request.session.flush()
        print "initaite was not in session...initiate session!"
        initiate_new_session_vars(request.session, PRICES)
        request.session['initiated'] = True
        request.session.modified = True

    elif request.session['initiated'] == False:
        print "initaite was false...initiate session!"
        request.session['initiated'] = True
        initiate_new_session_vars(request.session, PRICES)
        request.session.modified = True

    print "session task status:", request.session['task_status']

    # if i get here without a new session, that means I've started this and went through the directions

    # TODO: make the session info handler NOT inside this class, save a dictionary in session and use that to manage trials

    # TODO: when the session runs out of items, set it to false and the page will go to the results or something

    # FIXME: if request.session[next_trial] == 'instructions' then need to change show_questions in context to False

    task_instructions = get_task_instructions()

    next_trial = request.session['next_trial'][len(request.session['next_trial'])-1]
    print "session next trial before tests:", next_trial

    if next_trial == 'DONE':
        print "task finished, redirect to completion"
        # TODO: store response data
        return redirect('/completion')


    if next_trial == 'instructions':
        print "the instructions are next up"
        request.session['manual_trial_number'] = 0
        show_questions = False
        # that should make the next item be a trial number
        test_item = request.session['next_trial'].pop()
        print "next_trial thing in session", test_item

        context = {
            'heading': "THIS IS THE FORM",
            'task': task_instructions,
            'show_questions': False,
        }
        request.session.modified = True
        return render(request, 'dashboard.html', context)


    if request.session['in_progress'] == True:
        show_questions = True

        next_trial = request.session['next_trial'].pop()
        current_item_string = request.session['price_strings'].pop()
        trial_number = request.session['trial_numbers'].pop()
        price_number = request.session['price_numbers'].pop()

        print "next trial popped was:", next_trial
        print "current item string:", current_item_string
        print "current trial number", trial_number
        request.session.modified = True

        context = {
            'heading': "THIS IS THE FORM",
            'price_level': '1',
            'price_as_dollar': '$100',
            'quantity_response_form': quantity_response_form,
            'task': task_instructions,
            'show_questions': show_questions,
            }

    elif request.session['in_progress'] == False:
        print "something went wrong. Starting over. Do not refresh the page"

    if quantity_response_form.is_valid():

        print "quantity form was valid"
        response_quant = quantity_response_form.cleaned_data.get('quantity')
        manual_trial_number = request.session['manual_trial_number']
        print "Trial number upon submit:", manual_trial_number
        # save in session
        prices_as_float = get_price_as_float(PRICES)
        request.session['response_set']['trial_number'].append(manual_trial_number)
        request.session['response_set']['item_price'].append(prices_as_float[manual_trial_number])
        request.session['response_set']['quantity'].append(response_quant)
        # request.session['response_set']['trial_number'].append(trial_number)
        # request.session['response_set']['item_price'].append(price_number)
        # request.session['response_set']['quantity'].append(response_quant)
        # print "response set", request.session['response_set']['trial_number']
        print "response set", request.session['response_set']

        request.session.modified = True

        # print "quantity received:", response_quant

        # TODO: get the response from the user and save it in session with corresponding trial number
        print "trial number:", trial_number
        print "response:", response_quant
        request.session['manual_trial_number'] = request.session['manual_trial_number'] + 1
        print "new manual trial number:", request.session['manual_trial_number']
        # return redirect('/')

        current_question = task_instructions['individual_price_level'].format(current_item_string)
        print "current question:", current_question
        task_instructions['individual_price_level'] = current_question

    return render(request, 'dashboard.html', context)
    return redirect('/')

# TODO: add the logic to process the response (maybe in this method, maybe in a different method)
# COULD add the response to their DB and then continue




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



def purchase_task(request):
    pass


def logout_view(request):
    print "reached logout"
    request.session.flush()
    request.session.modified = True
    return redirect('/task')


def clear_session(request):
    print "clearing the session data"
    request.session.flush()
    request.session['initiated'] = False
    return redirect('/task')

    # to delete keys but keep the user logged in
    # for key in request.session.keys():
    #     del request.session[key]


