from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ServiceReview(models.Model):
    _name = 'service.review'
    _description = 'Отзыв об исполнителе'
    _order = 'create_date desc'

    provider_id = fields.Many2one(
        'service.provider', string='Исполнитель', required=True, ondelete='cascade'
    )
    author_id = fields.Many2one(
        'res.partner', string='Автор отзыва (заказчик)'
    )
    rating = fields.Selection(
        [('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')],
        string='Оценка',
        required=True,
    )
    comment = fields.Text(string='Комментарий')

    # rating хранится как Selection (строка), но для расчёта среднего
    # в service.provider удобнее работать с числом — приводим через related-поле
    rating_value = fields.Integer(
        string='Оценка (число)', compute='_compute_rating_value', store=True
    )

    @api.depends('rating')
    def _compute_rating_value(self):
        for review in self:
            review.rating_value = int(review.rating) if review.rating else 0
