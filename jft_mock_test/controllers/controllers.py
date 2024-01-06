# -*- coding: utf-8 -*-

from itertools import takewhile
from odoo import http
from odoo.addons.survey.controllers.main import Survey
from odoo.http import request, content_disposition

SESSION_LIFETIME = 60 * 60 * 2


class JFTSurvey(Survey):

    def _prepare_question_html(self, survey_sudo, answer_sudo, **post):
        """
        Prepare HTML content for survey questions.

        This method enhances the HTML content for survey questions by integrating
        additional data such as section titles and aside information. It utilizes
        the provided survey_sudo, answer_sudo, and additional post parameters to
        create a structured response.

        Args:
            survey_sudo (recordset): Survey record.
            answer_sudo (recordset): Survey answer record.
            **post: Additional parameters from the HTTP request.

        Returns:
            dict: A dictionary containing the prepared HTML content with added
                  details about section titles and aside information.
        """

        res = super()._prepare_question_html(survey_sudo, answer_sudo, **post)
        survey_data = self._prepare_survey_data(survey_sudo, answer_sudo, **post)

        jft_section_title = request.env['ir.qweb']._render('jft_mock_test.jft_survey_section_title', survey_data)
        jft_section_aside = request.env['ir.qweb']._render('jft_mock_test.jft_survey_aside', survey_data)
        jft_survey_navigation = request.env['ir.qweb']._render('jft_mock_test.jft_survey_navigation', survey_data)
        jft_survey_header_left = request.env['ir.qweb']._render('jft_mock_test.jft_survey_left_header', survey_data)
        jft_survey_header_right = request.env['ir.qweb']._render('jft_mock_test.jft_survey_header_right', survey_data)

        res['jft_section_title'] = jft_section_title
        res['jft_section_aside'] = jft_section_aside
        res['jft_survey_navigation'] = jft_survey_navigation
        res['jft_survey_header_left'] = jft_survey_header_left
        res['jft_survey_header_right'] = jft_survey_header_right

        return res

    def _set_default_active_session_cookie(self):
        request_cookies = request.httprequest.cookies.get('active_session_id', '0')
        if not request_cookies:
            request.future_response.set_cookie('active_session_id', '0', max_age=SESSION_LIFETIME)

    def _update_active_session_cookie(self, question_id):
        request.future_response.set_cookie('active_session_id', str(question_id), max_age=SESSION_LIFETIME)

    def _update_survey_data(self, res, intro_dict):
        if 'breadcrumb_pages' in res:
            res['breadcrumb_pages'].insert(0, intro_dict)

    def _prepare_intro_dict(self):
        return {'id': 0, 'title': 'Introduction'}

    def _question_index_by_page(self, question_id, page_question_ids):
        reset_index = 1
        for question in page_question_ids:
            if question.is_page:
                reset_index = 0
            if question.id == question_id:
                return reset_index
            if not question.is_page:
                reset_index += 1
        return 0

    def _prepare_survey_data(self, survey_sudo, answer_sudo, **post):
        res = super()._prepare_survey_data(survey_sudo, answer_sudo, **post)
        jft_section_question = {}
        section_title = ''

        self._set_default_active_session_cookie()

        if 'active_session_id' not in res:
            res['active_session_id'] = '0'
        if 'question' in res:
            if res['question'].is_page:
                section_title = res['question'].title
            else:
                section_title = res['question'].page_id.title
            self._update_active_session_cookie(res['question'].page_id.id)

            res['question_index'] = self._question_index_by_page(res['question'].id,
                                                                 res['question'].page_id.question_ids)
        else:
            res['question_index'] = 0

        intro_dict = self._prepare_intro_dict()
        self._update_survey_data(res, intro_dict)
        active_session = request.httprequest.cookies.get('active_session_id')
        res['active_session_id'] = int(active_session) if active_session and active_session != 'False' else 0

        res['jft_section'] = jft_section_question
        res['jft_section_title'] = section_title
        return res

    @http.route()
    def survey_display_page(self, survey_token, answer_token, **post):
        access_data = self._get_access_data(survey_token, answer_token, ensure_token=True)
        answer_sudo = access_data['answer_sudo']
        if answer_sudo.state == 'new':
            request.future_response.set_cookie('active_session_id', '0', max_age=SESSION_LIFETIME)
        res = super().survey_display_page(survey_token, answer_token, **post)
        return res

    @http.route()
    def survey_begin(self, survey_token, answer_token, **post):
        res = super().survey_begin(survey_token, answer_token, **post)
        return res

    @http.route()
    def survey_next_question(self, survey_token, answer_token, **post):
        res = super().survey_next_question(survey_token, answer_token, **post)
        return res

    @http.route()
    def survey_submit(self, survey_token, answer_token, **post):
        res = super().survey_submit(survey_token, answer_token, **post)
        return res
