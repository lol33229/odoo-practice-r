from odoo import models, fields


class ServiceCategory(models.Model):
    _name = 'service.category'
    _description = 'Категория услуги (Сантехник, Электрик, Сварщик, Уборка снега и т.д.)'
    _order = 'sequence, name'

    name = fields.Char(string='Название категории', required=True)
    sequence = fields.Integer(string='Порядок', default=10)
    icon = fields.Char(
        string='Иконка (Font Awesome класс)',
        help="Например: fa-wrench, fa-bolt, fa-fire, fa-snowflake-o",
        default='fa-wrench',
    )
    provider_ids = fields.One2many(
        'service.provider', 'category_id', string='Исполнители'
    )
    provider_count = fields.Integer(
        string='Кол-во исполнителей', compute='_compute_provider_count'
    )

    def _compute_provider_count(self):
        for category in self:
            category.provider_count = len(category.provider_ids)
