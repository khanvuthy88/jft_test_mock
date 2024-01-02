# -*- coding: utf-8 -*-
from odoo import http
from odoo.addons.survey.controllers.main import Survey
from odoo.http import request, content_disposition


class JFTSurvey(Survey):

    def _prepare_question_html(self, survey_sudo, answer_sudo, **post):
        res = super()._prepare_question_html(survey_sudo, answer_sudo, **post)
        survey_data = self._prepare_survey_data(survey_sudo, answer_sudo, **post)
        jft_section_title = request.env['ir.qweb']._render('jft_mock_test.jft_survey_section_title', survey_data)
        res['jft_section_title'] = jft_section_title
        return res

    def _prepare_survey_data(self, survey_sudo, answer_sudo, **post):
        res = super()._prepare_survey_data(survey_sudo, answer_sudo, **post)
        jft_section_question = {}
        section_title = ''
        if 'question' in res:
            section_title = res['question'].title
        for section in survey_sudo.page_ids:
            jft_section_name = section.title
            if section.title not in jft_section_question:
                jft_section_question[jft_section_name] = []
            for question in section.question_ids:
                jft_section_question[jft_section_name].append({
                    'active': question.id == 'question' in res and res['question'].id,
                    'title': question.title,
                    'id': question.id,
                    'section': section.title
                })
                if 'question' in res and question.title == res['question'].title:
                    section_title = section.title
        res['jft_section'] = jft_section_question
        res['jft_section_title'] = section_title

        return res

    @http.route()
    def survey_begin(self, survey_token, answer_token, **post):
        return super().survey_begin(survey_token, answer_token, **post)
