# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 DevIntelle Consulting Service Pvt.Ltd (<http://www.devintellecs.com>).
#
#    For Module Support : devintelle@gmail.com  or Skype : devintelle
#
##############################################################################


from odoo import models, fields, _
from odoo.exceptions import ValidationError
import werkzeug


class PipelineSurveyHistory(models.Model):
    _name = 'pipeline.survey.history'
    _description = 'Pipeline Survey History'
    
    def send_survey_to_customer(self):
        print('hiiiiiii==',self.pipeline_id.partner_id)
        if not self.pipeline_id.partner_id:
            raise ValidationError(_('''Select Customer into Ticket'''))
        template_id = self.env.ref('dev_crm_survey.template_start_survey_dev_crm_survey')
        print("template_id---------",template_id,self.pipeline_id)
        print("hhhhhhhhh==========",self.pipeline_id.email_from)
        if template_id and self.pipeline_id and self.pipeline_id.email_from:
#             print("hi")
            template_id.email_from = self.env.user and self.env.user.company_id and self.env.user.company_id.email or ''
            print("template_id.email_from=======",template_id.email_from)
            template_id.email_to = self.pipeline_id.email_from
            print("template_id.email_to========",template_id.email_to)
            template_id.send_mail(self.id, force_send=True)

    def start_survey(self):
        partner = self.pipeline_id and self.pipeline_id.partner_id or False
        response = self.survey_id._create_answer(partner=partner)
        self.write({'survey_answer_id': response.id})
        res = self.survey_id.action_start_survey(answer=response)
        res.update({'target': 'new'})
        return res
        
    def get_survey_url(self):
        survey_url = werkzeug.urls.url_join(self.survey_id.get_base_url(), self.survey_id.get_start_url()) if self.survey_id else False
        return survey_url
        print("survey_url=========",survey_url)

    def print_survey(self):
        if self.survey_answer_id:
            res = self.survey_answer_id.sudo().action_print_answers()
            res.update({'target': 'new'})
            return res
        else:
            raise ValidationError(_('''No Answer found for '%s' Survey''') % (self.survey_id.title))

    def _compute_already_answer_survey(self):
        for rec in self:
            answer_given = False
            if rec.survey_answer_id:
                answer_given = True
            rec.already_answer_survey = answer_given

    pipeline_id = fields.Many2one('crm.lead', string='Pipeline', ondelete='cascade') # link
    survey_id = fields.Many2one('survey.survey', string='Survey', required=True)
    survey_answer_id = fields.Many2one('survey.user_input', string='Answer')
    already_answer_survey = fields.Boolean(string='Already Answer Survey', compute='_compute_already_answer_survey')

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
