from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .models import Category, Food
from .forms import CreateFoodForm
from django.http import HttpResponse
from .serializers import FoodSerializer
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    ListCreateAPIView,
    RetrieveUpdateAPIView,
    RetrieveDestroyAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request


# Dashboard uchun view
def get(request):
    return render(request, 'dashboard.html')

# GenericAPIView-based views
class FoodApiView(ListAPIView):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer

class FoodDetailAPIView(RetrieveAPIView):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer

class FoodCreateAPIView(ListCreateAPIView):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer

class FoodUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer

class FoodUpdateDeleteAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer

class FoodDeleteAPIView(RetrieveDestroyAPIView):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer

# APIView-based views
class FoodAPIView(APIView):
    def get(self, request: Request):
        foods = Food.objects.values()
        return Response({"foods": foods})

    def post(self, request: Request):
        serializer = FoodSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

class FoodUpdateAPIView(APIView):
    def put(self, request: Request, pk: int):
        try:
            food = Food.objects.get(pk=pk)
        except Food.DoesNotExist:
            return Response({"error": "Food not found."}, status=404)

        serializer = FoodSerializer(food, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)


# food.html sahifasini ko'rsatish uchun View-based view
class FoodView(View):
    def get(self, request):
        categories = Category.objects.all()
        foods = Food.objects.all()
        return render(request, 'FoodView.html', context={"categories": categories, "foods": foods})


# Category bo'yicha foodlarni ko'rsatish
def category(request):  # cat_id parametri kiritildi0
    #category = get_object_or_404(Category, id=cat_id)
    foods = Food.objects.all()  # `Category` bilan bog'liq barcha `Food` ob'ektlari
    categories = Category.objects.all()
    return render(request, 'dashboard.html', context={"foods": foods})


def dashboard(request):
    return render(request, 'base.html')

def FoodView(request):
    return render(request, 'FoodView.html')


def create_food(request):
    if request.method == "POST":
        print(request.POST)  # Yuborilayotgan barcha ma’lumotlarni ko‘rish
        form = CreateFoodForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('FoodView')
    else:
        form = CreateFoodForm() 
    return render(request, 'create_food.html', context={"form": form})


def delete_food(request, id):
    food = Food.objects.get(id=id)
    food.delete()
    return redirect('FoodView')

   
def update_food(request, id):
    food = Food.objects.get(id=id)
    form = CreateFoodForm(instance=food)
    
    if request.method == 'POST':
        form = CreateFoodForm(request.POST, instance=food)
        if form.is_valid():
            form.save()
            return redirect('FoodView')  
    return render(request, 'create_food.html', context={"form": form, "food": food})
