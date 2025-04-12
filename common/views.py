from rest_framework import status
from rest_framework.generics import ListAPIView, CreateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from common.models import LikedStadion
from common.serializers import LikedStadionSerializer, LikedStadionPostSerializer
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

    # def delete(self, request, id, *args, **kwargs):
    #     # serializer = LikedStadionPostSerializer(data=request.data)
    #     # if not serializer.is_valid():
    #     #     context = {
    #     #         'status': False,
    #     #         'message': 'Invalid_data'
    #     #     }
    #     #     return Response(context, status=status.HTTP_400_BAD_REQUEST)
    #     try:
    #         # data = serializer.validated_data
    #         stadion_id = id
    #         # stadion_id = data.get('stadion_id', None)
    #         likedstadion = LikedStadion.objects.get(id=stadion_id)
    #         if likedstadion.user != request.user:
    #             context = {
    #                 'status': False,
    #                 'message': 'Sizda huquq yo\'q'
    #             }
    #             return Response(context, status=status.HTTP_400_BAD_REQUEST)
    #         context = {
    #             'status': True,
    #             'message': 'LikedStadion was deleted successfully!!!'
    #         }
    #         return Response(context)
    #
    #     except LikedStadion.DoesNotExist:
    #         context = {
    #             'status': False,
    #             'message': 'LikedStadion topilmadi!!!'
    #         }
    #         return Response(context, status=status.HTTP_400_BAD_REQUEST)
    #
    #     except LikedStadion.DoesNotExist:
    #         context = {
    #             'status': False,
    #             'message': 'Liked Stadion topilmadi!!!'
    #         }
    #         return Response(context, status=status.HTTP_400_BAD_REQUEST)
    #
    #     except Exception as e:
    #         context = {
    #             'status': False,
    #             'message': str(e)
    #         }
    #         return Response(context, status=status.HTTP_400_BAD_REQUEST)


# class StartsPostAPIView(CreateAPIView):
#     serializer_class = StartsPostSerializer
#     queryset = Starts.objects.all()
#     permission_classes = [IsAuthenticated]
#
#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)


class DeleteLikedStadionView(DestroyAPIView):
    queryset = LikedStadion.objects.all()
    lookup_url_kwarg = id

    def get_object(self):
        id = self.kwargs.get('id')
        return self.queryset.all().get(id=id)

