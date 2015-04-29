import base64
from openerp.http import request
from openerp import http
from openerp.addons.website_hr_recruitment.controllers import main
from openerp import SUPERUSER_ID

class website_hr_recruitment_extra(main.website_hr_recruitment):
    @http.route('/jobs/thankyou', methods=['POST'], type='http', auth="public", website=True)
    def jobs_thankyou(self, **post):
        error = {}
        for field_name in ["partner_name", "phone", "email_from"]:
            if not post.get(field_name):
                error[field_name] = 'missing'
        if error:
            request.session['website_hr_recruitment_error'] = error
            ufile = post.pop('ufile')
            if ufile:
                error['ufile'] = 'reset'
            request.session['website_hr_recruitment_default'] = post
            return request.redirect('/jobs/apply/%s' % post.get("job_id"))

        # public user can't create applicants (duh)
        env = request.env(user=SUPERUSER_ID)
        value = {
            'source_id' : env.ref('hr_recruitment.source_website_company').id,
            'name': '%s\'s Application' % post.get('partner_name'),
        }
        # for f in ['email_from', 'partner_name', 'description']:
        #     value[f] = post.get(f)
        # for f in ['department_id', 'job_id']:
        #     value[f] = int(post.get(f) or 0)
        # # Retro-compatibility for saas-3. "phone" field should be replace by "partner_phone" in the template in trunk.
        # value['partner_phone'] = post.pop('phone', False)
        value.update(post)
        applicant_id = env['hr.applicant'].create(value).id
        if post['ufile']:
            attachment_value = {
                'name': post['ufile'].filename,
                'res_name': value['partner_name'],
                'res_model': 'hr.applicant',
                'res_id': applicant_id,
                'datas': base64.encodestring(post['ufile'].read()),
                'datas_fname': post['ufile'].filename,
            }
            env['ir.attachment'].create(attachment_value)
        return request.render("website_hr_recruitment.thankyou", {})
