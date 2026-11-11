from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import PacketSerializer
from .engines.rule_based import RuleBasedIDS
from .engines.ml_engine import MachineLearningIDS
from .engines.dl_engine import DeepLearningIDS

rule_engine = RuleBasedIDS()
ml_engine = MachineLearningIDS()
dl_engine = DeepLearningIDS()

class RuleDetectionView(APIView):
    def post(self, request):
        serializer = PacketSerializer(data=request.data)
        if serializer.is_valid():
            return Response(rule_engine.evaluate(serializer.validated_data), status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MLDetectionView(APIView):
    def post(self, request):
        serializer = PacketSerializer(data=request.data)
        if serializer.is_valid():
            return Response(ml_engine.evaluate(serializer.validated_data), status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DLDetectionView(APIView):
    def post(self, request):
        serializer = PacketSerializer(data=request.data)
        if serializer.is_valid():
            return Response(dl_engine.evaluate(serializer.validated_data), status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CompareAllView(APIView):
    def post(self, request):
        serializer = PacketSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            return Response({
                "rule_based": rule_engine.evaluate(data),
                "machine_learning": ml_engine.evaluate(data),
                "deep_learning": dl_engine.evaluate(data)
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)