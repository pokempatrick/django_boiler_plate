from rest_framework import serializers
from authentification.serializer import RegisterSerilizer
from todos.models import Todos


class TodoSerilizer(serializers.ModelSerializer):
    owner = RegisterSerilizer(read_only=True)

    class Meta:
        model = Todos
        fields = ("id", "title", "description",
                  "owner", "created_at", "updated_at", "is_completed")
