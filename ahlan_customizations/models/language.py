from openerp import models, fields


class Language(models.Model):
    _name = 'language'

    applicant = fields.Many2one('hr.applicant', required=True)
    name = fields.Char('Language', required=True)