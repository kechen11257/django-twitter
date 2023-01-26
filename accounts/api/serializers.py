from django.contrib.auth.models import User
from rest_framework import serializers, exceptions


# 取出数据，然后变成json的格式
#在前端去渲染一个用户的object的时候，我们把他转成一个json的格式
#在 django rest framwork中还有一个用处：用来去验证用户的输入（validation）
#看看用户输入的是不是按照要求来的
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')


# signup的检测比login多，因为login只需要去检测username和password有没有就好了
# 用 ModelSerializer表示当.save()的时候， signup的用户实际上能够创建出来
class SignupSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=20, min_length=6)
    password = serializers.CharField(max_length=20, min_length=6)
    email = serializers.EmailField()

    #因为传入的是ModelSerializer，所以会指定一下model是谁
    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    # validate（）帮助实现，当我们去call is_valid的时候
    def validate(self, data):
        # TODO<HOMEWORK> 增加验证 username 是不是只由给定的字符集合构成

        # 有时候我们希望password和username大小写不敏感
        # 在存储username的时候我们就要去存储他的小写的格式
        # 如果小写的username有重复的话，就会抛出一个异常
        if User.objects.filter(username=data['username'].lower()).exists():
            # from rest_framework import serializers, exceptions
            raise exceptions.ValidationError({
                'message': 'This username has been occupied.'
            })
        if User.objects.filter(email=data['email'].lower()).exists():
            raise exceptions.ValidationError({
                'message': 'This email address has been occupied.'
            })
        return data

    #传入的数据是已经经过validated
    def create(self, validated_data):
        username = validated_data['username'].lower()
        email = validated_data['email'].lower()
        # password大小写敏感
        password = validated_data['password']

        # create_user重要的做了：你传进去的password是明文，create_user讲明文变成了密文+对username和email进行了normalize（前面后面多了空格）
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
        )
        return user

# 只是会帮我们去检测，这两项他是否存在
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
