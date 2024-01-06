/** @odoo-module **/

import SurveyFormWidget from '@survey/js/survey_form';
import { browser } from "@web/core/browser/browser";

SurveyFormWidget.include({
    start() {

        var self = this;
        return this._super.apply(this, arguments).then(function () {
            self.$jftSurveyNavigation = $('.jft_survey_footer');
            self.$jftSurveyHeaderLeft = $('.jft_survey_left_header');
            self.$jftSurveyHeaderRight = $('.jft_survey_header_question_section');
        });
    },
    _onNextScreenDone(options) {
        var self = this;
        
        this._super(...arguments);
        var result = this.nextScreenResult;
        const active_breadcrumb = browser.localStorage.getItem('active_breadcrumb');
        
        if(active_breadcrumb == 0 && result.active_session_id){
            browser.localStorage.setItem('active_breadcrumb', result.active_session_id);
        }else{
            browser.localStorage.setItem('active_breadcrumb', 0);
        }
        if(result.jft_section_aside){
            $('.jft_survey_aside').empty();
            $('.jft_survey_aside').html(result.jft_section_aside);
        }        

        if(result.jft_section_title){
            $('section#jft_sub_title').empty();
            $('section#jft_sub_title').html(result.jft_section_title);
        }
        if(result.jft_survey_navigation && this.$jftSurveyNavigation.length !== 0){
            $('.jft_survey_footer').html(result.jft_survey_navigation);
            this.$jftSurveyNavigation.find('.jft_survey_navigation_submit').on('click', self._onSubmit.bind(self));
        }
        if(result.jft_survey_header_left && this.$jftSurveyHeaderLeft.length !== 0){
            $('.jft_survey_left_header').html(result.jft_survey_header_left);
        }
        if(result.jft_survey_header_right && this.$jftSurveyHeaderRight.length !== 0){
            $('.jft_survey_header_question_section').html(result.jft_survey_header_right);
        }
    },
});