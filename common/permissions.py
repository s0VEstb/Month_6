from rest_framework.permissions import BasePermission


class IsModerator(BasePermission):
    """1. Модератор **должен быть is_staff=True**.
       2. Модератор **может просматривать, изменять и удалять** чужие продукты.
       3. Модератор **не может создавать** продукты (запрещён метод POST)
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        if request.method == 'POST' and request.user.is_staff:
            return False
        return True
    
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        
        owner = getattr(obj, 'owner', None)
        return owner == request.user 