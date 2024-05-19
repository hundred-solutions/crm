from odoo import models, fields, api, _

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
    
    def action_send_survey(self):
        return self.survey_id.action_send_survey()

    def open_answers(self):
        action = self.survey_id.action_survey_user_input_completed()
        # Update the domain to filter survey answers based on the email_from field of the related crm.lead
        leads = self.env['crm.lead'].search([('id', '=', self.pipeline_id.id)])
        if leads:
            email_from = leads[0].email_from
            user_input_lines = self.env['survey.user_input.line'].search([('value_char_box', 'ilike', email_from)])
            user_input_ids = user_input_lines.mapped('user_input_id').ids
            action['domain'] = [('id', 'in', user_input_ids)]
        return action

class SurveyUserInputLine(models.Model):
    _inherit = 'survey.user_input.line'

    value_char_box = fields.Char(string='Value Char Box')

