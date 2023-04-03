from django.shortcuts import render
from rest_framework import viewsets, filters, permissions, response, status, generics
from django.shortcuts import get_object_or_404
from reservations.models import Reservations
from reservations.serializer import ReservationSerializer, ValidationSerializer
from rest_framework.decorators import action


class ReservationViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    # authentication_classes = ()
    filter_backends = (filters.SearchFilter,)
    filterset_field = ['statut', 'deposit', 'date']
    search_fields = ['statut', 'deposit', 'date',
                     'customer__last_name', 'customer__first_name']

    queryset = Reservations.objects.all()
    serializer_class = ReservationSerializer

    def create(self, request):

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(customer=self.request.user)
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)

        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None, partial=False):

        reservation = self.get_object()
        serializer = self.serializer_class(
            reservation, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save(owner=self.request.user)
            return response.Response(serializer.data, status=status.HTTP_200_OK)

        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # @action(detail=True, methods=['patch'])
    # def validate(self, request, pk=None):
    #     """ validate reservation """

    #     registration = self.get_object()
    #     serializer = self.serializer_class(data=request.data, partial=True)
    #     if serializer.is_valid():
    #         registration.statut = serializer.validated_data['statut']
    #         registration.owner = self.request.user
    #         registration.save()
    #         return response.Response({'message': 'statut updated'}, status=status.HTTP_200_OK)
    #     else:
    #         return response.Response(serializer.errors,
    #                                  status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def validate(self, request, pk=None):
        """ reservation validation """

        reservation = self.get_object()
        serializer = ValidationSerializer(data=request.data)
        if serializer.is_valid():
            if serializer.validated_data['statut']:
                reservation.statut = "VALIDATE"
            else:
                reservation.statut = "REJECT"

            serializer.save(user=self.request.user, reservation=reservation)
            reservation.save()
            return response.Response({'message': 'statut updated'}, status=status.HTTP_200_OK)
        else:
            return response.Response(serializer.errors,
                                     status=status.HTTP_400_BAD_REQUEST)
