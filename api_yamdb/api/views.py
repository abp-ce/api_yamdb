from django.core.mail import send_mail
from rest_framework.permissions import AllowAny

from .viewsets import CreateUpdateViewSet
from reviews.models import User
from .serializers import UserSerializer


class UserViewSet(CreateUpdateViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def send_password():
        password = 'asdftyui'
        send_mail(
            subject='Confirmation code',
            message=password,
            from_email='fake@yamdb.fake',
            recipient_list=['fake@yamdb.fake']
        )
        return 'asdftyui'

    def perform_create(self, serializer):
        serializer.save(password=self.send_password)

    def perform_update(self, serializer):
        serializer.save(password=self.send_password)
