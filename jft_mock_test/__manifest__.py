# -*- coding: utf-8 -*-
{
    'name': "JFT Mock Test",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['survey'],

    'assets': {
        'survey.survey_assets': [
            'jft_mock_test/static/src/scss/style.scss',
            'jft_mock_test/static/src/js/survey_form.js'
        ]
    },

    # always loaded
    'data': [
        'views/survey_survey_templates.xml',
    ],
}

