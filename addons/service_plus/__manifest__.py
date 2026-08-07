{
    'name': 'Сервис+ — Каталог исполнителей',
    'version': '19.0.1.0.0',
    'summary': 'Каталог мастеров (сантехник, электрик, сварщик, уборка снега) с рейтингом, отзывами и фильтрами',
    'description': """
Сервис+ (US №1: Поиск исполнителя)
===================================
Реализует user story директора магазина: быстрый поиск квалифицированного
мастера в каталоге, с рейтингом и отзывами, фильтрами по цене, географии
(расстояние до магазина) и срочности выполнения.
""",
    'category': 'Services',
    'author': 'Учебный проект',
    'license': 'LGPL-3',
    'depends': ['base', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/service_category_views.xml',
        'views/service_site_views.xml',
        'views/service_provider_views.xml',
        'views/service_review_views.xml',
        'views/service_order_views.xml',
        'views/service_order_response_wizard_views.xml',
        'views/service_menu_views.xml',
    ],
    'application': True,
    'installable': True,
} # type: ignore
