from odoo import models, fields
from odoo.exceptions import UserError


class ServiceOrderResponse(models.Model):
    _name = 'service.order.response'
    _description = 'Отклик исполнителя на заказ'
    _order = 'create_date desc'

    order_id = fields.Many2one(
        'service.order', string='Заявка', required=True, ondelete='cascade'
    )
    provider_id = fields.Many2one(
        'service.provider', string='Исполнитель', required=True
    )
    message = fields.Text(string='Сообщение заказчику')
    proposed_price = fields.Float(string='Предложенная цена, ₽')
    eta = fields.Datetime(string='Предполагаемое время прибытия')
    state = fields.Selection(
        [
            ('sent', 'Отправлен'),
            ('accepted', 'Принят'),
            ('rejected', 'Отклонён'),
        ],
        string='Статус', default='sent', required=True,
    )

    def action_accept(self):
        for response in self:
            if response.order_id.state != 'new':
                raise UserError('Эта заявка уже не в статусе "Новая".')
            response.state = 'accepted'
            order = response.order_id
            order.write({
                'state': 'assigned',
                'assigned_provider_id': response.provider_id.id,
                'arrival_eta': response.eta,
            })
            # подписываем контакт исполнителя на заявку — он увидит
            # уведомления и сможет отвечать в чате (chatter) заявки
            if response.provider_id.partner_id:
                order.message_subscribe(
                    partner_ids=[response.provider_id.partner_id.id]
                )
            order.message_post(
                body=(
                    f"Исполнитель назначен: {response.provider_id.name}. "
                    f"Ожидаемое время прибытия: "
                    f"{response.eta or 'не указано'}"
                )
            )
            # остальные отклики по этой же заявке автоматически отклоняем
            (order.response_ids - response).write({'state': 'rejected'})

    def action_reject(self):
        for response in self:
            response.state = 'rejected'
