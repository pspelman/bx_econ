import datetime

from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from models import *

User = get_user_model()



class TripForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = (
            'destination',
            'description',
            'start_date',
            'end_date',
        )

        this_year = datetime.datetime.now().year
        years_out = this_year + 10
        widgets = {
            'start_date': forms.SelectDateWidget(years=range(this_year, years_out)),
            'end_date': forms.SelectDateWidget(years=range(this_year, years_out)),
        }

    # def clean_start_date(self, *args, **kwargs):
    #     start_date = self.cleaned_data.get('start_date')
    #     if start_date <= datetime.date.today():
    #         raise forms.ValidationError("Only future trips may be added at this time")
    #     return start_date

    def clean_end_date(self, *args, **kwargs):
        end_date = self.cleaned_data.get('end_date')
        start_date = self.cleaned_data.get('start_date')
        print "end date:", end_date
        print "start date: ", start_date
        if start_date <= datetime.date.today():
            raise forms.ValidationError("Only future trips may be added at this time")
        if end_date == start_date:
            raise forms.ValidationError("Your trip must be more than one day")
        if end_date < start_date:
            raise forms.ValidationError("End date must be after start date")
        return end_date


class QuantityResponseForm(forms.ModelForm):
    quantity = forms.IntegerField(label='Drinks')
    class Meta:
        model = QuantityResponseModel
        fields = ['quantity']

    def clean_quantity(self, *args, **kwargs):
        quantity = self.cleaned_data.get('quantity')

        if quantity < 0:
            # raise forms.ValidationError("You may not enter negative numbers")
            raise forms.ValidationError("You may not enter negative numbers")
        if quantity > 100:
            raise forms.ValidationError("100-drink limit. Please enter fewer drinks.")
            # raise forms.ValidationError("100-drink limit. Please enter fewer drinks.")
        return quantity

    def __init__(self, *args, **kwargs):
        super(QuantityResponseForm, self).__init__(*args, **kwargs)

        self.fields['quantity'].widget.attrs= {'autofocus':'autofocus', 'size':'3'}
        # self.fields['quantity'].widget.attrs['autofocus'] = u'autofocus'


