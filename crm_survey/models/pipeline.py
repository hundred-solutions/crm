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

    user_id = fields.Many2one('res.users', string='User', related='survey_id.user_id', store=True)
    answer_duration_avg = fields.Float(string='Average Answer Duration', related='survey_id.answer_duration_avg', store=True)
    answer_count = fields.Integer(string='Total Answers', related='survey_id.answer_count', store=True)
    answer_done_count = fields.Integer(string='Completed Answers', related='survey_id.answer_done_count', store=True)
    success_count = fields.Integer(string='Success Count', related='survey_id.success_count', store=True)

    def action_send_survey(self):
        return self.survey_id.action_send_survey()

    def open_answers(self):
        action = self.survey_id.action_survey_user_input_completed()
        action['domain'] = [('survey_id', '=', self.survey_id.id)]
        return action
