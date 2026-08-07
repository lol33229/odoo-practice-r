

## 1. Что нового в модуле

```
service.site          — объект сети (магазин): название, город, адрес
service.order          — доработана:
    + site_id           (Many2one → service.site)
    + attachment_ids     (Many2many → ir.attachment, фото/видео)
    + state: добавлен статус 'draft' (Черновик), теперь он стартовый
    + action_publish()   — валидация обязательных полей + перевод в 'new'
```
