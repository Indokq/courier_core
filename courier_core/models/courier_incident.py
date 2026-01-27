from odoo import models, fields, api
from odoo.exceptions import ValidationError


class CourierCustomer(models.Model):
    """Stub model for customer - required for Many2one relation."""
    _name = 'courier.customer'
    _description = 'Courier Customer'

    name = fields.Char(string='Name', required=True)


class CourierShipment(models.Model):
    """Stub model for shipment - required for Many2one relation."""
    _name = 'courier.shipment'
    _description = 'Courier Shipment'

    name = fields.Char(string='No. Resi', required=True)
    customer_id = fields.Many2one('courier.customer', string='Customer')


class CourierIncident(models.Model):
    """Main model for incident logging."""
    _name = 'courier.incident'
    _description = 'Courier Incident Log'
    _order = 'incident_datetime desc'

    name = fields.Char(
        string='Judul Insiden',
        required=True,
    )
    customer_id = fields.Many2one(
        'courier.customer',
        string='Pelanggan',
        required=True,
    )
    shipment_id = fields.Many2one(
        'courier.shipment',
        string='No. Resi',
    )
    incident_type = fields.Selection(
        selection=[
            ('health', 'Health'),
            ('lost_item', 'Lost Item'),
            ('delay', 'Delay'),
            ('other', 'Other'),
        ],
        string='Tipe',
        default='other',
        required=True,
    )
    incident_datetime = fields.Datetime(
        string='Waktu',
        required=True,
        default=fields.Datetime.now,
    )
    severity = fields.Selection(
        selection=[
            ('low', 'Low'),
            ('medium', 'Medium'),
            ('high', 'High'),
        ],
        string='Urgensi',
        default='low',
        required=True,
    )
    description = fields.Text(
        string='Kronologi',
    )
    followup_note = fields.Text(
        string='Catatan',
    )
    state = fields.Selection(
        selection=[
            ('draft', 'Draft'),
            ('followup', 'Follow-up'),
            ('done', 'Done'),
        ],
        string='Status',
        default='draft',
        required=True,
    )
    resolved_at = fields.Datetime(
        string='Selesai pada',
        readonly=True,
    )

    _sql_constraints = [
        (
            'unique_customer_incident_type_datetime',
            'UNIQUE(customer_id, incident_type, incident_datetime)',
            'An incident with the same customer, type, and datetime already exists!'
        ),
    ]

    @api.constrains('state', 'followup_note')
    def _check_followup_note_required(self):
        for record in self:
            if record.state == 'done' and not record.followup_note:
                raise ValidationError(
                    'Catatan (followup_note) wajib diisi sebelum menyelesaikan insiden!'
                )

    def action_mark_followup(self):
        """Button action: Change state from draft to followup."""
        for record in self:
            record.state = 'followup'

    def action_resolve(self):
        """Button action: Change state to done and set resolved_at."""
        for record in self:
            record.write({
                'state': 'done',
                'resolved_at': fields.Datetime.now(),
            })
