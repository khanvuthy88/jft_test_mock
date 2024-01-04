# -*- coding: utf-8 -*-
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

    def _prepare_survey_data(self, survey_sudo, answer_sudo, **post):
        """
        Prepare survey data for rendering.

        This method enhances the prepared survey data by including information
        about active sections and their questions. It utilizes the provided
        survey_sudo, answer_sudo, and additional post parameters to create
        a structured response.

        Args:
            survey_sudo (recordset): Survey record.
            answer_sudo (recordset): Survey answer record.
            **post: Additional parameters from the HTTP request.

        Returns:
            dict: A dictionary containing the prepared survey data with added
                  details about sections and questions.
        """
        res = super()._prepare_survey_data(survey_sudo, answer_sudo, **post)

        jft_section_question = {}
        section_title = ''
        actived_section = []

        request_cookies = request.httprequest.cookies.get('active_session_id', '0')
        if not request_cookies:
            request.future_response.set_cookie('active_session_id', '0', max_age=SESSION_LIFETIME)

        if 'active_session_id' not in res:
            res['active_session_id'] = '0'

        if 'question' in res:
            section_title = res['question'].title
            if res['question'].is_page and int(res['active_session_id']) < res['question'].id:
                request.future_response.set_cookie('active_session_id', str(res['question'].id),
                                                   max_age=SESSION_LIFETIME)
        for section in survey_sudo.page_ids:
            jft_section_name = section.title

            if jft_section_name not in actived_section:
                actived_section.append(jft_section_name.title)

            if jft_section_name not in jft_section_question:
                jft_section_question[jft_section_name] = []

            for question in section.question_ids:
                is_active_question = 'question' in res and question.id == res['question'].id
                jft_section_question[jft_section_name].append({
                    'active': is_active_question,
                    'title': question.title,
                    'id': question.id,
                    'section': section.title
                })

                if is_active_question:
                    section_title = section.title
        intro_dict = {'id': 0, 'title': 'Introduction'}
        if 'breadcrumb_pages' in res:
            res['breadcrumb_pages'].insert(0, intro_dict)
        res['active_session_id'] = int(request.httprequest.cookies.get('active_session_id', 0))
        res['jft_section'] = jft_section_question
        res['jft_section_title'] = section_title
        res['active_section'] = actived_section
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
        return super().survey_begin(survey_token, answer_token, **post)

    @http.route()
    def survey_next_question(self, survey_token, answer_token, **post):
        res = super().survey_next_question(survey_token, answer_token, **post)
        print(res)
        return res

    @http.route()
    def survey_submit(self, survey_token, answer_token, **post):
        res = super().survey_submit(survey_token, answer_token, **post)
        return res
