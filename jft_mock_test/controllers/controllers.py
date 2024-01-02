# -*- coding: utf-8 -*-
from odoo import http
from odoo.addons.survey.controllers.main import Survey
from odoo.http import request, content_disposition



class JFTSurvey(Survey):

    def _prepare_survey_data(self, survey_sudo, answer_sudo, **post):
        res = super()._prepare_survey_data(survey_sudo, answer_sudo, **post)

        for key, value in enumerate(survey_sudo.question_and_page_ids):
            print(key, value)
        # print(res)
        return res

    # def _prepare_question_html(self, survey_sudo, answer_sudo, **post):
    #     res = super()._prepare_question_html(survey_sudo, answer_sudo, **post)
    #     print(res)
    #     return res

    @http.route()
    def survey_begin(self, survey_token, answer_token, **post):
        return super().survey_begin(survey_token, answer_token, **post)

