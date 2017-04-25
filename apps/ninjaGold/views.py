from django.shortcuts import render, redirect
import random, datetime
from django.utils import formats

def index(request):
    if 'total_gold' not in request.session:
        request.session['total_gold'] = 0
        request.session['activities'] = []

    return render(request, 'ninjaGold/index.html')

def process_money(request):
    if request.method == 'POST':
        print request.POST['location']
        now = datetime.datetime.now()
        location = request.POST['location']

        locations = {
            'farm': random.randint(10, 20),
            'house': random.randint(2, 5),
            'cave': random.randint(5, 10),
            'casino': random.randint(-50, 50),
        }

        if location in locations:
            gold = locations[location]
            request.session['total_gold'] += gold

        formatted_datetime = formats.date_format(now, "SHORT_DATETIME_FORMAT")

        if gold < 0:
            color = 'lost'
            activity = 'Sorry, you lost {} gold from the {} ! {}'.format(abs(gold),
            location.upper(), formatted_datetime)
        else:
            color = 'gain'
            activity = 'You went to the {} and gains {} gold! {}'.format(location.upper(), gold, formatted_datetime)

        activity = {'class': color, 'activity': activity}

        request.session['activities'].append(activity)
        request.session.modified = True

    return redirect('ninjagold:index')

def delete(request):
    request.session.clear()
    return redirect('ninjagold:index')
