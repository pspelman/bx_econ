from django import template

register = template.Library()
@register.filter(name='replace_linebr')
def replace_linebr(value):
    """
    Replaces all values of line break from the given string with a line space.
    example call in template:    {{ education_detail.education_details_institution_name|replace_linebr }}
    """
    return value.replace("<br />", ' ')


'''This method will return an array of price levels as strings
    formatted to look like dollars with two decimals (e.g., $2.00 '''

def get_price_as_dollar_string(price_levels):
    price_as_dollar = []
    for level in price_levels:
        price_as_dollar.append("${:.2f}".format((float(level) / 100)))
    return price_as_dollar
# return an array of prices formatted as strings

def get_price_as_float(price_levels):
    price_level = []
    for i in range(len(price_levels)):
        price_level.append(float(price_levels[i]) / 100)
    # for level in price_levels:
    #     price_level.append(float(level) / 100)
    return price_level
# return an array of prices formatted as strings

def get_price_dictionary(PRICES):
    price_strings = get_price_as_dollar_string(PRICES)
    prices_as_float = get_price_as_float(PRICES)
    price_dictionary = {}
    for i in range(len(price_strings)):
        price_dictionary["{}".format(i)] = PRICES[i]
    return price_dictionary


def get_trial_numbers(num_trials):
    trials = []
    for i in range(len(num_trials)):
        trials.append(i)
        # print "trials:", trials
    return trials


def create_task_response_key(num_trials):
    print "creating response key based on number of items to be presented"
    response_key = []
    for i in range(len(num_trials)):
        response_key.append({
            i:'',
        })
    return response_key


def get_next_unanswered_question(session):

    # todo: does current 'next_unanswered_question' have an answer?
    # check the response key against the current next_unanswered question

    # if there is NOW a response, then that question is answered, assign the next_unanswered question to the next item
    print "next unanswered q: ", session['next_unanswered_question']
    task_length = len(session['response_key'])
    answer = '0'

    # if there IS NO answer
    if session['response_key'][session['next_unanswered_question']][answer] == '':
        print "question {} has not yet been answered! No changes made".format(session['next_unanswered_question'])
        return session['next_unanswered_question']

    # if there IS an answer
    if session['response_key'][session['next_unanswered_question']][answer] != '':
        if session['next_unanswered_question'] == task_length:
            print "the last question has been answered. Task is complete"
            session['next_unanswered_question'] = "DONE"
            return "DONE"
        else:
            print "question answered, getting next question"
            session['next_unanswered_question'] = session['next_unanswered_question'] + 1

    return "THE NEXT UNANSWERED QUESTION GOES HERE"



def initiate_new_session_vars(session, PRICES):
    session['initiated'] = True
    session['user_id'] = "na"
    session['next_unanswered_question'] = 0
    session['current_question_number'] = []

    session['in_progress'] = False

    session['response_set'] = {
        'trial_number': [],
        'item_price': [],
        'quantity': [],
    }

    # TODO: put the reversal in a function, it should probably be defaulted to a lowest_num-to-highest presentation
    price_numbers = get_price_as_float(PRICES)
    price_strings = get_price_as_dollar_string(PRICES)
    trial_numbers = get_trial_numbers(PRICES)
    response_key = create_task_response_key(PRICES)

    # session['response_key'] = [{0:'answer'},{1:'answer'}] #need to pre-populate the keys

    session['response_key'] = []


    price_numbers.reverse()
    price_strings.reverse()
    trial_numbers.reverse()

    session['response_key'] = response_key
    session['price_numbers'] = price_numbers
    session['price_strings'] = price_strings
    session['trial_numbers'] = trial_numbers

    print price_numbers
    print price_strings
    print trial_numbers
    # instructions flag
    next_trial = []
    next_trial.append('instructions')
    next_trial.extend(trial_numbers)
    next_trial.append('DONE')
    next_trial.reverse()

    print "next_trial array is constructed:", next_trial

    session['next_trial'] = next_trial

    session['task_status'] = {
        'price_numbers': price_numbers,
        'price_strings': price_strings,
        'trial_numbers': trial_numbers,
        'next_trial': next_trial,
    }


    session.modified = True
    print "session initiated...returning to task_form"
    return


def get_task_instructions():
    instruction_head = "Instructions"

    acute_instructions = ("Imagine that you could drink alcohol RIGHT NOW.\n\n"
                          "Your task is to enter the number of alcoholic drinks you would consume at various prices\n")

    state_based_instructions = "Imagine you're going to go to a bar with friends this Friday night. ... get the rest of those instructions"

    # put together the instructions
    scenario_instructions = acute_instructions
    available_amounts_header = "The available drinks are:"
    drink_amounts_list = ['standard size domestic beer (12 oz.)',
                            'wine (5 oz.)',
                            'shots of hard liquor (1.5 oz.)',
                            'mixed drinks containing one shot of liquor',
                            ]
    assumption_instructions = "Please assume that you would consume every drink you request. \nYou cannot stockpile drinks for a later date or bring drinks home with you."
    how_to_respond_instructions = "Please use the number pad to enter numbers"
    individual_price_level_prompt = "How many drinks would you have right now if they were"

    task_dictionary = {
        'task_title': instruction_head,
        'instruction_head': instruction_head,
        'scenario_instructions': scenario_instructions,
        'drink_amounts_list': drink_amounts_list,
        'available_amounts_header': available_amounts_header,
        'post_instructions': assumption_instructions,
        'how_to_respond_instructions': how_to_respond_instructions,
        'individual_price_level_prompt': individual_price_level_prompt,
        'individual_price_level':'{} / drink',

        }

    return task_dictionary


