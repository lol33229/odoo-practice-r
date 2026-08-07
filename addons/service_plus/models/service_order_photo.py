from odoo import models, fields


class ServiceOrderPhoto(models.Model):
    _name = 'service.order.photo'
    _description = 'Фотография к заявке'
    _order = 'id'

    order_id = fields.Many2one(
        'service.order', string='Заявка', required=True, ondelete='cascade'
    )
    image = fields.Image(string='Фото', max_width=1024, max_height=1024)
