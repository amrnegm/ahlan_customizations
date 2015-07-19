from openerp import models, api, fields
from openerp.tools.translate import _


class Applicant(models.Model):
    _inherit = 'hr.applicant'

    address = fields.Char('Address')
    city = fields.Char('City')
    marital_status = fields.Selection([('single', 'Single'), ('married', 'Married')], 'Marital Status')
    academic_degree = fields.Char('Academic Degree')
    current_job = fields.Char('Current Job')
    languages = fields.One2many('language', 'applicant')
    offered_skills = fields.Text('Skills you offer')
    courses = fields.Text('Courses you got')
    da3wa_experience = fields.Text('Experience in Da3wa')
    facebook_url = fields.Char('Facebook URL')
    know_ahlan_how = fields.Char('How do you know Ahlan')
    notes = fields.Text('Notes')

    @api.v7
    def create(self, cr, uid, vals, context):
        context = dict(context or {})
        context['mail_create_nolog'] = True
        if vals.get('department_id') and not context.get('default_department_id'):
            context['default_department_id'] = vals.get('department_id')
        # if vals.get('job_id') or context.get('default_job_id'):
        #     job_id = vals.get('job_id') or context.get('default_job_id')
        #     vals.update(self.onchange_job(cr, uid, [], job_id, context=context)['value'])
        if vals.get('user_id'):
            vals['date_open'] = fields.datetime.now()
        if 'stage_id' in vals:
            vals.update(self.onchange_stage_id(cr, uid, None, vals.get('stage_id'), context=context)['value'])
        obj_id = super(Applicant, self).create(cr, uid, vals, context=context)
        applicant = self.browse(cr, uid, obj_id, context=context)
        if applicant.job_id:
            name = applicant.partner_name if applicant.partner_name else applicant.name
            self.pool['hr.job'].message_post(
                cr, uid, [applicant.job_id.id],
                body=_('New application from %s') % name,
                subtype="hr_recruitment.mt_job_applicant_new", context=context)
        return obj_id

    def onchange_job(self, cr, uid, ids, job_id=False, context=None):
        return {'value': {}}
        # department_id = False
        # user_id = False
        # if job_id:
        #     job_record = self.pool.get('hr.job').browse(cr, uid, job_id, context=context)
        #     department_id = job_record and job_record.department_id and job_record.department_id.id or False
        #     user_id = job_record and job_record.user_id and job_record.user_id.id or False
        # return {'value': {'department_id': department_id, 'user_id': user_id}}


class CRMLead(models.Model):
    _inherit = 'crm.lead'

    SOCIAL_MEDIA = [
        ('facebook', 'Facebook'),
        ('twitter', 'Twitter'),
        ('interpals', 'Interpals'),
        ('any_talk', 'AnyTalk'),
        ('i_talki', 'Italki'),
        ('youtube', 'Youtube')
    ]

    PAGE_TYPES = [
        ('page', 'Page'),
        ('group', 'Group'),
        ('hashtag', 'Hashtag'),
        ('twitter', 'Twitter'),
    ]

    SUBJECTS = [
        ('christianity', 'Christianity'),
        ('atheism', 'Atheism'),
        ('food', 'Food'),
        ('fastion', 'Fashion'),
        ('anger_management', 'Anger Management'),
        ('book_store', 'Book Store'),
        ('photography', 'Photography'),
        ('travelling', 'Travelling'),
        ('women_rights', 'Women Rights'),
        ('islam', 'Islam'),
        ('ethics', 'Ethics'),
        ('anti_racism_equality', 'Anti-racism Equality'),
        ('quran', 'Quran'),
        ('purpose_of_life', 'Purpose of Life'),
        ('new_muslim', 'New Muslim'),
        ('prophet_muhammed', 'Prophet Muhammed'),
    ]

    ENGAGEMENT_TYPES = [
        ('engaging_comment', 'Engaging Comment'),
        ('text', 'Text'),
        ('video', 'Video'),
        ('image', 'Image'),
    ]

    FEEDBACK_TYPES = [
        ('like', 'Like'),
        ('comment', 'Comment'),
        ('positive_comment', 'Positive Comment'),
    ]

    REGIONS = [
        ('europe_and_russia', 'Europe & Russia'),
        ('far_east', 'Far East'),
        ('usa_canada_and_australia', 'USA, Canada & Australia'),
        ('latin_america', 'Latin America'),
        ('africa', 'Africa'),
        ('unavailable', 'Unavailable'),
    ]

    GENDERS = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]

    RELIGIONS = [
        ('bahai', "Baha'i"),
        ('buddhism', 'Buddhism'),
        ('christianity', 'Christianity'),
        ('confucianism', 'Confucianism'),
        ('hinduism', 'Hinduism'),
        ('islam', 'Islam'),
        ('jainism', 'Jainism'),
        ('judaism', 'Judaism'),
        ('shinto', 'Shinto'),
        ('sikhism', 'Sikhism'),
        ('taoism', 'Taoism'),
        ('zoroastrianism', 'Zoroastrianism'),
        ('atheism', 'Atheism'),
        ('agnosticism', 'Agnosticism'),
    ]

    first_time_meeting = fields.Date(string='First-time Meeting', required=True)
    user_id = fields.Many2one('res.users', string='Volunteer Member',
                              help='Volunteering Team who brought the opportunity', required=True)
    section_id = fields.Many2one('crm.case.section', string='Volunteer Team')
    social_media = fields.Selection(SOCIAL_MEDIA, 'Social Media',
                                    help='Where the opportunity was found')
    page_name = fields.Char('Page Name')
    page_type = fields.Selection(PAGE_TYPES, 'Page Type')
    page_subject = fields.Selection(SUBJECTS, 'Page Subject')
    page_link = fields.Char('Page Link')
    post_subject = fields.Selection(SUBJECTS, 'Post Subject')
    post_link = fields.Char('Post Link')
    engagement_type = fields.Selection(ENGAGEMENT_TYPES, 'Engagement Type')
    feedback_type = fields.Selection(FEEDBACK_TYPES, 'Feedback Type')
    feedback = fields.Text('Feedback')
    region = fields.Selection(REGIONS, 'Region')
    gender = fields.Selection(GENDERS, 'Gender', required=True)
    religion = fields.Selection(RELIGIONS, 'Religion')
    description = fields.Text(string='Comment')
