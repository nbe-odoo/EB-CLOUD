from odoo import api, fields, models
from odoo.exceptions import UserError
import datetime
import base64
from io import StringIO


class Wizard(models.TransientModel):
    _name = 'invoice_export.wizard'

    def _print_csv(self):
        invoices = self.env['account.invoice'].browse(self.env.context.get('active_ids'))
        f = StringIO()
        f.write(
            "ID, Type, Nominal A/C Ref, , Account Reference, Date, Reference, Details, Net Amount, Tax Code, Tax Amount, Exchange Rate\n")
        for invoice in invoices:
            source_doc = ""
            if invoice.origin:
                for source in invoice.origin:
                    source_doc += source
                    source = ''.join(source_doc).replace(',', '')
            else:
                source = ""

            if invoice.type == 'out_refund':
                journal_type = 'Credit Notes'
            elif invoice.type == 'out_invoice':
                journal_type = 'Customer Invoice'
            elif invoice.type == 'in_invoice':
                journal_type = 'Vendor Bills'
            elif invoice.type == 'in_refund':
                journal_type = 'Vendor Refunds'
            else:
                journal_type = 'Other'

            currency_rates = invoice.env['res.currency.rate'].search(
                ['&', ('currency_id.name', '=', invoice.currency_id.name), ('name', '<=', invoice.date_invoice)],
                limit=1)

            if invoice.date_invoice:
                new_date = datetime.datetime.strptime(str(invoice.date_invoice), "%Y-%m-%d").strftime("%d-%m-%Y")
            else:
                new_date = ""

            account_type = []
            for line in invoice.invoice_line_ids:
                account_type.append(line.account_id.code)

            account_type_unique = set(account_type)

            for account in account_type_unique:
                total_unpaid = 0
                tax = 0

                for line in invoice.invoice_line_ids:

                    if line.account_id.code == account:
                        total_unpaid += line.price_subtotal
                        tax += line.price_subtotal * line.invoice_line_tax_ids.amount / 100

                f.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s \n" % (invoice.id,
                                                                    journal_type, account, '',
                                                                    invoice.x_studio_field_xuLH1, new_date,
                                                                    invoice.number, source,
                                                                    round(total_unpaid, 2),
                                                                    invoice.fiscal_position_id.name, round(tax, 2),
                                                                    str.format('{0:.6f}', currency_rates.rate, 6)))

        decoded = f.getvalue()
        f.close()
        return decoded

    def _get_filename(self):
        return "odoo.sage.import " + datetime.datetime.now().strftime("%d/%m/%y %H%M%S") + '.csv'

    def _get_data(self):
        return base64.b64encode(self._print_csv().encode())

    filename = fields.Char(default=_get_filename)
    file = fields.Binary(default=_get_data)
