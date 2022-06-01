from .viewsets import CreateViewSet
from .models import User
from .serializers import UserSerializer


class UserViewSet(CreateViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        # send email
        serializer.save(user=self.request.user)
