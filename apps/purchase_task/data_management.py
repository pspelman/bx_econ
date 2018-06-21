import StringIO
import csv

from django.http import JsonResponse, HttpResponse

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





def make_csv(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="apt_results_{}.csv"'.format(request.session['start_timestamp'])

    writer = csv.writer(response)
    writer.writerow(['participant_id',  "=\"" + request.session['participant_id'] + "\""])
    writer.writerow(['start_timestamp', request.session['start_timestamp']])
    writer.writerow(['end_timestamp', request.session['end_timestamp']])
    writer.writerow(['researcher_email', request.session['researcher_email']])
    writer.writerow(['Raw Data'])
    writer.writerow(['item', 'price', 'quantity', '$'])

    raw_data = request.session['raw_data']
    final_indices = request.session['final_indices']
    print "final indices: ", final_indices

    for trial in raw_data:
        writer.writerow([trial[0], trial[1], trial[2], trial[1]*trial[2]])

    writer.writerow(['Demand Indices'])
    writer.writerow([])
    writer.writerow(['Intensity', final_indices['intensity']])
    writer.writerow(['Omax', final_indices['omax']])
    writer.writerow(['Pmax', final_indices['pmax']])
    writer.writerow(['Breakpoint', final_indices['breakpoint']])
    writer.writerow([])
    writer.writerow(['Warnings:'])
    for warning in final_indices['data_warnings']:
        writer.writerow([warning[0], warning[1]])

    writer.writerow([])
    writer.writerow([])
    writer.writerow(['Note:','','Current Pmax value is the FIRST price associated with Omax (i.e., in the event of multiple Omax values, Pmax is the price associated with the first occurence of Omax)'])

    return response