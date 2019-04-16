from odoo import api, fields, models, _
from odoo.exceptions import UserError
import csv, datetime


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    def print_csv(self):

        with open("odoo.sage.import %s.csv" % (datetime.datetime.now()), 'w') as f:
            f.write(
                "ID, Type, Nominal A/C Ref, , Account Reference, Date, Reference, Details, Net Amount, Tax Code, Tax Amount, Exchange Rate\n")
            for self in self:

                source_doc = ""
                if self.origin:
                    for source in self.origin:
                        source_doc += source
                        source = ''.join(source_doc).replace(',', '')
                else:
                    source = ""

                currency_rate = self.env['res.currency'].search([('name', '=', self.currency_id.name)])
                total_unpayed = 0
                tax = 0
                for line in self.invoice_line_ids:
                    if line.name == 'US Ground Carriage':
                        f.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s \n" % (self.id,
                                                                            self.journal_id.name, line.account_id.code,
                                                                            '', self.x_studio_sage_ac_1,
                                                                            self.date_invoice, self.number, source,
                                                                            line.price_subtotal,
                                                                            self.fiscal_position_id.name,
                                                                            line.price_subtotal * line.invoice_line_tax_ids.amount / 100,
                                                                            round(currency_rate.rate, 5)))
                    else:
                        total_unpayed += line.price_subtotal
                        tax += line.price_subtotal * line.invoice_line_tax_ids.amount / 100
                        account_id = line.account_id.code
                f.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s \n" % (self.id,
                                                                    self.journal_id.name, account_id, '',
                                                                    self.x_studio_sage_ac_1, self.date_invoice,
                                                                    self.number, source,
                                                                    total_unpayed, self.fiscal_position_id.name, tax,
                                                                    round(currency_rate.rate, 5)))
