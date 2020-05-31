from django.apps import apps
from django.contrib import admin
from django.contrib.admin.sites import AlreadyRegistered
from import_export import widgets, resources
from .models import *
from import_export.admin import ImportExportModelAdmin


class NameForeignKeyWidget(widgets.ForeignKeyWidget):
    def clean(self, value, row=None, *args, **kwargs):
        return self.model.objects.get_or_create(name=value)[0] if value else None


#    RESOURCES    #


class CityResource(resources.ModelResource):

    class Meta:
        model = City
        import_id_fields = ('name',)
        exclude = ('id',)


class CountryResource(resources.ModelResource):

    class Meta:
        model = Country
        import_id_fields = ('name',)
        exclude = ('id',)


class WorkTypeResource(resources.ModelResource):

    class Meta:
        model = WorkType
        import_id_fields = ('name',)
        exclude = ('id',)


class AuthorResource(resources.ModelResource):

    class Meta:
        model = Author
        import_id_fields = ('surname', 'name', 'patronymic')
        exclude = ('id', 'works')


class OwnerResource(resources.ModelResource):

    class Meta:
        model = Owner
        import_id_fields = ('name',)
        exclude = ('id',)

class WorkAuthorshipResource(resources.ModelResource):

    class Meta:
        model = WorkAuthorship
        import_id_fields = ('work', 'author')
        exclude = ('id',)


class CollectionWorkResource(resources.ModelResource):

    class Meta:
        model = CollectionWork
        import_id_fields = ('title',)
        exclude = ('genericwork_ptr', 'authors', 'id', 'polymorphic_ctype')


class IndependentWorkResource(resources.ModelResource):

    class Meta:
        model = IndependentWork
        import_id_fields = ('title',)
        exclude = ('genericwork_ptr', 'authors', 'id', 'polymorphic_ctype')

class PatentResource(resources.ModelResource):

    class Meta:
        model = Patent
        import_id_fields = ('title',)
        exclude = ('genericwork_ptr', 'authors', 'id', 'polymorphic_ctype')

class CollectionResource(resources.ModelResource):

    class Meta:
        model = Collection
        import_id_fields = ('title',)
        exclude = ('id',)


class CollectionIssueResource(resources.ModelResource):

    class Meta:
        model = CollectionIssue
        import_id_fields = ('collection', 'year', 'issue')
        exclude = ('id')


class PublisherResource(resources.ModelResource):

    class Meta:
        model = Publisher
        import_id_fields = ('name',)
        exclude = ('id',)


#    ADMIN INTERFACES    #

class CityAdmin(ImportExportModelAdmin):
    resource_class = CityResource


class CountryAdmin(ImportExportModelAdmin):
    resource_class = CountryResource


class WorkTypeAdmin(ImportExportModelAdmin):
    resource_class = WorkTypeResource


class AuthorAdmin(ImportExportModelAdmin):
    resource_class = AuthorResource
    list_display = ('surname', 'name', 'patronymic')


class OwnerAdmin(ImportExportModelAdmin):
    resource_class = OwnerResource


class WorkAuthorshipAdmin(ImportExportModelAdmin):
    resource_class = WorkAuthorshipResource
    list_display = ('author', 'work', 'pages_authored')


class CollectionWorkAdmin(ImportExportModelAdmin):
    resource_class = CollectionWorkResource
    list_display = ('title', 'work_type',
                    'collection_issue', 'pages_number', 'pages_from')


class IndependentWorkAdmin(ImportExportModelAdmin):
    resource_class = IndependentWorkResource
    list_display = ('title', 'work_type',
                    'year', 'publisher', 'pages_number')


class PatentAdmin(ImportExportModelAdmin):
    resource_class = PatentResource
    list_display = ('title', 'work_type', 'patent_code', 'country', 'ipc',
                    'owner', 'patent_number', 'issue_date', 'publication_date', 'bulletin_number')


class CollectionAdmin(ImportExportModelAdmin):
    resource_class = CollectionResource
    list_display = ('title', 'serie', 'description', 'editorship', 'publisher')


class CollectionIssueAdmin(ImportExportModelAdmin):
    resource_class = CollectionIssueResource
    list_display = ('collection', 'year', 'issue')


class PublisherAdmin(ImportExportModelAdmin):
    resource_class = PublisherResource
    list_display = ('name', 'city')


admin.site.register(City, CityAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(WorkType, WorkTypeAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Owner, OwnerAdmin)
admin.site.register(WorkAuthorship, WorkAuthorshipAdmin)
admin.site.register(CollectionWork, CollectionWorkAdmin)
admin.site.register(IndependentWork, IndependentWorkAdmin)
admin.site.register(Patent, PatentAdmin)
admin.site.register(Collection, CollectionAdmin)
admin.site.register(CollectionIssue, CollectionIssueAdmin)
admin.site.register(Publisher, PublisherAdmin)
