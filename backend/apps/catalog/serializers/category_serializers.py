from rest_framework import serializers
from ..models import Category

class CategorySerializer(serializers.ModelSerializer):
    """
    Сериализатор для категории
    """
    parent_name = serializers.CharField(source='parent.name', read_only=True)
    children = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'parent', 'parent_name', 'children']

    def get_children(self, obj):
        """
        Возвращает список дочерних категорий
        """
        children = obj.children.all()
        if children:
            return CategorySerializer(children, many=True, read_only=True).data
        return []