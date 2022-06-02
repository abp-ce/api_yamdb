from django.core.mail import send_mail
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView

from .viewsets import CreateViewSet
from reviews.models import User
from .serializers import UserSerializer, YamdbTokenObtainPairSerializer


class UserViewSet(CreateViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def send_confirmation_code(self):
        confirmation_code = 'asdftyui'
        send_mail(
            subject='Confirmation code',
            message=confirmation_code,
            from_email='fake@yamdb.fake',
            recipient_list=['fake@yamdb.fake']
        )
        return confirmation_code

    def perform_create(self, serializer):
        user = User(username=self.request.data['username'],
                    email=self.request.data['email'])
        user.set_password(self.send_confirmation_code())
        user.save()


class YamdbTokenObtainPairView(TokenObtainPairView):
    serializer_class = YamdbTokenObtainPairSerializer
