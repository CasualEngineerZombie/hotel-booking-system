from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from .models import Booking, Room

class BookingUpdateForm(forms.ModelForm):
    check_in = forms.DateField(
        widget=forms.DateInput(attrs={
            "type": "date", 
            "class": "mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md text-sm shadow-sm placeholder-gray-400 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
        }),
    )
    check_out = forms.DateField(
        widget=forms.DateInput(attrs={
            "type": "date", 
            "class": "mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md text-sm shadow-sm placeholder-gray-400 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
        }),
    )
    total_guest = forms.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        widget=forms.NumberInput(attrs={
            "min": 1, 
            "max": 10, 
            "class": "mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md text-sm shadow-sm placeholder-gray-400 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
        }),
    )
    room = forms.ModelChoiceField(
        queryset=Room.objects.filter(is_available=True),
        empty_label="Select Room",
        widget=forms.Select(attrs={
            "class": "mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md text-sm shadow-sm placeholder-gray-400 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
        }),
    )

    class Meta:
        model = Booking
        fields = ["guest_name", "guest_email", "room", "check_in", "check_out", "total_guest"]
        widgets = {
            "guest_name": forms.TextInput(attrs={
                "class": "mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md text-sm shadow-sm placeholder-gray-400 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500", 
                "placeholder": "Enter guest name"
            }),
            "guest_email": forms.EmailInput(attrs={
                "class": "mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md text-sm shadow-sm placeholder-gray-400 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500", 
                "placeholder": "Enter email address"
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        check_in = cleaned_data.get("check_in")
        check_out = cleaned_data.get("check_out")

        if check_in and check_out and check_in >= check_out:
            raise forms.ValidationError("Check-out date must be after the check-in date.")

        return cleaned_data



class BookingCreateForm(forms.ModelForm):
    check_in = forms.DateField(
        widget=forms.DateInput(attrs={
            "type": "date",
            "class": "mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md text-sm shadow-sm placeholder-gray-400 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
        })
    )
    check_out = forms.DateField(
        widget=forms.DateInput(attrs={
            "type": "date",
            "class": "mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md text-sm shadow-sm placeholder-gray-400 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
        })
    )
    total_guest = forms.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        widget=forms.NumberInput(attrs={
            "min": 1,
            "max": 10,
            "class": "mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md text-sm shadow-sm placeholder-gray-400 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
        })
    )
    room = forms.ModelChoiceField(
        queryset=Room.objects.filter(is_available=True),
        widget=forms.Select(attrs={
            "class": "mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md text-sm shadow-sm placeholder-gray-400 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
        })
    )
    
    class Meta:
        model = Booking
        fields = [
            "guest_name", 
            "guest_email", 
            "room", 
            "check_in", 
            "check_out", 
            "total_guest",
            "special_request"
        ]
        widgets = {
            "guest_name": forms.TextInput(attrs={
                "placeholder": "Enter guest name",
                "class": "mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md text-sm shadow-sm placeholder-gray-400 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
            }),
            "guest_email": forms.EmailInput(attrs={
                "placeholder": "Enter email address",
                "class": "mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md text-sm shadow-sm placeholder-gray-400 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
            }),
            "special_request": forms.Textarea(attrs={
                "placeholder": "Any special requests or preferences?",
                "class": "mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md text-sm shadow-sm placeholder-gray-400 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 resize-none",
                "rows": 4
            })
        }

