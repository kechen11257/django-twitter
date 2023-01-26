from accounts.api.serializers import UserSerializer
from django.contrib.auth.models import User
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from django.contrib.auth import (
    authenticate as django_authenticate,
    login as django_login,
    logout as django_logout,
)
from accounts.api.serializers import SignupSerializer, LoginSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)


class AccountViewSet(viewsets.ViewSet):
    permission_classes = (AllowAny,)
    serializer_class = SignupSerializer

    @action(methods=['POST'], detail=False)
    def login(self, request):
        """
        默认的 username 是 admin, password 也是 admin
        """
        # -- write your code here --
        #要从request中去获取用户的信息，得到username和password，然后去实现登录
        # 在post中是从哪里来的呢？ 其实是从request的data里面
        # request.data['username']
        # request.data['password']
        # 这么直接写会有问题，因为有可能用户没传，
        # 所以需要用到django的serialize的机制，转到serializers.py文件
        # 定义一个django的serialize，叫做login serializer

        # 把包含username 和 password的信息传给LoginSerializer

        #首先要去import LoginSerializer, 传一个data给LoginSerializer（data从用户请求的request的data中获得）
        #如果是一个GET请求，改成data = request.query.params
        # 就得到了一个serializer的对象，的实例
        serializer = LoginSerializer(data=request.data)
        #调用is.valid()：根据你在serializers.py设置的Field判断是否符合field的要求
        #调了is.valid()之后会output： true/false
        #本例子是false（if not），就要return一个400的写法
        #前面没有写status，是因为默认 status_code = 200,200就不用写
        # 400： bad request，表示用户的请求是不对的，缺这个，少那个了，不是服务端的错，是客户端的错
        
        #处理出错的情况：
        if not serializer.is_valid():
            return Response({
                "success": False,
                "message": "Please check input",
                #可以直接调用serializer里面的errors来获取
                # errors是django rest framwork自带的：只要调用了is.valid()这个函数之后，如果出错了
                # errors就会有信息
                "errors": serializer.errors,
            }, status=400)
        
        #如果没有出错的话，我们会从serializer里面去拿到validated_data
        # 在is.valid()之后，serializer会对数据进行比如说：数据类型的转换等操作
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        # from django.contrib.auth import authenticate as django_authenticate
        #调用django_authenticate,把username和password作为参数传进去
        # 可以看官方文档：https://docs.djangoproject.com/en/3.1/topics/auth/default/#django.contrib.auth.login
        # django_authenticate, 验证和后端是否相同，返回一个user
        # 注意：django_authenticate之后得到的user，才是我们能够拿去login的user（想了解的可以去了解user_backend的机制）
        user = django_authenticate(username=username, password=password)
         #如果是空或者是anonymous
        if not user or user.is_anonymous:
            return Response({
                "success": False,
                "message": "username and password does not match",
            }, status=400)
        
         #调用login的接口来完成login（django的login：from django.contrib.auth import login as django_login,）
        django_login(request, user)
        return Response({
            "success": True,
            # instance也可以不写 UserSerializer(user).data,
            "user": UserSerializer(instance=user).data,
        })

    @action(methods=['POST'], detail=False)
    def logout(self, request):
        """
        登出当前用户
        """
        django_logout(request)
        return Response({"success": True})

    @action(methods=['POST'], detail=False)
    def signup(self, request):
        """
        使用 username, email, password 进行注册
        """
        # 不太优雅的写法
        # username = request.data.get('username')
        # if not username:
        #     return Response("username required", status=400)
        # password = request.data.get('password')
        # if not password:
        #     return Response("password required", status=400)
        # if User.objects.filter(username=username).exists():
        #     return Response("password required", status=400)
        serializer = SignupSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'success': False,
                'message': "Please check input",
                'errors': serializer.errors,
            }, status=400)

        user = serializer.save()
        django_login(request, user)
        return Response({
            'success': True,
            'user': UserSerializer(user).data,
        })

    @action(methods=['GET'], detail=False)
    def login_status(self, request):
        """
        查看用户当前的登录状态和具体信息
        """
        data = {
            'has_logged_in': request.user.is_authenticated,
            # 把虚拟机当前的ip地址显示出来
            'ip':request.META['REMOTE_ADDR'],
            }
        if request.user.is_authenticated:
            data['user'] = UserSerializer(request.user).data
        return Response(data)
