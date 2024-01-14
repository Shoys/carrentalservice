from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from .models import Car, Booking
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth import login
import json

def admin_check(user):
    return user.is_authenticated and user.is_staff

@csrf_exempt
@require_http_methods(["GET", "POST"])
def car_operations(request):
    if request.method == 'GET':
        cars = Car.objects.all().values()
        return JsonResponse(list(cars), safe=False)
    elif request.method == 'POST':
        # Add permission check for admin
        # Assuming admin_check function or similar logic
        if not admin_check(request.user):
            return HttpResponse(status=403)
        try:
            data = json.loads(request.body)
            car = Car.objects.create(**data)
            return JsonResponse({'id': car.id}, status=201)
        except Exception as e:
            return HttpResponse(status=400)

@csrf_exempt
@require_http_methods(["GET", "PUT", "DELETE"])
def specific_car_operations(request, carId):
    try:
        car = Car.objects.get(id=carId)
    except Car.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        return JsonResponse({'id': car.id, 'make': car.make, 'model': car.model, 'year': car.year, 'color': car.color})

    elif request.method == 'PUT':
        if not admin_check(request.user):
            return HttpResponse(status=403)
        try:
            data = json.loads(request.body)
            for key, value in data.items():
                setattr(car, key, value)
            car.save()
            return HttpResponse(status=200)
        except Exception as e:
            return HttpResponse(status=400)

    elif request.method == 'DELETE':
        if not admin_check(request.user):
            return HttpResponse(status=403)
        car.delete()
        return HttpResponse(status=204)

@csrf_exempt
@login_required
@require_http_methods(["GET", "POST"])
def booking_operations(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            car_id = data.get('carId')
            start_time = data.get('startTime')
            end_time = data.get('endTime')

            # Fetch the Car instance
            try:
                car = Car.objects.get(id=car_id)
            except Car.DoesNotExist:
                return JsonResponse({'error': 'Car not found.'}, status=400)

            # Check for any bookings that overlap with the requested time for the same car
            overlapping_bookings = overlapping_bookings = Booking.objects.filter(
                car_id=car_id,
                endTime__gt=start_time,
                startTime__lt=end_time
            ).exists()

            if overlapping_bookings:
                # Car is unavailable, return an appropriate response
                return JsonResponse({'error': 'Car is unavailable for the requested time.'}, status=400)

            # Create the Booking instance
            booking = Booking.objects.create(
                car=car,
                user=request.user,
                startTime=start_time,
                endTime=end_time,
                status='confirmed' # Status is always 'confirmed'
            )

            return JsonResponse({'bookingId': booking.bookingId}, status=201)
        except KeyError as e:
            # Handle missing fields in request
            return JsonResponse({'error': str(e) + ' is required.'}, status=400)
        except Exception as e:
            # Handle other errors
            print(e)
            return HttpResponse(status=400)
    elif request.method == 'GET':
        if not request.user.is_authenticated:
            return HttpResponse(status=403)
        bookings = Booking.objects.filter(user=request.user).values()
        return JsonResponse(list(bookings), safe=False)

@login_required
@require_http_methods(["GET"])
def index(request):
    return render(request, 'booking/index.html')

@require_http_methods(["GET", "POST"])
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    elif request.method == 'GET':
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})
