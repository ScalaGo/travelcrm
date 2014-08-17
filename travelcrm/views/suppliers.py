# -*-coding: utf-8-*-

import logging
import colander

from pyramid.view import view_config

from ..models import DBSession
from ..models.supplier import Supplier
from ..models.bperson import BPerson
from ..models.bank_detail import BankDetail
from ..lib.qb.suppliers import SuppliersQueryBuilder
from ..lib.utils.common_utils import translate as _
from ..forms.suppliers import SupplierSchema


log = logging.getLogger(__name__)


class Suppliers(object):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @view_config(
        context='..resources.suppliers.Suppliers',
        request_method='GET',
        renderer='travelcrm:templates/suppliers/index.mak',
        permission='view'
    )
    def index(self):
        return {}

    @view_config(
        name='list',
        context='..resources.suppliers.Suppliers',
        xhr='True',
        request_method='POST',
        renderer='json',
        permission='view'
    )
    def list(self):
        qb = SuppliersQueryBuilder(self.context)
        qb.search_simple(
            self.request.params.get('q'),
        )
        qb.advanced_search(
            **self.request.params.mixed()
        )
        id = self.request.params.get('id')
        if id:
            qb.filter_id(id.split(','))
        qb.sort_query(
            self.request.params.get('sort'),
            self.request.params.get('order', 'asc')
        )
        qb.page_query(
            int(self.request.params.get('rows')),
            int(self.request.params.get('page'))
        )
        return {
            'total': qb.get_count(),
            'rows': qb.get_serialized()
        }

    @view_config(
        name='add',
        context='..resources.suppliers.Suppliers',
        request_method='GET',
        renderer='travelcrm:templates/suppliers/form.mak',
        permission='add'
    )
    def add(self):
        return {
            'title': _(u'Add Supplier'),
        }

    @view_config(
        name='add',
        context='..resources.suppliers.Suppliers',
        request_method='POST',
        renderer='json',
        permission='add'
    )
    def _add(self):
        schema = SupplierSchema().bind(request=self.request)
        try:
            controls = schema.deserialize(self.request.params.mixed())
            supplier = Supplier(
                name=controls.get('name'),
                resource=self.context.create_resource()
            )
            for id in controls.get('bperson_id'):
                bperson = BPerson.get(id)
                supplier.bpersons.append(bperson)
            for id in controls.get('bank_detail_id'):
                bank_detail = BankDetail.get(id)
                supplier.banks_details.append(bank_detail)
            DBSession.add(supplier)
            DBSession.flush()
            return {
                'success_message': _(u'Saved'),
                'response': supplier.id
            }
        except colander.Invalid, e:
            return {
                'error_message': _(u'Please, check errors'),
                'errors': e.asdict()
            }

    @view_config(
        name='edit',
        context='..resources.suppliers.Suppliers',
        request_method='GET',
        renderer='travelcrm:templates/suppliers/form.mak',
        permission='edit'
    )
    def edit(self):
        supplier = Supplier.get(self.request.params.get('id'))
        return {
            'item': supplier,
            'title': _(u'Edit Supplier'),
        }

    @view_config(
        name='edit',
        context='..resources.suppliers.Suppliers',
        request_method='POST',
        renderer='json',
        permission='edit'
    )
    def _edit(self):
        schema = SupplierSchema().bind(request=self.request)
        supplier = Supplier.get(self.request.params.get('id'))
        try:
            controls = schema.deserialize(self.request.params.mixed())
            supplier.name = controls.get('name')
            supplier.licences = []
            supplier.bpersons = []
            supplier.banks_details = []
            supplier.commissions = []
            for id in controls.get('bperson_id'):
                bperson = BPerson.get(id)
                supplier.bpersons.append(bperson)
            for id in controls.get('bank_detail_id'):
                bank_detail = BankDetail.get(id)
                supplier.banks_details.append(bank_detail)
            return {
                'success_message': _(u'Saved'),
                'response': supplier.id,
            }
        except colander.Invalid, e:
            return {
                'error_message': _(u'Please, check errors'),
                'errors': e.asdict()
            }

    @view_config(
        name='details',
        context='..resources.suppliers.Suppliers',
        request_method='GET',
        renderer='travelcrm:templates/suppliers/details.mak',
        permission='view'
    )
    def details(self):
        supplier = Supplier.get(self.request.params.get('id'))
        return {
            'item': supplier,
        }

    @view_config(
        name='delete',
        context='..resources.suppliers.Suppliers',
        request_method='GET',
        renderer='travelcrm:templates/suppliers/delete.mak',
        permission='delete'
    )
    def delete(self):
        return {
            'title': _(u'Delete Suppliers'),
            'id': self.request.params.get('id')
        }

    @view_config(
        name='delete',
        context='..resources.suppliers.Suppliers',
        request_method='POST',
        renderer='json',
        permission='delete'
    )
    def _delete(self):
        errors = 0
        for id in self.request.params.getall('id'):
            item = Supplier.get(id)
            if item:
                DBSession.begin_nested()
                try:
                    DBSession.delete(item)
                    DBSession.commit()
                except:
                    errors += 1
                    DBSession.rollback()
        if errors > 0:
            return {
                'error_message': _(
                    u'Some objects could not be delete'
                ),
            }
        return {'success_message': _(u'Deleted')}
