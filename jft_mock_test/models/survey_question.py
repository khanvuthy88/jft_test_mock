# -*- coding: utf-8  -*-

from odoo import fields, models, api, _


class SurveyQuestion(models.Model):
    _inherit = "survey.question"

    skip_question = fields.Boolean()


