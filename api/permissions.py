from rest_framework import permissions, authentication


class CustomIsAdmin(permissions.BasePermission):
    '''
    Custom permission to only allow owners of an object to edit it.
    '''

    def has_object_permission(self, request, view, obj):
        #읽기 권한은 누구에게나 있으므로 GET, HEAD, OPTIONS request는 항상 열려있다.
        
        
        #쓰기 권한은 owner에게만 있다.
        return request.user.is_superuser



