# Courier Core - Incident Log System

Odoo 18 module for tracking and managing courier incidents for BeraniExpress.

## Features

- **Incident Logging**: Track incidents with severity levels (low, medium, high)
- **Workflow States**: Draft → Follow-up → Done
- **Validation**: Follow-up notes required before resolving
- **Unique Constraint**: Prevents duplicate incidents (same customer, type, datetime)

## Installation

1. Copy the `courier_core` folder to your Odoo addons directory
2. Update the apps list in Odoo (Apps → Update Apps List)
3. Search for "Courier Core" and install

## Module Structure

```
courier_core/
├── __init__.py
├── __manifest__.py
├── README.md
├── models/
│   ├── __init__.py
│   ├── courier_customer.py
│   ├── courier_shipment.py
│   └── courier_incident.py
├── views/
│   └── courier_incident_views.xml
└── security/
    └── ir.model.access.csv
```

## Testing Instructions

### Manual Testing Steps

1. **Create a Customer**
   - Go to Settings → Technical → Sequences & Identifiers → Database Structure → Models
   - Find `courier.customer` and create a test record via SQL or shell

2. **Create an Incident**
   - Navigate to BeraniExpress Courier → Log Insiden
   - Click "Create"
   - Fill in required fields:
     - Judul Insiden (name)
     - Pelanggan (customer_id)
     - Waktu (incident_datetime) - defaults to now
   - Save the record

3. **Mark Follow-up**
   - Open an incident in Draft state
   - Click "Mark Follow-up" button
   - State changes to "Follow-up"
   - Row color in tree view changes to orange/warning

4. **Resolve Incident**
   - Open an incident in Follow-up state
   - Fill in "Catatan" (followup_note) in the "Catatan Tindakan" tab
   - Click "Resolve" button
   - State changes to "Done"
   - "Selesai pada" (resolved_at) is auto-filled with current datetime
   - Row color in tree view changes to green/success

5. **Test Validation**
   - Try to resolve an incident without filling followup_note
   - Expected: ValidationError message appears

6. **Test Unique Constraint**
   - Try to create a duplicate incident with same customer, type, and datetime
   - Expected: Database constraint error

## Technical Specifications

### Model: `courier.incident`

| Field | Type | Description |
|-------|------|-------------|
| name | Char | Judul Insiden (required) |
| customer_id | Many2one | Link to courier.customer (required) |
| shipment_id | Many2one | Link to courier.shipment |
| incident_type | Selection | health, lost_item, delay, other |
| incident_datetime | Datetime | When incident occurred (required) |
| severity | Selection | low, medium, high |
| description | Text | Incident details |
| followup_note | Text | Action taken |
| state | Selection | draft, followup, done |
| resolved_at | Datetime | Auto-filled when resolved |

### Business Logic

- `action_mark_followup()`: Changes state from draft to followup
- `action_resolve()`: Changes state to done and sets resolved_at

### Constraints

- **SQL**: Unique combination of (customer_id, incident_type, incident_datetime)
- **Python**: followup_note required when state is 'done'

## License

LGPL-3
