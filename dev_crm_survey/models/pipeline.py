# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 DevIntelle Consulting Service Pvt.Ltd (<http://www.devintellecs.com>).
#
#    For Module Support : devintelle@gmail.com  or Skype : devintelle
#
##############################################################################

from odoo import models, fields, api, _

class Pipeline(models.Model):
    _inherit = 'crm.lead'
    
    @api.onchange('survey_template_id')
    def onchange_survey_template_id(self):
        if self.survey_template_id:
#           print("hiiii---",self.survey_template_id)
            data = []
            self.survey_history_ids = [(6, 0, [])]
            print("self.survey_history_ids======",self.survey_history_ids)
            if self.survey_template_id and self.survey_template_id.survey_ids:
                for line in self.survey_template_id.survey_ids:
                    data.append((0, 0, {'survey_id': line.id}))
            if data:
                self.survey_history_ids = data
            else:
                self.survey_history_ids = [(6, 0, [])]


    
    survey_template_id=fields.Many2one('crm.survey.template', string='Survey Template')
    survey_history_ids = fields.One2many('pipeline.survey.history', 'pipeline_id', string='Survey History')

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
