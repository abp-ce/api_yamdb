from rest_framework import mixins, viewsets


class CreateUpdateViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin,
                          viewsets.GenericViewSet):
    pass
