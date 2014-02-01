# -*coding: utf-8-*-

from . import ResourcesQueryBuilder
from ...models.resource import Resource
from ...models.employee import Employee


class EmployeesQueryBuilder(ResourcesQueryBuilder):
    _fields = {
        'id': Employee.id,
        '_id': Employee.id,
        'first_name': Employee.first_name,
        'last_name': Employee.last_name,
    }

    def __init__(self):
        super(EmployeesQueryBuilder, self).__init__()
        fields = ResourcesQueryBuilder.get_fields_with_labels(
            self.get_fields()
        )
        self.query = self.query.join(Employee, Resource.employee)
        self.query = self.query.add_columns(*fields)
