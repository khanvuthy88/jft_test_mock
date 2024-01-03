/** @odoo-module **/

import SurveyFormWidget from '@survey/js/survey_form';

SurveyFormWidget.include({
    _onNextScreenDone(options) {
        var result = this.nextScreenResult;
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