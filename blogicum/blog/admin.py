from django.contrib import admin
from .models import Category, Post, Location

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'pub_date', 'is_published')  # Поля для отображения
    list_filter = ('pub_date', 'author', 'category', 'is_published')  # Фильтры
    search_fields = ('title', 'text')  # Поля для поиска
    def delete_image(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" style="max-width: 100px;"/> <br/><input type="checkbox" name="delete_image" id="delete_image" /> Удалить изображение'
        return "Нет изображения"
    delete_image.allow_tags = True  # Позволяет использовать HTML в выводе

    def save_model(self, request, obj, form, change):
        if 'delete_image' in request.POST and request.POST['delete_image']:
            obj.delete_image()  # Удаляем изображение
        super().save_model(request, obj, form, change)

    

admin.site.register(Category)
admin.site.register(Post, PostAdmin)
admin.site.register(Location)

# Register your models here.
