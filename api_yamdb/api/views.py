from django.core.mail import send_mail

from .viewsets import CreateViewSet
from .models import User
from .serializers import UserSerializer


class UserViewSet(CreateViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def send_password():
        password = 'asdftyui'
        send_mail(
            'Confirmation code',
            password,
            'fake@yamdb.fake',
            ['fake@yamdb.fake']
        )
        return 'asdftyui'

    def perform_create(self, serializer):
        serializer.save(password=self.send_password())

    def perform_update(self, serializer):
        serializer.save(password=self.send_password())
