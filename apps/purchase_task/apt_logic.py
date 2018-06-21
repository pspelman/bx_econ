import csv

from django.http import HttpResponse


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

    for trial in raw_data:
        writer.writerow([trial[0], trial[1], trial[2], trial[1]*trial[2]])

    writer.writerow(['Demand Indices'])
    writer.writerow([])
    writer.writerow(['Intensity', final_indices['intensity']])
    writer.writerow(['Omax', final_indices['omax']])
    writer.writerow(['Pmax', final_indices['pmax']])
    writer.writerow(['Breakpoint', final_indices['breakpoint']])

    writer.writerow([])
    writer.writerow(['Note:','','Current Pmax value is the FIRST price associated with Omax (i.e., in the event of multiple Omax values, Pmax is the price associated with the first occurence of Omax)'])

    return response