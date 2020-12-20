from django.contrib import admin

from snowebsvg.models import Collection, GroupSvg, Svg


class GroupSvgInline(admin.TabularInline):
    model = GroupSvg
    extra = 1


class SvgInline(admin.TabularInline):
    model = Svg
    extra = 1


class CollectionAdmin(admin.ModelAdmin):
    inlines = [
        GroupSvgInline
    ]


class GroupSvgAdmin(admin.ModelAdmin):
    inlines = [
        SvgInline
    ]


admin.site.register(Collection, CollectionAdmin)
admin.site.register(GroupSvg, GroupSvgAdmin)
admin.site.register(Svg)
