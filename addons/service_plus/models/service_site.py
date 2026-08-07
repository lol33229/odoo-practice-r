from odoo import models, fields


class ServiceSite(models.Model):
    _name = 'service.site'
    _description = 'Объект сети (магазин/точка)'
    _order = 'name'

    name = fields.Char(string='Название объекта', required=True,
                        help="Например: Магазин №5, ТЦ «Мега»")
    address = fields.Char(string='Адрес', required=True)
    city = fields.Char(string='Город')
    active = fields.Boolean(string='Активен', default=True)
    order_ids = fields.One2many('service.order', 'site_id', string='Заявки')
    order_count = fields.Integer(string='Кол-во заявок', compute='_compute_order_count')

    def _compute_order_count(self):
        for site in self:
            site.order_count = len(site.order_ids)
