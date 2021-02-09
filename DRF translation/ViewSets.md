# ViewSets

```
요청을 처리하는 컨트롤러를 위한 라우트가 결정된 후, 컨트롤러는 요청에 대한 적절한 결과물을 생성할 수 있어야 한다.
- 루비 온 레일즈 문서
```

DRF는 `ViewSet`라는 단일 클래스를 제공하는데, 이는 뷰에 관련된 로직들을 조합할 수 있게 한다. 다른 프레임워크에서 언급하는 'Controllers'나 'Resources'와 유사하다.

`ViewSet` 클래스는 `.get()`, `.post()`와 같은 어떤 메서드 핸들러도 제공하지 않는 class-based View다. 대신 `.list()`, '`create()`와 같은 액션들을 제공한다.

`ViewSet`을 위한 메서드 핸들러는 뷰를 완성하는 시점에서 `.as_view()` 메서드로

일반적으로 urlconf에 viewset의 views를 명시적으로 등록하기보다는 viewset을 router 클래스에 등록하여 자동으로 urlconf가 결정되도록 하는 것이 좋다.

```python
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from myapp.serializers import UserSerializer
from rest_framework import viewsets
from rest_framework.response import Response

class UserViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)
```

필요에 따라 다음과 같이 viewset을 두 개의 view로 분리할 수 있다.

```python
user_list = UserViewSet.as_view({'get':'list'})
user_detail = UserViewSet.as_view({'get':'retrieve'})
```

일반적으로 이렇게 viewset을 분리하지는 않는다. 대신 라우터에 등록하여 자동으로 urlconf을 생성한다.

```python
from myapp.views import UserViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
urlpatterns = router.urls
```

다음과 같이 viewset이 아닌 모델을 그대로 사용할 수도 있다.

```python
class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
```

`View` 클래스보다 `ViewSet`을 사용하는 것이 2가지 면에서 장점이 있다.

- 반복되는 로직을 단일 클래스로 조합할 수 있다. 상기 예처럼 `queryset`을 한번 특정하면 여러 뷰에서 재사용이 가능하다.
- 라우터를 사용함으로써 더이상 URL conf를 신경쓸 필요가 없다.

`View`든 `ViewSet`든 트레이드 오프가 존재한다. 일반 view와 URL conf를 사용하는 것은 명시적이고 작업에 더 자세하게 관여할 수 있다. viewset은 빠르게 또는 큰 API를 구축할 때 도움이 되며, 일관적인 URL conf를 강제할 때도 유용하다.



### ViewSet actions

DRF에서 제공하는 기본 라우터에는 다음과 같이 기본적인 CRUD 라우트를 제공한다.

```python
class UserViewSet(viewsets.ViewSet):
    """
    비어있는 viewset은 router 클래스에 의해 다루어지는 기본 액션이다.
    만약에 포맷 접미어를 사용 중이라면 'format=None' 키워드 인자를 각각의 액션에 추가해야한다.
    """

    def list(self, request):
        pass

    def create(self, request):
        pass

    def retrieve(self, request, pk=None):
        pass

    def update(self, request, pk=None):
        pass

    def partial_update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        pass
```



### Introspecting ViewSet actions

- `basename` : 생성된 URL의 기본 이름
- `action` : 현재 액션의 이름(create, list)
- `detail` : 현재 액션이 리스트 또는 디테일인지 여부
- `suffix` : viewset의 타입을 보여주는 접미어
- `name` : viewset의 이름
- `description` : viewset의 개별 뷰에 대한 설명

```python
def get_permission(self):
    if self.action == 'list':
        permission_classes = [IsAuthenticated]
    else:
        permission_classes = [IsAdmin]
    return [permission() for permission in permission_classes]
```



### Marking extra action for routing



```python
from django.contrib.auth.models import User
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from myapp.serializers import UserSerializer, PasswordSerializer

class UserViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides the standard actions
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=True, methods=['post'])
    def set_password(self, request, pk=None):
        user = self.get_object()
        serializer = PasswordSerializer(data=request.data)
        if serializer.is_valid():
            user.set_password(serializer.data['password'])
            user.save()
            return Response({'status': 'password set'})
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False)
    def recent_users(self, request):
        recent_users = User.objects.all().order_by('-last_login')

        page = self.paginate_queryset(recent_users)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(recent_users, many=True)
        return Response(serializer.data)
```

