# Copyright 2015 Antiun Ingeniería, S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase


class LeadCase(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.lead = cls.env["crm.lead"].create({"name": __file__, "partner_name": "HÎ"})
        cls.partner = cls.env["res.partner"].create({"name": __file__})
        cls.test_field = "ES98765432M"
        cls.test2_field = "11111111H"

    def test_transfered_values(self):
        """Field gets transfered when creating partner."""
        self.lead.vat = self.test_field
        self.lead._handle_partner_assignment()
        self.assertEqual(self.lead.partner_id.vat, self.test_field)

    def test_onchange_partner_id(self):
        """Lead gets VAT from partner when linked to it."""
        self.partner.vat = self.test_field
        result = self.lead._prepare_values_from_partner(self.lead.partner_id)
        self.assertNotIn("vat", result)
        self.lead.partner_id = self.partner
        result = self.lead._prepare_values_from_partner(self.lead.partner_id)
        self.assertEqual(result["vat"], self.test_field)

    def test_onchange_vat(self):
        """First change vat in partner, after it change in lead"""
        self.lead.partner_id = self.partner
        self.partner.vat = self.test_field
        self.assertEqual(self.partner.vat, self.lead.vat)
        self.lead.vat = self.test2_field
        self.assertEqual(self.partner.vat, self.lead.vat)
