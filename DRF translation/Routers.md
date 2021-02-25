# Routers

```
"Resource 라우팅은 주어진 resource한 컨트롤러로부터 빠르게 일반 라우트들을 생성할 수 있게 해준다. 각 인덱스에 대해 별개의 라우트를 선언하는 것 보다... 단 한줄의 코드만으로 resource한 라우트를 생성할 수 있다."
- 루비 온 레일즈 문서
```

레일즈와 같은 몇몇 웹 프레임워크들은 어떻게 해야 URL을 들어온 요청들을 다루는 로직에 자동으로 매핑할 수 있는지에 관한 기능들을 제공한다.

REST 프레임워크 역시 장고에 자동으로 간편하고 빠르게 URL 라우트를 생성하는 기능을 제공한다.



### Usage

`SimpleRouter`를 활용한 예제다.

```python
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'users', UserViewSet)
router.register(r'accounts', AccountViewSet)
urlpatterns = router.urls
```

`register()` 메서드를 사용하기 위해서는 2개의 인자를 필수적으로 입력해야한다.

- `prefix` - 라우트를 설정하기 위한 URL 접두사
- `viewset` - viewset 클래스

부가적으로, 다음과 같은 인자들을 설정할 수 있다.

- `basename` - 생성된 URL이 기본적으로 사용할 이름이다. 입력하지 않을 경우, viewset의 `queryset` 인자로 자동으로 설정된다. 만약 viewset이 `queryset` 인자를 가지지 않을 경우, 명시적으로 `basename`을 등록해야한다.

상기의 예시는 다음과 같은 URL을 생성한다.

- URL Pattern : `^users/$` Name : `user-list`
- URL Pattern : `^users/{pk}/$` Name : `user-detail`
- URL Pattern : `^accounts/$` Name : `account-list`
- URL Pattern : `^accounts/{pk}/$` Name : `account-detail`

`basename` 인자를 입력하지 않았기 때문에 viewset의 `queryset` 인자로부터 각각 `user`와 `account`를 가져왔다. 만약, `get_queryset` 메서드와 같이 오버라이딩에 의해 `.queryset` 인자가 지정되지 않았다면 `basename` 인자를 반드시 명시적으로 설정해줘야한다.



### Using `include` with routers

라우터 인스턴스의 `.urls` 인자는 URL 패턴들의 기본 리스트다. 이 url들을 장고에 반영하는 몇 가지 다른 방법들이 있다.

```python
from rest_framework import routers

router = router.SimpleRouter()
router.register(r'users', UserViewSet)
router.register(r'accounts', ACcountViewSet)

urlpatterns = [
    path('forgot-password/', ForgotPasswordFormView.as_view()),
]

urlpatterns += router.urls
```

다른 대안으로 장고의 `include` 함수를 사용할 수 있다.

```python
urlpatterns = [
    path('forgot-password/', ForgotPasswordFormView.as_view()),
    path('', include(router.urls)),
]
```

애플리케이션의 네임스페이스와 함께 `include` 함수를 사용할 수도 있다.

```python
urlpatterns = [
    path('forgot-password/', ForgotPasswordFormView.as_view()),
    path('api/', include((router.urls, 'app_name'))),
]
```

또는, 애플리케이션과 인스턴스 네임스페이스를 둘 다 사용할 수도 있다.

```python
urlpatterns = [
    path('forgot-password/', ForgotPasswordFormView.as_view()),
    path('api/', include((router.urls, 'app_name'), namespace='instance_name')),
]
```



### Routing for extra actions

