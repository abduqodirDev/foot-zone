from datetime import date, timedelta, datetime

from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, RetrieveUpdateAPIView, UpdateAPIView, \
    DestroyAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from order.models import BronStadion
from stadion.models import Stadion, StadionReview, Images
from stadion.serializers import StadionSerializer, StadionDetailSerializer, StadionAddSerializer, \
    AllStadionMapSerializer, StadionImageSerializer, StadionReviewSerializer, StadionAddReviewSerializer, \
    ImageSerializer


class StadionListAPIView(ListAPIView):
    queryset = Stadion.objects.all()
    serializer_class = StadionSerializer


class DetailStadionAPIView(RetrieveAPIView):
    queryset = Stadion.objects.all()
    serializer_class = StadionDetailSerializer
    lookup_url_kwarg = "id"


class AddStadionAPIView(CreateAPIView):
    serializer_class = StadionAddSerializer
    queryset = Stadion
    permission_classes = [IsAuthenticated, ]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AllStadionMapAPIView(ListAPIView):
    serializer_class = AllStadionMapSerializer
    queryset = Stadion.objects.all()


class StadionImageAPIView(ListAPIView):
    serializer_class = StadionImageSerializer
    queryset = Stadion.objects.all()


class StadionReviewAPIView(ListAPIView):
    queryset = StadionReview.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return StadionReviewSerializer
        elif self.request.method == 'POST':
            return StadionAddReviewSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return [AllowAny()]

    def get_queryset(self):
        id = self.kwargs.get('id')
        stadion = Stadion.objects.get(id=id)
        return self.queryset.filter(stadion=stadion).order_by('-created_at')

    def post(self, request, id, *args, **kwargs):
        try:
            serializer = StadionAddReviewSerializer(data=request.data)
            if not serializer.is_valid():
                context = {
                    'status': False,
                    'message': 'Invalid_data'
                }
                return Response(context)
            data = serializer.validated_data
            stadion = Stadion.objects.get(id=id)
            comment = StadionReview.objects.create(user=request.user, stadion=stadion, comment=data.get('comment'))
            context = {
                'status': True,
                'message': 'comment saved successfully',
                'comment_id': comment.id
            }
            return Response(context)

        except Stadion.DoesNotExist:
            context = {
                'status': False,
                'message': 'Stadion topilmadi'
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            context = {
                'status': False,
                'message': str(e)
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)


class AdminStadionListAPIView(ListAPIView):
    serializer_class = StadionAddSerializer
    queryset = Stadion.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        return self.queryset.filter(user=user)


class AdminStadionUpdateAPIView(UpdateAPIView):
    serializer_class = StadionAddSerializer
    queryset = Stadion.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_url_kwarg = 'id'


class AdminStadionDeleteAPIView(DestroyAPIView):
    serializer_class = StadionAddSerializer
    queryset = Stadion.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_url_kwarg = 'id'


class StadionImagePostAPIView(CreateAPIView):
    serializer_class = ImageSerializer
    queryset = Images.objects.all()
    permission_classes = [IsAuthenticated]


class StadionStatistikaKunAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        user = request.user
        stadion_id = request.GET.get('stadion_id', None)
        stadion_date = request.GET.get('stadion_date', None)
        try:
            stadion = Stadion.objects.get(id=stadion_id)
            start_time = datetime.combine(datetime.today(), stadion.start_time)
            end_time = datetime.combine(datetime.today(), stadion.end_time)
            brons = BronStadion.objects.filter(stadion=stadion, date=stadion_date)
            # print('start_time:', start_time)
            # print('end_time:', end_time)
            print('brons:', brons)
            if stadion.user != user:
                context = {
                    'status': False,
                    'message': 'Siz stadion egasi emassiz'
                }
                return Response(context, status.HTTP_400_BAD_REQUEST)
            # print("start_time:", type(start_time))
            result = {}
            context = {}
            price = 0
            for bron in brons:
                price += bron.stadion.price
            while start_time != end_time:
                time = int(str(start_time.time()).split(':')[0])
                print('time:', time)
                for bron in brons:
                    print('bron:', int(bron.time))
                    if int(bron.time) == time:
                        result[f"{start_time.time().strftime('%H:%M')}"] = True
                        start_time = start_time + timedelta(hours=1)
                        continue
                result[f"{start_time.time().strftime('%H:%M')}"] = False
                start_time = start_time + timedelta(hours=1)

            context['bron'] = result
            context['date'] = stadion_date
            context['bron_count'] = len(brons)
            context['daromat'] = price


            return Response(context)

        except Stadion.DoesNotExist:
            context = {
                'status': False,
                'message': 'Stadion topilmadi'
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)

        # except Exception as e:
        #     context = {
        #         'status': False,
        #         'message': str(e)
        #     }
        #     return Response(context, status=status.HTTP_400_BAD_REQUEST)

