from django.contrib import admin
from .models import Project, Expense, Category


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "project",)


class ExpenseAdmin(admin.ModelAdmin):
    list_display = ("project", "title", "amount", "category",)


class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "budget", "total_transactions", "budget_left")


admin.site.register(Project, ProjectAdmin)
admin.site.register(Expense, ExpenseAdmin)
admin.site.register(Category, CategoryAdmin)
