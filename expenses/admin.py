from django.contrib import admin

from expenses.models import ExpenseType, Expense


class ExpenseTypeAdmin(admin.ModelAdmin):
    list_display = ["__str__", "position"]
    search_fields = ["name"]
    ordering = ["parent", "-position"]


class ExpenseAdmin(admin.ModelAdmin):
    list_display = ["related_date", "value", "target", "paid_by", "comment"]
    ordering = ["-pk"]


admin.site.register(ExpenseType, ExpenseTypeAdmin)
admin.site.register(Expense, ExpenseAdmin)
