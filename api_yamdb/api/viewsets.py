from rest_framework import mixins, viewsets


class MeViewSet(viewsets.GenericViewSet):
    pass


class CreateListDestroyViewSet(mixins.CreateModelMixin,
                               mixins.ListModelMixin,
                               mixins.DestroyModelMixin,
                               viewsets.GenericViewSet):
    pass
