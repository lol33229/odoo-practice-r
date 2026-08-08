from odoo import models, fields


class ServiceOrderResponseWizard(models.TransientModel):
    _name = 'service.order.response.wizard'
    _description = 'Мастер отклика на заказ'

    order_id = fields.Many2one('service.order', string='Заявка', required=True)
    provider_id = fields.Many2one(
        'service.provider', string='Вы откликаетесь как исполнитель',
        required=True,
    )
    message = fields.Text(string='Сообщение заказчику')
    proposed_price = fields.Float(string='Ваша цена, ₽')
    eta = fields.Datetime(string='Когда сможете прибыть на объект')

    def action_submit(self):
        self.ensure_one()
        self.env['service.order.response'].create({
            'order_id': self.order_id.id,
            'provider_id': self.provider_id.id,
            'message': self.message,
            'proposed_price': self.proposed_price,
            'eta': self.eta,
        })
        return {'type': 'ir.actions.act_window_close'}
