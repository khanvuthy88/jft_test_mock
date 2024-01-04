/** @odoo-module **/

import SurveyFormWidget from '@survey/js/survey_form';
import { browser } from "@web/core/browser/browser";

SurveyFormWidget.include({
    _onNextScreenDone(options) {
        var result = this.nextScreenResult;
        console.log(result);
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
        this._super(...arguments);

        if(result.jft_section_title){
            $('section#jft_sub_title').empty();
            $('section#jft_sub_title').html(result.jft_section_title);
        }
    },
});