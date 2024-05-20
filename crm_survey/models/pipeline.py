from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import werkzeug

class Pipeline(models.Model):
    _inherit = 'crm.lead'

    survey_history_ids = fields.One2many('pipeline.survey.history', 'pipeline_id', string='Survey History')

class PipelineSurveyHistory(models.Model):
    _name = 'pipeline.survey.history'
    _description = 'Pipeline Survey History'
    
    pipeline_id = fields.Many2one('crm.lead', string='Pipeline', ondelete='cascade')
    survey_id = fields.Many2one('survey.survey', string='Survey', required=True)
    survey_answer_id = fields.Many2one('survey.user_input', string='Answer')

    answer_duration_avg = fields.Float(string='Average Answer Duration', related='survey_id.answer_duration_avg', store=True)
    answer_count = fields.Integer(string='Total Answers', related='survey_id.answer_count', store=True)
    answer_done_count = fields.Integer(string='Completed Answers', related='survey_id.answer_done_count', store=True)
    
    def action_start_survey(self):
        return self.survey_id.action_send_survey()

    def open_answers(self):
        action = self.survey_id.action_survey_user_input_completed()
        # Update the domain to filter survey answers based on the email_from field of the related crm.lead
        leads = self.env['crm.lead'].search([('id', '=', self.pipeline_id.id)])
        if leads:
            email_from = leads[0].email_from
            # Search for survey.user_input.line where value_char_box matches email_from
            user_input_lines = self.env['survey.user_input.line'].search([('value_char_box', 'ilike', email_from)])
            user_input_ids_from_lines = user_input_lines.mapped('user_input_id').ids
            # Search for survey.user_input where email matches email_from
            user_inputs = self.env['survey.user_input'].search([('email', 'ilike', email_from)])
            user_input_ids_from_inputs = user_inputs.ids
            # Combine both sets of user_input_ids
            combined_user_input_ids = list(set(user_input_ids_from_lines + user_input_ids_from_inputs))
            action['domain'] = [('id', 'in', combined_user_input_ids)]
        return action

    def send_survey_to_customer(self):
        if not self.pipeline_id.partner_id:
            raise ValidationError(_('''Select Customer into Ticket'''))
        template_id = self.env.ref('crm_survey.template_start_survey_crm_survey')
        if template_id and self.pipeline_id and self.pipeline_id.email_from:
            email_from = self.env.user.company_id.email if self.env.user and self.env.user.company_id else ''
            email_to = self.pipeline_id.email_from
            survey_title = self.survey_id.title if self.survey_id else 'Survey'
            template_id.email_from = email_from
            template_id.email_to = email_to
            template_id.send_mail(self.id, force_send=True)
            
            # Prepare the email content for the chatter
            email_subject = template_id.subject
            email_body = template_id.body_html
            
            # Add message to the chatter indicating the email has been sent
            self.pipeline_id.message_post(
                body=_("Survey '%s' has been sent to %s" % (survey_title, email_to)),
                subject=_("Survey Email Sent"),
                message_type='comment',
                subtype_xmlid='mail.mt_comment',
            )

    def get_survey_url(self):
        survey_url = werkzeug.urls.url_join(self.survey_id.get_base_url(), self.survey_id.get_start_url()) if self.survey_id else False
        return survey_url

class SurveyUserInputLine(models.Model):
    _inherit = 'survey.user_input.line'

    value_char_box = fields.Char(string='Value Char Box')

