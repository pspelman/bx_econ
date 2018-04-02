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
        initiate_task_session(request.session, PRICES)
    #reqeust.session['in_progress'] WILL be false, so this will display the directions page AS INTENDED

    if request.session['in_progress']:
        print "task is already in progress...return to next item"
        return redirect('task_view')
        # return HttpResponse("task is already in progress. Placeholder to return to next unanswered item: {}".format(get_next_unanswered_question(request.session)))

    print "not yet in progress...show the instructions!"
    context = {
        'task': get_task_instructions(),
    }
    request.session.modified = True
    return render(request, 'instructions.html', context)



def task_view(request):
    print "reached task_view"
    next_unanswered_question = get_next_unanswered_question(request.session)
    if next_unanswered_question == "DONE":
        print "Task is done...redirect to completion"
        return redirect('/task/completion')

    print "not done, getting context"
    # if it's not done, show the next question
    context = get_task_question_context(request.session)

    print "don't forget to redirect back to the task_view after processing the form"

    return render(request, 'task_question_form.html', context)

    # should probably use get_context or something to assign the context variables and question logic

    return HttpResponse("reached the end of task_view...not sure why you're seeing this")


""" this will return the variables to send to the template
    based on the next question that needs to be answered """
def get_task_question_context(session):
    print "reached get_task_question_context"
    next_unanswered_question = get_next_unanswered_question(session)
    print "next unanswered question: ", next_unanswered_question

    # TODO: get the price associated with the current item (string price)
    quantity_response_form = QuantityResponseForm(None)
    print "quant form set"

    current_price_text = session['price_strings'][next_unanswered_question]
    print 'current price text:', current_price_text


    context = {
        'individual_price_level': current_price_text,
        'price_as_dollar': '$100',
        'quantity_response_form': quantity_response_form,
        'task': get_task_instructions(current_price_text),
    }

    return context

def begin_task(request):
    print "reached begin task...test to see if task was already started"
    if request.session['in_progress']:
        print " the task was already started, do the code to get the right context vars"
        return HttpResponse('placeholder for resuming the task')
        # context = get_task_question_context(request)


    print "Task has not been started. Starting at the beginning!"
    request.session['in_progress'] = True
    request.session.modified = True
    print "redirecting to task view...it should then show questions"
    return redirect('task_view')

# in_progress redirects here
def render_question_page_view(request):
    print "reached render_question_page_view"
    # TODO: determine which question needs to be answered next
    next_unanswered_question = get_next_unanswered_question(request.session)

    # TODO: prepare the appropriate context variables for the item
    print "next_unanswered_question: ", next_unanswered_question

    if next_unanswered_question == "DONE":
        print "Task is done...redirect to completion"
        return HttpResponse("Placeholder for ALL DONE")
    else:
        return HttpResponse('this is a response')



    print "next unanswered question was NOT done...so getting the next context ready"

    return HttpResponse("Placeholder for NEXT question context")


def process_form_data(request):
    print "reached process_form_data"
    print "request contents: ", request
    quantity_response_form = QuantityResponseForm(request.POST or None)
    print "quant form set"
    if quantity_response_form.is_valid():

        print "quantity form was valid"
        response_quant = quantity_response_form.cleaned_data.get('quantity')
        next_unanswered_question = get_next_unanswered_question(request.session)

        print "Trial number upon submit:", next_unanswered_question
        response = 'placeholder for values from item {} | user submitted {}' \
                   ' need to save to session'.format(next_unanswered_question, response_quant)

        print "saving the response {} to the session for trial {}".format(response_quant, next_unanswered_question)
        request.session['response_key'][next_unanswered_question]['0'] = response_quant
        request.session.modified = True

        print "saved to session: ", request.session['response_key'][next_unanswered_question]['0']

        print "trying to redirect to task_view"
        return redirect('task_view')


        print "setting the next_unanswered question... ? NOT SURE IF I DO THIS HERE"

        return HttpResponse(response)

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


def process_raw_data(session):
    print "reached process_raw_data"

    response_key = session['response_key']
    print "response_key: ", response_key
    raw_data_dict = []
    raw_task_tuples = []
    raw_price_and_consumption_only = []


    price_list = session['price_numbers']
    print "price_list: ", price_list


    for i in range(len(response_key)):
        raw_price_and_consumption_only.append(
            (price_list[i], response_key[i]['0'])
        )

        raw_task_tuples.append(
            (i, price_list[i], response_key[i]['0'])
        )

        raw_data_dict.append(
            {
                price_list[i]: response_key[i]['0']
            }
        )



    print "raw_task_tuples processed... ->", raw_task_tuples
    print "raw_data_dict processed... -> ", raw_data_dict
    raw_task_results = {
        'raw_tuples': raw_task_tuples,
        'raw_data_dict': raw_data_dict,
        'raw_price_and_consumption_only': raw_price_and_consumption_only,
    }

    return raw_task_results


def task_complete_view(request):
    print "task complete_view reached...let's get some results!"

    raw_task_results = process_raw_data(request.session)
    raw_price_and_consumption_only = raw_task_results['raw_price_and_consumption_only']
    print "raw price and consumption: ", raw_price_and_consumption_only

    demand_indices = get_demand_indices(raw_price_and_consumption_only)
    omax = "${:.2f}".format((float(demand_indices['omax'])))
    pmax_results = demand_indices['pmax']

    pmax = "${:.2f}".format((float(pmax_results[len(pmax_results)-1][0])))

    breakpoint = "${:.2f}".format((float(demand_indices['breakpoint'])))



    print "omax: {}\npmax: {}".format(omax, pmax)
    print "breakpoint: ", demand_indices['breakpoint']

    results_indices = {
        'intensity': demand_indices['intensity'],
        'omax':omax,
        'pmax': pmax,
        'breakpoint': breakpoint,
    }

    # TODO: send dirty data to the database
    # TODO: determine the number of reversals in participant data
    # TODO: auto-clean one or two reversals
    # TODO: send clean data to the database

    context = {
        'data': raw_task_results['raw_tuples'],
        'indices': results_indices,


    }
    return render(request, 'task_complete.html', context)



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


def get_demand_indices(consumption_data):
    # consumption data will be JUST the price and consumption, not the trial (price, quant)
    print "reached get_omax"
    intensity = consumption_data[0][1]
    print "intensity: ", intensity
    omax = 0
    pmax = []
    breakpoint = 0

    for trial in consumption_data:
        print trial[0] * trial[1]
        # NOTE: change the logic below to >= for the possibility of multiple pmax values
        if trial[0] * trial[1] > omax:
            omax = trial[0] * trial[1]
            pmax.append([trial[0], omax])
            print "new omax:{} at price: {} ".format(omax, trial[0])

    if consumption_data[0][1]>0:
        #if something was consumed at this price, but NOTHING at the next price, the next price is the breakpoint
        for i in range(1,len(consumption_data)):
            print "consumption {} = {} | and consumption {} = {}".format(consumption_data[i],consumption_data[i][1], consumption_data[i-1], consumption_data[i-1][1])
            if consumption_data[i][1] == 0:
                if consumption_data[i-1][1] > 0:
                    print "breakpoint reached at price {}".format(consumption_data[i][0])
                    breakpoint = consumption_data[i][0]
        # if breakpoint == 0:
        #     breakpoint = "no breakpoint"

    return {'intensity': intensity, 'omax': omax, 'pmax': pmax, 'breakpoint': breakpoint}


