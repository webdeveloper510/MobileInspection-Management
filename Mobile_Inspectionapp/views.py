from .models import *
from .serializer import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from Mobile_Inspectionapp.renderer import UserRenderer
from django.http import Http404
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404

class InspectionView(APIView): 
   renderer_classes=[UserRenderer]
   def post(self, request, format=None):
      serializer=InspectionSerializer(data=request.data)
      if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"message":"Inspection Completed successfully"})
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

class Login(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer_class = UserLoginSerializer(data=request.data)
        if serializer_class.is_valid(raise_exception=True):
            return Response({"Status":"you have logged in successfully"})
        return Response(serializer_class.errors, status=HTTP_400_BAD_REQUEST)
      
class Logout(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserLogoutSerializer

    def post(self, request, *args, **kwargs):
        serializer_class = UserLogoutSerializer(data=request.data)
        if serializer_class.is_valid(raise_exception=True):
            return Response(serializer_class.data, status=HTTP_200_OK)
        return Response(serializer_class.errors, status=HTTP_400_BAD_REQUEST) 
        

            
class UnitListView(APIView):
   
    def get(self, request, format=None):
        snippets = Unit.objects.all().order_by('id')
        serializer = UnitSerializer(snippets, many=True)
        return Response(serializer.data)
    
    
    def post(self, request, format=None):
        serializer = UnitSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'success':'Unit added Successfully'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeleteUnit(APIView):
    
    @csrf_exempt
    def get_object(self, pk):
        try:
            return Unit.objects.get(pk=pk)
        except Unit.DoesNotExist:
            raise Http404  
    @csrf_exempt
    def delete(self, request, pk, format=None):
        unit = self.get_object(pk)
        if unit.delete():
          return Response({'success':'unit deleted successfully'})
        return Response(status=status.HTTP_400_BAD_REQUEST)
          
            
class ServicesListView(APIView):
   
    def get(self, request, format=None):
        snippets = Services.objects.all().order_by('id')
        serializer = ServicesSerializer(snippets, many=True)
        return Response(serializer.data)
    
    
    def post(self, request, format=None):
        serializer = ServicesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'success':'services added Successfully'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
    
class DeleteService(APIView):
    
    @csrf_exempt
    def get_object(self, pk):
        try:
            return Services.objects.get(pk=pk)
        except Services.DoesNotExist:
            raise Http404  
    @csrf_exempt
    def delete(self, request, pk, format=None):
        service = self.get_object(pk)
        if service.delete():
          return Response({'success':'service deleted successfully'})
        return Response(status=status.HTTP_400_BAD_REQUEST)       
            
class ElectricalInspectableItemView(APIView):
   
    def get(self, request, format=None):
        snippets = ElectricalInspectableItem.objects.all().order_by('id')
        serializer = ElectricalInspectableItemSerializer(snippets, many=True)
        return Response(serializer.data)
    
    
    def post(self, request, format=None):
        serializer = ElectricalInspectableItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'success':'Electrical Item added Successfully'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

class DeleteElectricalInspectableItem(APIView):
    
    @csrf_exempt
    def get_object(self, pk):
        try:
            return ElectricalInspectableItem.objects.get(pk=pk)
        except ElectricalInspectableItem.DoesNotExist:
            raise Http404  
    @csrf_exempt
    def delete(self, request, pk, format=None):
        item = self.get_object(pk)
        if item.delete():
          return Response({'success':'item deleted successfully'})
        return Response(status=status.HTTP_400_BAD_REQUEST)              

            
      