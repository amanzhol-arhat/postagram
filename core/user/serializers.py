from .models import User
from core.abstract import AbstractSerializer

class UserSerializer(AbstractSerializer):

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'is_active',
            'is_superuser',
            'created_at',
            'updated_at',
            'bio',
        ]
        read_only_fields = ['is_active', 'is_superuser']
