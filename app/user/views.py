from rest_framework import (
    generics,
    permissions,
    status,
    viewsets,
)
from user.serializers import UserSerializer, UserMeImageSerializer
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action
from rest_framework.response import Response


@extend_schema(tags=['User'])
class CreateUserView(generics.CreateAPIView):
    """ View to create a new user in the system. """

    serializer_class = UserSerializer


@extend_schema(tags=['Me'])
class UserMeView(generics.RetrieveUpdateAPIView):
    """ View for authenticated user. """

    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """ Retrieve and return the authenticated user. """
        return self.request.user


@extend_schema(tags=['Me'])
class UserMeCustomActionsView(viewsets.ModelViewSet):
    """ View for custom actions in the authenticated user. """

    serializer_class = UserMeImageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """ Retrieve and return the authenticated user. """
        return self.request.user

    @action(methods=['PATCH'], detail=True, url_path='upload-image')
    def upload_image(self, request):
        """ Upload an image to the authenticated user. """

        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
