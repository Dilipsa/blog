from rest_framework import status
from rest_framework.generics import(
        CreateAPIView,
        DestroyAPIView,
        ListAPIView,
        UpdateAPIView,
        RetrieveAPIView,
        RetrieveUpdateAPIView,

    )


from rest_framework.permissions import(
        AllowAny,
        IsAuthenticated,
        IsAdminUser,
        IsAuthenticatedOrReadOnly
    )

from posts.models import Post
from .permissions import IsOwnerOrReadOnly

from .serializers import (
        PostCreateUpdateSerializer,
        PostDetailSerializer,
        PostListSerializer,
    )


from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from django.shortcuts import redirect, get_object_or_404


class PostCreateAPIView(CreateAPIView):
    # queryset = Post.objects.all()
    # serializer_class = PostCreateUpdateSerializer
    # permission_classes = [IsAuthenticated]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'create.html'

    # def post(self, request, slug):
    #     profile = get_object_or_404(Post, slug=slug)
    #     serializer = PostCreateUpdateSerializer(profile, data=request.data)
    #     if not serializer.is_valid():
    #         return Response({'serializer': serializer, 'profile': profile})
    #     serializer.save()
    #     return redirect('/api/posts/')
    def get(self, request):
        serializer = PostDetailSerializer()
        return Response({'serializer': serializer})

    def post(self, request):
        serializer = PostCreateUpdateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'serializer': serializer})
        serializer.save()
        return redirect('/api/posts/')


    def perform_create(self, serializer):
        # serializer.save(user=self.request.user, title="my title")
        serializer.save(user=self.request.user)


# class PostDetailAPIView(RetrieveAPIView):
class PostDetailAPIView(RetrieveUpdateAPIView):
    # queryset = Post.objects.all()
    # serializer_class = PostDetailSerializer
    # lookup_field = 'slug'
    # lookup_url_kwarg = "abc"

    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'detail.html'

    def get(self, request, slug):
        profile = get_object_or_404(Post, slug=slug)
        serializer = PostDetailSerializer(profile)
        return Response({'serializer': serializer, 'profile': profile})

    # def post(self, request, slug):
    #     profile = get_object_or_404(Post, slug=slug)
    #     serializer = PostCreateUpdateSerializer(profile, data=request.data)
    #     if not serializer.is_valid():
    #         return Response({'serializer': serializer, 'profile': profile})
    #     serializer.save()
    #     return redirect('profile-list')


class PostUpdateAPIView(RetrieveUpdateAPIView):
    # queryset = Post.objects.all()
    # serializer_class = PostCreateUpdateSerializer
    # lookup_field = 'slug'
    # lookup_url_kwarg = "abc"
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'detail.html'

    def post(self, request, slug):
        profile = get_object_or_404(Post, slug=slug)
        serializer = PostCreateUpdateSerializer(profile, data=request.data)
        if not serializer.is_valid():
            return Response({'serializer': serializer, 'profile': profile})
        serializer.save()
        return redirect('/api/posts/')

    def perform_update(self, serializer):
        # serializer.save(user=self.request.user, title="my title")
        serializer.save(user=self.request.user)


class PostDeleteAPIView(DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    lookup_field = 'slug'
    # lookup_url_kwarg = "abc"
    # renderer_classes = [TemplateHTMLRenderer]
    # template_name = 'list.html'
    #
    # def destroy(self, request, *args, **kwargs):
    #     return self.destroy(request, *args, **kwargs)


class PostListAPIView(ListAPIView):
    # queryset = Post.objects.all()
    serializer_class = PostListSerializer

    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'list.html'

    def get(self, request, *args, **kwargs):
        queryset = Post.objects.all()
        return Response({'posts': queryset})
