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


class ValidationAPIView(generics.GenericAPIView):

    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ['statut', 'created_at',
                     'user__last_name', 'user__first_name']
    serializer_class = ValidationSerializer

    def post(self, request, pk=None):

        reservation = get_object_or_404(Reservations, id=pk)
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            if serializer.validated_data['statut']:
                reservation.statut = "VALIDATE"
            else:
                reservation.statut = "REJECT"
            serializer.save(user=self.request.user, reservation=reservation)
            reservation.save()
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)

        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
