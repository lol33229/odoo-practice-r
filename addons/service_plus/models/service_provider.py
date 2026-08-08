from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ServiceProvider(models.Model):
    _name = 'service.provider'
    _description = 'Исполнитель услуги (мастер)'
    _order = 'rating desc, name'

    # --- Основная информация ---
    name = fields.Char(string='Имя / название мастера', required=True)
    partner_id = fields.Many2one(
        'res.partner', string='Контакт (для чата и уведомлений)',
        help="Партнёр Odoo, привязанный к мастеру — на него приходят "
             "уведомления и через него можно писать в чат заявки",
    )
    category_id = fields.Many2one(
        'service.category', string='Категория услуги', required=True
    )
    phone = fields.Char(string='Телефон')
    description = fields.Text(string='Описание / специализация')
    active = fields.Boolean(string='Активен', default=True)
    photo = fields.Image(string='Фото', max_width=256, max_height=256)

    # --- Критерий: ориентировочная стоимость ---
    price_from = fields.Float(string='Цена от, ₽', default=0.0)
    price_to = fields.Float(string='Цена до, ₽', default=0.0)

    # --- Критерий: география (близость к магазину) ---
    distance_km = fields.Float(
        string='Расстояние до магазина, км',
        help="Ориентировочное расстояние от точки магазина до мастера",
    )
    district = fields.Char(string='Район / город')

    # --- Критерий: срочность ---
    urgency = fields.Selection(
        [
            ('urgent', 'Срочно (сегодня/в течение часа)'),
            ('standard', 'В течение 2-3 дней'),
            ('scheduled', 'По предварительной записи'),
        ],
        string='Доступная срочность',
        default='standard',
        required=True,
    )

    # --- Рейтинг и отзывы ---
    review_ids = fields.One2many(
        'service.review', 'provider_id', string='Отзывы'
    )
    rating = fields.Float(
        string='Рейтинг',
        compute='_compute_rating',
        store=True,
        digits=(3, 2),
        help="Средняя оценка по всем отзывам (от 1 до 5)",
    )
    review_count = fields.Integer(
        string='Количество отзывов', compute='_compute_rating', store=True
    )

    @api.depends('review_ids.rating_value')
    def _compute_rating(self):
        for provider in self:
            reviews = provider.review_ids
            provider.review_count = len(reviews)
            if reviews:
                provider.rating = sum(reviews.mapped('rating_value')) / len(reviews)
            else:
                provider.rating = 0.0

    @api.constrains('price_from', 'price_to')
    def _check_price_range(self):
        for provider in self:
            if provider.price_from < 0 or provider.price_to < 0:
                raise ValidationError('Цена не может быть отрицательной.')
            if provider.price_to and provider.price_from > provider.price_to:
                raise ValidationError(
                    'Цена "от" не может быть больше цены "до".'
                )

    @api.constrains('distance_km')
    def _check_distance(self):
        for provider in self:
            if provider.distance_km < 0:
                raise ValidationError('Расстояние не может быть отрицательным.')
