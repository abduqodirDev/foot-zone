from datetime import date

from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from common.models import LikedStadion
from common.serializers import LikedStadionSerializer, LikedStadionPostSerializer
from order.models import BronStadion
from stadion.models import Stadion


class LikedStadionView(ListAPIView):
    serializer_class = LikedStadionSerializer
    queryset = LikedStadion.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return LikedStadionSerializer
        elif self.request.method == 'POST':
            return LikedStadionPostSerializer
        elif self.request.method == 'DELETE':
            return LikedStadionPostSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def post(self, request, *args, **kwargs):
        serializer = LikedStadionPostSerializer(data=request.data)
        if not serializer.is_valid():
            context = {
                'status': False,
                'message': 'Invalid_data'
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
        try:
            data = serializer.validated_data
            stadion_id = data.get('stadion_id', None)
            stadion = Stadion.objects.get(id=stadion_id)
            LikedStadion.objects.create(user=request.user, stadion=stadion)
            context = {
                'status': True,
                'message': 'LikedStadion was saved successfully!!!'
            }
            return Response(context)

        except Stadion.DoesNotExist:
            context = {
                'status': False,
                'message': 'Stadion topilmadi!!!'
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            context = {
                'status': False,
                'message': str(e)
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        serializer = LikedStadionPostSerializer(data=request.data)
        if not serializer.is_valid():
            context = {
                'status': False,
                'message': 'Invalid_data'
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
        try:
            data = serializer.validated_data
            stadion_id = data.get('stadion_id', None)
            likedstadion = LikedStadion.objects.get(id=stadion_id)
            if likedstadion.user != request.user:
                context = {
                    'status': False,
                    'message': 'Sizda huquq yo\'q'
                }
                return Response(context, status=status.HTTP_400_BAD_REQUEST)
            context = {
                'status': True,
                'message': 'LikedStadion was deleted successfully!!!'
            }
            return Response(context)

        except LikedStadion.DoesNotExist:
            context = {
                'status': False,
                'message': 'LikedStadion topilmadi!!!'
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)

        except LikedStadion.DoesNotExist:
            context = {
                'status': False,
                'message': 'Liked Stadion topilmadi!!!'
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            context = {
                'status': False,
                'message': str(e)
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)


# class StadionMoneyStatistika(APIView):
#     permission_classes = [IsAuthenticated]
#     def get(self, request, *args, **kwargs):
#         user = request.user
#         just = int()
#         if user.role != 'A':
#             context = {
#                 'status': False,
#                 'message': 'Siz admin emassiz!!'
#             }
#             return Response(context, status=status.HTTP_400_BAD_REQUEST)
#         stadions = user.stadions.all()
#         for stadion in stadions:
#             bronstadion = stadion.stadion_bronorders.all().filter(date=date.today())
#

