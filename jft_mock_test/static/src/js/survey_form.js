/** @odoo-module **/

import SurveyFormWidget from '@survey/js/survey_form';

SurveyFormWidget.include({
    _onNextScreenDone(options) {
        this._super(...arguments);
        var result = this.nextScreenResult;
        if(result.jft_section_title){
            $('section#jft_sub_title').empty();
            $('section#jft_sub_title').html(result.jft_section_title);
        }
    },
});