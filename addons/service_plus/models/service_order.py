from odoo import models, fields, api
from odoo.exceptions import UserError


class ServiceOrder(models.Model):
    _name = 'service.order'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Заявка на услугу'
    _order = 'create_date desc'
    _rec_name = 'address'

    # --- Основное ---
    site_id = fields.Many2one(
        'service.site', string='Объект (магазин)',
        help="Точка сети, на которой возникла проблема",
    )
    category_id = fields.Many2one(
        'service.category', string='Вид работ', required=True
    )
    description = fields.Text(string='Описание проблемы')
    address = fields.Char(string='Адрес объекта', required=True)
    photo_ids = fields.One2many(
        'service.order.photo', 'order_id', string='Фотографии'
    )
    attachment_ids = fields.Many2many(
        'ir.attachment', string='Фото / видео проблемы',
        help="Можно прикрепить любые файлы: фотографии, видео и т.д.",
    )

    # --- Критерии для фильтров исполнителя (US1 "Получение заказов") ---
    price_offered = fields.Float(string='Бюджет заказчика, ₽')
    distance_km = fields.Float(string='Расстояние до объекта, км')

    # --- Заказчик и статус ---
    partner_id = fields.Many2one(
        'res.partner', string='Заказчик',
        default=lambda self: self.env.user.partner_id,
    )
    # Детальные статусы выполнения работ (US2 "Контроль выполнения работ")
    state = fields.Selection(
        [
            ('draft', 'Черновик'),
            ('new', 'Новая'),
            ('assigned', 'Исполнитель назначен'),
            ('en_route', 'Исполнитель в пути'),
            ('in_progress', 'Работы выполняются'),
            ('done', 'Выполнена'),
            ('cancelled', 'Отменена'),
        ],
        string='Статус', default='draft', required=True, tracking=True,
    )
    assigned_provider_id = fields.Many2one(
        'service.provider', string='Назначенный исполнитель', readonly=True,
        tracking=True,
    )
    arrival_eta = fields.Datetime(
        string='Ожидаемое время прибытия исполнителя', readonly=True,
        tracking=True,
    )

    # --- Отклики мастеров ---
    response_ids = fields.One2many(
        'service.order.response', 'order_id', string='Отклики'
    )
    response_count = fields.Integer(
        string='Кол-во откликов', compute='_compute_response_count'
    )

    @api.depends('response_ids')
    def _compute_response_count(self):
        for order in self:
            order.response_count = len(order.response_ids)

    @api.onchange('site_id')
    def _onchange_site_id(self):
        """При выборе объекта сети сразу подставляем его адрес."""
        for order in self:
            if order.site_id:
                order.address = order.site_id.address

    # --- Действия ---
    def action_publish(self):
        """Кнопка «Опубликовать» — доступна только когда заполнены
        обязательные для публикации поля (категория, адрес, описание).
        Заявка становится видимой в каталоге исполнителей."""
        for order in self:
            missing = []
            if not order.category_id:
                missing.append('Категория услуги')
            if not order.address:
                missing.append('Адрес объекта')
            if not order.description:
                missing.append('Описание проблемы')
            if missing:
                raise UserError(
                    'Перед публикацией заполните обязательные поля:\n- '
                    + '\n- '.join(missing)
                )
            order.state = 'new'
            order.message_post(body='Заявка опубликована и доступна исполнителям.')

    def action_open_respond_wizard(self):
        """Кнопка «Откликнуться» — открывает мастер выбора исполнителя."""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Откликнуться на заказ',
            'res_model': 'service.order.response.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_order_id': self.id},
        }

    def action_start_travel(self):
        """Исполнитель отметил, что выехал на объект."""
        for order in self:
            order.state = 'en_route'
            order.message_post(body='Исполнитель выехал на объект.')

    def action_start_work(self):
        """Исполнитель отметил начало работ на месте."""
        for order in self:
            order.state = 'in_progress'
            order.message_post(body='Исполнитель приступил к работам на объекте.')

    def action_cancel(self):
        for order in self:
            order.state = 'cancelled'
            order.message_post(body='Заявка отменена.')

    def action_done(self):
        for order in self:
            order.state = 'done'
            order.message_post(body='Работы по заявке завершены.')
