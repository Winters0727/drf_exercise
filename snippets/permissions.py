from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    객체를 수정할 수 있는 권한을 owner에게 주는 permission
    """

    def has_object_permission(self, request, view, obj):
        # 어떤 요청에도 Read permission은 주어진다.
        # 요청의 Head 또는 Option에 Get HTTP 메서드를 허용
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write 작업은 권한을 가진 owner에 대해서만 이루어져야한다.
        return obj.owner == request.user