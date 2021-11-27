
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.permissions import IsAuthenticated, AllowAny
from tweets.api.serializers import TweetSerializer, TweetSerializerWithComments
from tweets.api.serializers import TweetSerializerForCreate
from rest_framework.response import Response
from tweets.models import Tweet
from newsfeeds.services import NewsFeedService
from rest_framework.response import Response
from rest_framework import status
from functools import wraps


class TweetViewSet(viewsets.GenericViewSet):
    serializer_class = TweetSerializerForCreate
    queryset = Tweet.objects.all()

    def get_permissions(self):
        if self.action == ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAuthenticated()]

    #mainly used to test
    def required_params(request_attr='query_params', params=None):
        """
        当我们使用 @required_params(params=['some_param']) 的时候
        这个 required_params 函数应该需要返回一个 decorator 函数，这个 decorator 函数的参数
        就是被 @required_params 包裹起来的函数 view_func
        """

        # 从效果上来说，参数中写 params=[] 很多时候也没有太大问题
        # 但是从好的编程习惯上来说，函数的参数列表中的值不能是一个 mutable 的参数
        if params is None:
            params = []

        def decorator(view_func):
            """
            decorator 函数通过 wraps 来将 view_func 里的参数解析出来传递给 _wrapped_view
            这里的 instance 参数其实就是在 view_func 里的 self
            """

            @wraps(view_func)
            def _wrapped_view(instance, request, *args, **kwargs):
                data = getattr(request, request_attr)
                missing_params = [
                    param
                    for param in params
                    if param not in data
                ]
                if missing_params:
                    params_str = ','.join(missing_params)
                    return Response({
                        'message': u'missing {} in request'.format(params_str),
                        'success': False,
                    }, status=status.HTTP_400_BAD_REQUEST)
                # 做完检测之后，再去调用被 @required_params 包裹起来的 view_func
                return view_func(instance, request, *args, **kwargs)

            return _wrapped_view

        return decorator


    def list(self, request):
        if 'user_id' not in request.query_params:
            return Response('missing user_id', status=400)
        user_id = request.query_params['user_id']
        tweets = Tweet.objects.filter(user_id=user_id).order_by('-created_at')
        serializer = TweetSerializer(tweets, many=True)
        return Response({'Tweets': serializer.data})

    def retrieve(self,request,*args,**kwargs):
        tweet = self.get_object()
        return Response(TweetSerializerWithComments(tweet).data)


    def create(self, request):
        serializer = TweetSerializerForCreate(
            data=request.data,
            context={'request': request},
        )

        if not serializer.is_valid():
            return Response({
                "success": False,
                "message": "Please check input.",
                "errors": serializer.errors,
            }, status=400)
        # save will trigger create method in TweetSerializerForCreate
        tweet = serializer.save()
        NewsFeedService.fanout_to_followers(tweet)
        return Response(TweetSerializer(tweet).data, status=201)


