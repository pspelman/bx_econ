# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from time import sleep, time

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader

from apt_logic import get_results_indices, process_raw_data
from forms import QuantityResponseForm
from methods import *
from django.http import JsonResponse


##
# Handle 404 Errors
# @param request WSGIRequest list with all HTTP Request
def error404(request):
    # 1. Load models for this view
    #from idgsupply.models import My404Method

    # 2. Generate Content for this view
    response_page = loader.get_template('404.html')
    context = {
        'message': 'Not available',
        }

    # 3. Return Template for this view + Data
    return HttpResponse(content=response_page.render(context), content_type='text/html; charset=utf-8', status=404)

# TODO: add ability to call price_levels file OR add ability for price levels to be specified via the researcher page

# price_levels = [0, 5, 10, 25, 50, 75, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500]
PRICES = [0, 25, 50, 75, 100, 200, 300, 400, 500, 1000]


def welcome_vew(request):
    # buffer = io.StringIO()
    # wr = csv.writer(buffer, quoting=csv.QUOTE_ALL)
    # wr.writerows(file_rows)
    # buffer.seek(0)
    # response = HttpResponse(buffer, content_type='text/csv')
    # response['Content-Disposition'] = 'attachment; filename=stockitems_misuper.csv'
    # return response

    sleep(0.05)
    ###123### print "reached welcome_view"
    return render(request, 'welcome.html', {"theTime": time()})


def instructions_view(request):
    ###123### print "reached instructions_view"
    if 'in_progress' not in request.session:
        ###123### print "needs to start new session...calling initiate_task_session(rq)"
        initiate_task_session(request.session, PRICES)
        start_timestamp = time()
        ###123### print "setting start_timestamp to {}".format(start_timestamp)
        request.session['start_timestamp'] = start_timestamp
    # reqeust.session['in_progress'] WILL be false, so this will display the directions page AS INTENDED

    if request.session['in_progress']:
        ###123### print "task is already in progress...return to next item"
        response_data = {}
        response_data['result'] = 'error'
        response_data['message'] = 'Some error message'
        context = {
            "error_message": "try the reset button"
        }
        return render(request, 'error_page.html', context)

        # return JsonResponse({"message": "there is a session in progress. Try the reset button."})
        # return redirect('task_view')
        # return HttpResponse("task is already in progress. Placeholder to return to next unanswered item: {}".format(get_next_unanswered_question(request.session)))

    ###123### print "not yet in progress...show the instructions!"
    context = {
        'task': get_task_instructions(),
    }
    request.session.modified = True
    return render(request, 'instructions.html', context)


def task_view(request):
    sleep(0.1)
    ###123### print "reached task_view"
    next_unanswered_question = get_next_unanswered_question(request.session)
    if next_unanswered_question == "DONE":
        ###123### print "Task is done...redirect to completion"
        sleep(0.1)
        return redirect('/completion')
    ###123### print "not done, getting context"
    # if it's not done, show the next question
    context = get_task_question_context(request)

    ###123### print "don't forget to redirect back to the task_view after processing the form"

    return render(request, 'task_question_form.html', context)

    # should probably use get_context or something to assign the context variables and question logic
    return HttpResponse("reached the end of task_view...not sure why you're seeing this")


""" this will return the variables to send to the template
    based on the next question that needs to be answered """


def get_task_question_context(request):
    ###123### print "reached get_task_question_context"
    next_unanswered_question = get_next_unanswered_question(request.session)
    ###123### print "next unanswered question: ", next_unanswered_question

    # get the price associated with the current item (string price)
    quantity_response_form = QuantityResponseForm(request.POST or None)
    ###123### print "quant form set"

    current_price_text = request.session['price_strings'][next_unanswered_question]
    ###123### print 'current price text:', current_price_text

    context = {
        'individual_price_level': current_price_text,
        'price_as_dollar': '$100',
        'quantity_response_form': quantity_response_form,
        'task': get_task_instructions(current_price_text),
    }

    return context


def begin_task(request):
    ###123### print "reached begin task...test to see if task was already started"
    if request.session['in_progress']:
        ###123### print " the task was already started, do the code to get the right context vars"
        return JsonResponse({"message": "Placeholder for RESUMING a task already started"})
        # return HttpResponse('placeholder for resuming the task')
        # context = get_task_question_context(request)

    #
    ###123### print "Task has not been started. Starting at the beginning!"
    request.session['in_progress'] = True
    request.session.modified = True
    ###123### print "redirecting to task view...it should then show questions"
    # return JsonResponse({"message": "Beginning new purchase task"})
    return redirect('/task_view')



def process_form_data(request):
    print "reached process_form_data"
    ###123### print "request contents: ", request
    #
    if request.method == 'POST':
        quantity_response_form = QuantityResponseForm(request.POST or None)
        # ###123### print "quant form set"
        if quantity_response_form.is_valid():
            print "quantity form was valid"
            response_quant = quantity_response_form.cleaned_data.get('quantity')
            next_unanswered_question = get_next_unanswered_question(request.session)

            ###123### print "Trial number upon submit:", next_unanswered_question
            response = 'placeholder for values from item {} | user submitted {}' \
                       ' need to save to session'.format(next_unanswered_question, response_quant)

            ###123### print "saving the response {} to the session for trial {}".format(response_quant, next_unanswered_question)
            request.session['response_key'][next_unanswered_question]['0'] = response_quant
            request.session.modified = True

            ###123### print "saved to session: ", request.session['response_key'][next_unanswered_question]['0']

            ###123### print "trying to redirect to task_view"
            return redirect('/task_view')

        else:
            quantity_response_form = QuantityResponseForm(request.POST)
            print "INVALID entry"
            context = get_task_question_context(request)

            ###123### print "don't forget to redirect back to the task_view after processing the form"

            # return render(request, 'task_question_form.html', {'quantity_response_form': quantity_response_form})
            return render(request, 'task_question_form.html', context)
    # return render(request, 'task_question_form.html', context)
    #     # FIXME: NEED TO ACCOUNT FOR INVALID FORM DATA
    #     print "NEVER GETS HERE"
    #     ###123### print "setting the next_unanswered question... ? NOT SURE IF I DO THIS HERE"
    #
    #     return HttpResponse(response)
    #
    #     # save in session
    #     prices_as_float = get_price_as_float(PRICES)
    #     request.session['response_set']['trial_number'].append(manual_trial_number)
    #     request.session['response_set']['item_price'].append(prices_as_float[manual_trial_number])
    #     request.session['response_set']['quantity'].append(response_quant)
    #     # request.session['response_set']['trial_number'].append(trial_number)
    #     # request.session['response_set']['item_price'].append(price_number)
    #     # request.session['response_set']['quantity'].append(response_quant)
    #     # ###123### print "response set", request.session['response_set']['trial_number']
    #     ###123### print "response set", request.session['response_set']
    #
    #     request.session.modified = True
    #
    #     # ###123### print "quantity received:", response_quant
    #
    #     # TODO: get the response from the user and save it in session with corresponding trial number
    #     ###123### print "trial number:", trial_number
    #     ###123### print "response:", response_quant
    #     request.session['manual_trial_number'] = request.session['manual_trial_number'] + 1
    #     ###123### print "new manual trial number:", request.session['manual_trial_number']
    #     # return redirect('/')
    #
    #     current_question = task_instructions['individual_price_level'].format(current_item_string)
    #     ###123### print "current question:", current_question
    #     task_instructions['individual_price_level'] = current_question
    # #     FIXME: add ELSE if the form data is NOT valid
    #
    #     return render(request, 'dashboard.html', context)
    # return redirect('/')


# TODO: add the logic to process the response (maybe in this method, maybe in a different method)
# COULD add the response to their DB and then continue





def task_complete_view(request):
    end_timestamp = time()
    request.session['end_timestamp'] = end_timestamp
    ###123### print "task complete_view reached...let's get some results. Setting end_timestamp: {}".format(end_timestamp)

    raw_task_results = process_raw_data(request.session)


    results_indices = get_results_indices(raw_task_results)

    # TODO: send dirty data to the database
    # TODO: determine the number of reversals in participant data
    # TODO: auto-clean one or two reversals
    # TODO: send clean data to the database

    request.session['raw_data'] = raw_task_results['raw_tuples']
    request.session['final_indices'] = results_indices
    request.session.modified = True

    # TODO: EMAIL the results

    # FIXME: Once the task is live, DISABLE the display of the user's results
    context = {
        'start_timestamp': request.session['start_timestamp'],
        'end_timestamp': request.session['end_timestamp'],
        'researcher_email': request.session['researcher_email'],
        'participant_id': request.session['participant_id'],
        'data': raw_task_results['raw_tuples'],
        'indices': results_indices,
    }
    return render(request, 'task_complete.html', context)


def logout_view(request):
    ###123### print "reached logout"
    request.session.flush()
    clear_session(request)
    request.session.modified = True
    return redirect('/')
    # return redirect('/task')


def clear_session(request):
    ###123### print "clearing the session data"
    request.session.flush()
    request.session['initiated'] = False
    return redirect('/task')

    # to delete keys but keep the user logged in
    # for key in request.session.keys():
    #     del request.session[key]


def manual_input(request):
    print "reached manual input"
    researcher_email = request.GET['researcher_email']
    participant_id = request.GET['participant_id']
    if researcher_email == "":
        researcher_email = 'research@philspelman.com'
    if participant_id == "":
        participant_id = 'none'

    print "researcher_email: {} | participant_id: {}".format(researcher_email, participant_id)
    return begin_task_with_url_params(request, researcher_email, participant_id)

def begin_task_with_url_params(request, researcher_email='research@philspelman.com', participant_id='none'):
    ###123### print "arrived at grab data path for grabbing data from URL string"
    ###123### print "got data: {}".format(researcher_email)
    ###123### print "participant id: {}".format(participant_id)
    print "reached begin task"

    # DONE: save participant_id in session
    # DONE: save researcher email in session
    request.session['participant_id'] = participant_id
    request.session['researcher_email'] = researcher_email
    request.session.modified = True

    return redirect("/instructions")
    # return JsonResponse({"message": "got some email: {} || participant_id: {}".format(researcher_email, participant_id)})


# in_progress redirects here
def render_question_page_view(request):
    ###123### print "reached render_question_page_view"
    # TODO: determine which question needs to be answered next
    next_unanswered_question = get_next_unanswered_question(request.session)

    # TODO: prepare the appropriate context variables for the item
    ###123### print "next_unanswered_question: ", next_unanswered_question

    if next_unanswered_question == "DONE":
        ###123### print "Task is done...redirect to completion"
        return HttpResponse("Placeholder for ALL DONE")
    else:
        return HttpResponse('this is a response')

    ###123### print "next unanswered question was NOT done...so getting the next context ready"

    return HttpResponse("Placeholder for NEXT question context")

