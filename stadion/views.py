import calendar
from datetime import timedelta, datetime

from django.db.models import Avg
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, \
    DestroyAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from order.models import BronStadion, TASDIQLANGAN
from order.utils import format_time
from stadion.models import Stadion, StadionReview, Images, StadionPrice
from stadion.serializers import StadionSerializer, StadionDetailSerializer, StadionAddSerializer, \
    AllStadionMapSerializer, StadionImageSerializer, StadionReviewSerializer, StadionAddReviewSerializer, \
    ImageSerializer, StadionEditPriceSerializer, StadionImagesSerializer, StadionImagesAddSerializer, \
    StadionImageUploadSerializer
from users.permissions import StadionAdminPermission


class StadionListAPIView(ListAPIView):
    queryset = Stadion.objects.all()
    serializer_class = StadionSerializer

    # def get_queryset(self):
    #     tuman = self.request.query_params.get('tuman', None)
    #     queryset = self.queryset.filter(is_active=True).select_related('tuman')
    #
    #     if tuman:
    #         queryset = queryset.filter(tuman__id=tuman)
    #
    #     return queryset

    from django.db.models import Avg

    def get_queryset(self):
        tuman = self.request.query_params.get('tuman', None)

        queryset = self.queryset.filter(is_active=True).select_related('tuman', 'viloyat').prefetch_related(
            'StadionStarts')

        if tuman:
            queryset = queryset.filter(tuman__id=tuman)

        return queryset.annotate(star_avg=Avg('StadionStarts__rank'))


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

    def get_queryset(self):
        return self.queryset.filter(is_active=True)


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
    permission_classes = [StadionAdminPermission]
    serializer_class = None
    def get(self, request, *args, **kwargs):
        user = request.user
        stadion_id = request.GET.get('stadion_id', None)
        stadion_date = request.GET.get('stadion_date', None)
        try:
            if stadion_id == 'all':
                stadions = user.stadions.all()

                brons = BronStadion.objects.filter(stadion__in=stadions, date=stadion_date, status=TASDIQLANGAN)
                result = {}
                price = 0
                for stadion in stadions:
                    prices = stadion.prices.all()
                    just = brons.filter(stadion=stadion)
                    for bron in just:
                        price += prices.get(time=bron.time).price

                for time in range(0, 24):
                    t = format_time(str(time)).split('-')[0]
                    result[t] = False
                    for bron in brons:
                        if int(bron.time) == time:
                            result[t] = True
                            continue

                context = {
                    'bron': result,
                    'date': stadion_date,
                    'bron_count': len(brons),
                    'daromad': price
                }

                return Response(context)

            stadion = Stadion.objects.get(id=stadion_id)
            prices = stadion.prices.all()
            if stadion.user != user:
                context = {
                    'status': False,
                    'message': 'Siz stadion egasi emassiz'
                }
                return Response(context, status.HTTP_400_BAD_REQUEST)

            brons = BronStadion.objects.filter(stadion=stadion, date=stadion_date, status=TASDIQLANGAN)
            result = {}
            context = {}
            price = 0

            for bron in brons:
                price += prices.get(time=bron.time).price

            for time in range(0, 24):
                t = format_time(str(time)).split('-')[0]
                result[t] = False
                for bron in brons:
                    if int(bron.time) == time:
                        result[t] = True
                        continue

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

        except Exception as e:
            context = {
                'status': False,
                'message': str(e)
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)


class StadionStatistikaOyAPIView(APIView):
    permission_classes = [StadionAdminPermission]
    serializer_class = None

    @staticmethod
    def validate_yil(yil):
        if not str(yil).isdigit() or len(yil) != 4:
            return False
        else:
            return True

    @staticmethod
    def validate_oy(oy):
        if not str(oy).isdigit() or int(oy) not in range(1, 13):
            return False
        else:
            return True

    def get(self, request, *args, **kwargs):
        user = request.user
        stadion_id = request.GET.get('stadion_id', None)
        data = request.GET.get('data', None)
        oy = data.split('-')[1]
        yil = data.split('-')[0]
        if not self.validate_yil(yil):
            context = {
                'status': False,
                'message': "Yilni to'g'ri kiriting"
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)

        if not self.validate_oy(oy):
            context = {
                'status': False,
                'message': "Oyni to'g'ri kiriting"
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)

        try:
            if stadion_id == 'all':
                stadions = user.stadions.all()

                brons = BronStadion.objects.filter(stadion__in=stadions, date__year=yil, date__month=oy,
                                                   status=TASDIQLANGAN)
                _, days = calendar.monthrange(int(yil), int(oy))

                context = {}
                daromod = 0

                for day in range(1, days + 1):
                    result = {}
                    price = 0
                    bron = brons.filter(date__day=day)
                    result['bron'] = len(bron)
                    for b in bron:
                        a = StadionPrice.objects.filter(stadion=b.stadion, time=b.time).first()
                        if a:
                            price += a.price
                        else:
                            price += b.stadion.price
                    result['price'] = price
                    context[str(day)] = result
                    daromod += price

                context['yil'] = yil
                context['oy'] = oy
                context['bron_count'] = len(brons)
                context['daromad'] = daromod

                return Response(context)

            stadion = Stadion.objects.get(id=stadion_id)
            prices = stadion.prices.all()
            if stadion.user != user:
                context = {
                    'status': False,
                    'message': 'Siz stadion egasi emassiz'
                }
                return Response(context, status=status.HTTP_400_BAD_REQUEST)

            brons = BronStadion.objects.filter(stadion=stadion, date__year=yil, date__month=oy, status=TASDIQLANGAN)
            _, days = calendar.monthrange(int(yil), int(oy))

            context = {}
            daromod = 0

            for day in range(1, days+1):
                result = {}
                price = 0
                bron = brons.filter(date__day=day)
                result['bron'] = len(bron)
                for b in bron:
                    price += prices.get(time=b.time).price
                result['price'] = price
                context[str(day)] = result
                daromod += price

            context['yil'] = yil
            context['oy'] = oy
            context['bron_count'] = len(brons)
            context['daromad'] = daromod
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


class StadionStatistikaYilAPIView(APIView):
    permission_classes = [StadionAdminPermission]
    serializer_class = None

    @staticmethod
    def validate_yil(yil):
        if not str(yil).isdigit() or len(yil) != 4:
            return False
        else:
            return True

    def get(self, request, *args, **kwargs):
        user = request.user
        stadion_id = request.GET.get('stadion_id', None)
        yil = request.GET.get('yil', None)
        if not self.validate_yil(yil):
            context = {
                'status': False,
                'message': "Yilni to'g'ri kiriting"
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)

        try:
            if stadion_id == 'all':
                stadions = user.stadions.all()

                brons = BronStadion.objects.filter(stadion__in=stadions, date__year=yil, status=TASDIQLANGAN)
                context = {}
                daromad = 0

                for day in range(1, 13):
                    result = {}
                    price = 0
                    bron = brons.filter(date__month=day)
                    for b in bron:
                        a = StadionPrice.objects.filter(stadion=b.stadion, time=b.time).first()
                        if a:
                            price += a.price
                        else:
                            price += b.stadion.price
                    result['bron'] = len(bron)
                    result['price'] = price
                    context[str(day)] = result
                    daromad += price

                context['yil'] = yil
                context['bron_count'] = len(brons)
                context['daromad'] = daromad
                return Response(context)

            stadion = Stadion.objects.get(id=stadion_id)
            prices = stadion.prices.all()
            if stadion.user != user:
                context = {
                    'status': False,
                    'message': 'Siz stadion egasi emassiz'
                }
                return Response(context, status=status.HTTP_400_BAD_REQUEST)

            brons = BronStadion.objects.filter(stadion=stadion, date__year=yil, status=TASDIQLANGAN)
            context = {}
            daromad = 0

            for day in range(1, 13):
                result = {}
                price = 0
                bron = brons.filter(date__month=day)
                for b in bron:
                    price += prices.get(time=b.time).price
                result['bron'] = len(bron)
                result['price'] = price
                context[str(day)] = result
                daromad += price

            context['yil'] = yil
            context['bron_count'] = len(brons)
            context['daromad'] = daromad
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


class StadionStatistikaUmumAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = None

    def get(self, request, *args, **kwargs):
        user = request.user
        bron_count = 0
        price = 0
        context = {}
        stadions = user.stadions.all()
        context['stadion_count'] = len(stadions)
        for stadion in stadions:
            just = 0
            prices = stadion.prices.all()
            brons = stadion.stadion_bronorders.filter(status=TASDIQLANGAN)
            for bron in brons:
                just += prices.get(time=bron.time).price
            bron_count += len(brons)
            price += just
        context['bron_count'] = bron_count
        context['price'] = price

        return Response(context)


class StadionStatistikaKunlarAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        stadion_id = request.GET.get('stadion_id', None)
        date_to = request.GET.get('date_to', None)
        date_from = request.GET.get('date_from', None)

        try:
            if stadion_id == 'all':
                stadions = user.stadions.all()

                date_from = datetime.strptime(date_from, '%Y-%m-%d').date()
                date_to = datetime.strptime(date_to, '%Y-%m-%d').date()
                brons = BronStadion.objects.filter(stadion__in=stadions, date__lte=date_from, date__gte=date_to)
                context = {}
                daromad = 0
                while date_to <= date_from:
                    result = {}
                    price = 0
                    bron = brons.filter(date=date_to)
                    result['bron'] = len(bron)
                    for b in bron:
                        a = StadionPrice.objects.filter(stadion=b.stadion, time=b.time).first()
                        if a:
                            price += a.price
                        else:
                            price += b.stadion.price

                    result['price'] = price
                    context[str(date_to)] = result
                    daromad += price

                    date_to += timedelta(days=1)

                context['bron_count'] = len(brons)
                context['daromad'] = daromad

                return Response(context)

            stadion = Stadion.objects.get(id=stadion_id)
            prices = stadion.prices.all()
            if stadion.user != user:
                context = {
                    "status": False,
                    'message': 'Error'
                }
                return Response(context, status=status.HTTP_400_BAD_REQUEST)

            date_from = datetime.strptime(date_from, '%Y-%m-%d').date()
            date_to = datetime.strptime(date_to, '%Y-%m-%d').date()
            brons = BronStadion.objects.filter(stadion=stadion, date__lte=date_from, date__gte=date_to)
            context = {}
            daromad = 0
            while date_to <= date_from:
                result = {}
                price = 0
                bron = brons.filter(date=date_to)
                result['bron'] = len(bron)
                for b in bron:
                    price += prices.get(time=b.time).price
                result['price'] = price
                context[str(date_to)] = result
                daromad += price

                date_to += timedelta(days=1)

            context['bron_count'] = len(brons)
            context['daromad'] = daromad

            # for day in range(1, days + 1):
            #     result = {}
            #     bron = brons.filter(date__day=day)
            #     result['bron'] = len(bron)
            #     result['price'] = stadion.price * len(bron)
            #     context[str(day)] = result

            return Response(context)

        except Stadion.DoesNotExist:
            context = {
                'status': False,
                'message': 'Stadion not found!!!'
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            context = {
                'status': False,
                'message': str(e)
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)


class StadionEditPriceAPIView(APIView):
    http_method_names = ['post']
    permission_classes = [IsAuthenticated]
    serializer_class = StadionEditPriceSerializer

    def post(self, request, id, *args, **kwargs):
        user = request.user
        try:
            stadion = Stadion.objects.get(id=id)
            prices = stadion.prices.all()
            serializer = StadionEditPriceSerializer(data=request.data)
            if stadion.user != user:
                context = {
                    'status': False,
                    'message': 'Error'
                }
                return Response(context, status=status.HTTP_400_BAD_REQUEST)

            if not serializer.is_valid():
                context = {
                    'status': False,
                    'message': 'Invalid_data'
                }
                return Response(context, status=status.HTTP_400_BAD_REQUEST)
            data = serializer.validated_data
            time = data.get('time')
            price = data.get('price')
            Price = prices.filter(time=time)
            if Price:
                Price.update(price=price)
            else:
                StadionPrice.objects.create(stadion=stadion, time=time, price=price)

            context = {
                'status': True,
                'message': 'Yangilandi'
            }
            return Response(context)

        except Stadion.DoesNotExist:
            context = {
                'status': False,
                'message': 'Stadion not found'
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            context = {
                'status': False,
                'message': str(e)
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)


class StadionImagesAPIView(ListAPIView):
    serializer_class = StadionImagesSerializer
    queryset = Images.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_url_kwarg = 'id'

    def get_queryset(self):
        id = self.kwargs.get(self.lookup_url_kwarg)
        return self.queryset.filter(stadion_id=id)


class StadionImagesDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated]
    http_method_names = ['post']

    def post(self, request, id, pk, *args, **kwargs):
        try:
            user = request.user
            stadion = Stadion.objects.get(id=id)
            image = Images.objects.get(id=pk)
            if stadion.user != user or image.stadion != stadion:
                context = {
                    'status': False,
                    'message': 'Error'
                }
                return Response(context, status=400)
            image.delete()
            context = {
                'status': True,
                'message': 'Image deleted'
            }
            return Response(context)

        except Images.DoesNotExist:
            context = {
                'status': False,
                'message': 'Image not found'
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)

        except Stadion.DoesNotExist:
            context = {
                'status': False,
                'message': 'Stadion not found'
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)


class StadionImagesAllAPIView(APIView):
    permission_classes = [StadionAdminPermission]
    def post(self, request, *args, **kwargs):
        serializer = StadionImageUploadSerializer(data=request.data)

        if serializer.is_valid():
            stadion_id = serializer.validated_data['stadion_id']
            stadion = Stadion.objects.get(id=stadion_id)
            if request.user != stadion.user:
                return Response({"message": "Error"}, status=status.HTTP_400_BAD_REQUEST)

            serializer.save()

            return Response({"message": "Rasmlar muvaffaqiyatli qo‘shildi"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
