import StringIO

from django.http import JsonResponse

from methods import make_JSON


def send_results(request):
    ###123### print "trying to send results via email"
    # ###123### print "data: " + request.session
    ###123### print request.session['raw_data']
    ###123### print request.session['final_indices']

    participant_id = request.session['participant_id']
    researcher_email = request.session['researcher_email']

    # TODO: Add participant ID
    ###123### print "participant id: {}".format(participant_id)
    ###123### print "researcher email : {}".format(researcher_email)

    # TODO: get researcher email
    # send_mail(
    #     'Test results',
    #     'Here is the message.',
    #     FROM: 'purcahseTask@philspelman.com',
    #     TO: ['phil.spelman@gmail.com'],
    #     fail_silently=False,
    # )
    task_result_data = {"participant_id": participant_id, "researcher_email": researcher_email,
                        "raw_data": request.session['raw_data'], "final_indices": request.session['final_indices']}

    ###123### print "getting JSON"
    result = StringIO.StringIO(make_JSON(task_result_data))

    # todo: Make CSV file
    ###123### print result.read()
    # result.read()
    return JsonResponse({"message": "trying to send results via email", "raw_data": request.session['raw_data'],
                         "final_indices": request.session['final_indices']})