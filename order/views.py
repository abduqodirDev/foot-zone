import datetime
from datetime import date, timedelta

from django.db.models import Q
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from order.models import BronStadion, TASDIQLANGAN
from order.serializers import BronStadionSerializer, BronStadionPostSerializer, MyBronstadionSerializer, \
    MyStadionBronSerializer, VerifyBronSerializer
from order.utils import send_bron_sms
from stadion.models import Stadion
from users.models import User
from users.serializers import UserAdminInfoSerializer


class BronStadionAPIView(APIView):
    queryset = BronStadion.objects.all()
    serializer_class = BronStadionPostSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post']

    def get(self, request, id, *args, **kwargs):
        just = {}
        just1 = {}
        current_date = date.today()
        try:
            stadion = Stadion.objects.get(id=id)
            # bronstadions = stadion.stadion_bronorders.filter(date__gte=current_date, is_active=True, status=TASDIQLANGAN)
            bronstadions = stadion.stadion_bronorders.filter(~Q(status='B'), date__gte=current_date)
            for i in range(7):
                brons = bronstadions.filter(date=current_date)
                serializer = BronStadionSerializer(brons, many=True).data
                just[f"{current_date}"] = serializer
                current_date = current_date + timedelta(days=1)
            # just1["start_time"] = stadion.start_time
            # just1["end_time"] = stadion.end_time
            # just1["price"] = stadion.price
            price = []
            prices = stadion.prices.all()
            for n in range(0, 24):
                just1 = {}
                just1['time'] = n
                p = prices.filter(time=str(n))
                if p:
                    just1['price'] = p.first().price
                    just1['is_active'] = p.first().is_active
                else:
                    just1['price'] = stadion.price
                    just1['is_active'] = True
                price.append(just1)

            data = {
                # 'stadion': just1,
                'brons': just,
                'prices': price
            }
            return Response(data)

        except Stadion.DoesNotExist:
            data = {
                'status': False,
                'message': "Stadion_topilmadi!!!"
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            data = {
                'status': False,
                'message': str(e)
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, id):
        user = request.user
        data = request.data
        serializer = BronStadionPostSerializer(data=data)
        try:
            if not serializer.is_valid():
                context = {
                    'status': False,
                    'message': 'Invalid_data'
                }
                return Response(context, status=status.HTTP_400_BAD_REQUEST)
            stadion = Stadion.objects.get(id=id)

            for dict in data['brons']:
                if BronStadion.objects.filter(~Q(status="B"), stadion=stadion, date=dict['date'], time=str(dict['bron'])).exists():
                    content = {
                        "status": False,
                        "message": "Bu vaqtda stadion bron qilingan!!!"
                    }
                    return Response(content, status=status.HTTP_400_BAD_REQUEST)

            bron_id = []
            if stadion.user == user:
                for dict in data['brons']:
                    time = dict['bron']
                    date = dict['date']
                    bron = BronStadion.objects.create(user=user, stadion=stadion, time=time, date=date, status=TASDIQLANGAN, is_active=True)
                    bron_id.append(bron.id)
            else:
                for dict in data['brons']:
                    time = dict['bron']
                    date = dict['date']
                    bron = BronStadion.objects.create(user=user, stadion=stadion, time=time, date=date)
                    bron_id.append(bron.id)

                send_bron_sms(bron_id)

            context = {
                "status": True,
                "message": "Bron stadions was saved successfully",
                "bron_id": bron_id,
                "user": request.user.first_name
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
                "status": False,
                "message": str(e)
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        else:
            return [IsAuthenticated()]


class MyBronStadion(ListAPIView):
    serializer_class = MyBronstadionSerializer
    queryset = BronStadion.objects.all()
    permission_classes = [IsAuthenticated,]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by('-created_at')


class MyStadionBronListAPIView(ListAPIView):
    serializer_class = MyStadionBronSerializer
    queryset = BronStadion.objects.all()
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        current_time = date.today()
        stadions = Stadion.objects.filter(user=self.request.user)
        query = []
        for stadion in stadions:
            query += self.queryset.filter(stadion=stadion, date__gte=current_time, user__isnull=False).order_by('-created_at')
        return query


class VerifyBronAPIView(APIView):
    serializer_class = VerifyBronSerializer
    http_method_names = ['post', ]

    def post(self, request, *args, **kwargs):
        context_data = {
            "status": False,
            "message": "Invalid_data"
        }
        serializer = VerifyBronSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(context_data, status=status.HTTP_400_BAD_REQUEST)
        try:
            data = serializer.validated_data
            bron_id = data.get('bron_id', None)
            is_active = data.get('is_active', None)
            bron = BronStadion.objects.get(id=bron_id)
            bron.is_active = is_active
            if is_active:
                bron.status = 'T'
            else:
                bron.status = 'B'
            bron.save()
            context = {
                'status': True,
                'is_active': bron.is_active,
                'bron_status': bron.status,
                'bron_id': bron.id
            }
            return Response(context)

        except BronStadion.DoesNotExist:
            context = {
                'status': False,
                'message': 'Bron stadion topilmadi'
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            context = {
                'status': False,
                'message': str(e)
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)


class StadionBronDiagrammaAPIView(APIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = None
    
    def get(self, request, id, *args, **kwargs):
        try:
            context = {}
            user = request.user
            stadion = Stadion.objects.get(id=id)
            if stadion.user != user:
                context = {
                    'status': False,
                    'message': 'Siz bu stadion admini emassiz'
                }
                return Response(context, status=status.HTTP_400_BAD_REQUEST)

            brons = BronStadion.objects.filter(stadion=stadion)
            today_brons = brons.filter(date=date.today())

            context['zakazlar_soni'] = len(today_brons)
            context['tasdiqlangan_bronlar'] = len(today_brons.filter(status='T'))
            context['bekorqilingan_bronlar'] = len(today_brons.filter(status='B'))
            context['kutilayotgan_bronlar'] = len(today_brons.filter(status='K'))

            users = brons.values_list('user', flat=True).distinct()

            just1 = list()
            for user in users:
                user = User.objects.get(id=user)
                just = {'user': UserAdminInfoSerializer(user).data, 'bron': brons.filter(user=user).count()}
                just1.append(just)

            context['users'] = sorted(just1, key=lambda x: x["bron"], reverse=True)
            return Response(context)

        except Stadion.DoesNotExist:
            context = {
                'status': False,
                'message': 'Bu userda stadion mavjud emas'
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            context = {
                'status': False,
                'message': str(e)
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)


class MyStadionHistoryBronAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MyStadionBronSerializer
    queryset = BronStadion.objects.all()

    def get_queryset(self):
        current_time = date.today()
        stadions = Stadion.objects.filter(user=self.request.user)
        query = []
        for stadion in stadions:
            query += self.queryset.filter(stadion=stadion, date__lte=current_time - datetime.timedelta(days=1), user__isnull=False).order_by('-created_at')
        return query
