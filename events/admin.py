from django.contrib import admin
from events.models import Event, EventExpense


class EventExpenseAdmin(admin.ModelAdmin):
    list_display = [
        "event_name",
        "target",
        "value",
        "related_date",
        "paid_by",
        "comment",
    ]
    ordering = ["-pk"]

    def related_date(self, obj):
        return obj.expense.related_date

    def value(self, obj):
        return obj.expense.value

    def target(self, obj):
        return obj.expense.target

    def paid_by(self, obj):
        return obj.expense.paid_by

    def comment(self, obj):
        return obj.expense.comment

    def event_name(self, obj):
        return obj.event.name


admin.site.register(Event)
admin.site.register(EventExpense, EventExpenseAdmin)
