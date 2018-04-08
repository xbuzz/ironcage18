from django.test import TestCase

from . import factories

from tickets import actions
from tickets.models import TicketInvitation


class CreatePendingOrderTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.alice = factories.create_user()

    def test_order_for_self_individual(self):
        order = actions.create_pending_order(
            purchaser=self.alice,
            billing_details={'name': 'Alice Apple', 'addr': 'Eadrax, Sirius Tau'},
            rate='individual',
            days_for_self=['thu', 'fri', 'sat']
        )

        self.assertEqual(self.alice.orders.count(), 1)
        self.assertIsNone(self.alice.get_ticket())

        self.assertEqual(order.purchaser, self.alice)
        self.assertEqual(order.status, 'pending')
        self.assertEqual(order.invoice_number, None)
        self.assertEqual(order.billing_name, 'Alice Apple')
        self.assertEqual(order.billing_addr, 'Eadrax, Sirius Tau')

    def test_order_for_self_corporate(self):
        order = actions.create_pending_order(
            purchaser=self.alice,
            billing_details={'name': 'Sirius Cybernetics Corp.', 'addr': 'Eadrax, Sirius Tau'},
            rate='corporate',
            days_for_self=['thu', 'fri', 'sat'],
        )

        self.assertEqual(self.alice.orders.count(), 1)
        self.assertIsNone(self.alice.get_ticket())

        self.assertEqual(order.purchaser, self.alice)
        self.assertEqual(order.status, 'pending')
        self.assertEqual(order.invoice_number, None)
        self.assertEqual(order.billing_name, 'Sirius Cybernetics Corp.')
        self.assertEqual(order.billing_addr, 'Eadrax, Sirius Tau')

    def test_order_for_others(self):
        order = actions.create_pending_order(
            purchaser=self.alice,
            billing_details={'name': 'Alice Apple', 'addr': 'Eadrax, Sirius Tau'},
            rate='individual',
            email_addrs_and_days_for_others=[
                ('bob@example.com', ['fri', 'sat']),
                ('carol@example.com', ['sat', 'sun']),
            ]
        )

        self.assertEqual(self.alice.orders.count(), 1)
        self.assertIsNone(self.alice.get_ticket())

        self.assertEqual(order.purchaser, self.alice)
        self.assertEqual(order.status, 'pending')
        self.assertEqual(order.invoice_number, None)
        self.assertEqual(order.billing_name, 'Alice Apple')
        self.assertEqual(order.billing_addr, 'Eadrax, Sirius Tau')

    def test_order_for_self_and_others(self):
        order = actions.create_pending_order(
            purchaser=self.alice,
            billing_details={'name': 'Alice Apple', 'addr': 'Eadrax, Sirius Tau'},
            rate='individual',
            days_for_self=['thu', 'fri', 'sat'],
            email_addrs_and_days_for_others=[
                ('bob@example.com', ['fri', 'sat']),
                ('carol@example.com', ['sat', 'sun']),
            ]
        )

        self.assertEqual(self.alice.orders.count(), 1)
        self.assertIsNone(self.alice.get_ticket())

        self.assertEqual(order.purchaser, self.alice)
        self.assertEqual(order.status, 'pending')
        self.assertEqual(order.invoice_number, None)
        self.assertEqual(order.billing_name, 'Alice Apple')
        self.assertEqual(order.billing_addr, 'Eadrax, Sirius Tau')


class UpdatePendingOrderTests(TestCase):
    def test_order_for_self_to_order_for_self(self):
        order = factories.create_pending_order_for_self()
        actions.update_pending_order(
            order,
            billing_details={'name': 'Alice Apple', 'addr': 'Eadrax, Sirius Tau'},
            rate='individual',
            days_for_self=['fri'],
        )

        self.assertEqual(order.status, 'pending')
        self.assertEqual(order.invoice_number, None)
        self.assertEqual(order.billing_name, 'Alice Apple')
        self.assertEqual(order.billing_addr, 'Eadrax, Sirius Tau')

        [row] = order.all_order_rows()

        self.assertEqual(row.cost_excl_vat, 45)
        self.assertEqual(row.item_descr, '1-day individual-rate ticket')
        self.assertEqual(row.item_descr_extra, 'Friday')

        ticket = row.item
        self.assertEqual(ticket.owner, order.purchaser)
        self.assertEqual(ticket.rate, 'individual')
        self.assertEqual(ticket.days(), ['Friday'])

    def test_order_for_self_to_order_for_others(self):
        order = factories.create_pending_order_for_self()
        actions.update_pending_order(
            order,
            billing_details={'name': 'Alice Apple', 'addr': 'Eadrax, Sirius Tau'},
            rate='individual',
            email_addrs_and_days_for_others=[
                ('bob@example.com', ['fri', 'sat']),
                ('carol@example.com', ['sat', 'sun']),
            ]
        )

        self.assertEqual(order.status, 'pending')
        self.assertEqual(order.invoice_number, None)
        self.assertEqual(order.billing_name, 'Alice Apple')
        self.assertEqual(order.billing_addr, 'Eadrax, Sirius Tau')

        [row1, row2] = order.all_order_rows()

        self.assertEqual(row1.cost_excl_vat, 75)
        self.assertEqual(row1.item_descr, '2-day individual-rate ticket')
        self.assertEqual(row1.item_descr_extra, 'Friday, Saturday')

        ticket1 = row1.item
        self.assertEqual(ticket1.owner, None)
        self.assertEqual(ticket1.rate, 'individual')
        self.assertEqual(ticket1.days(), ['Friday', 'Saturday'])

        self.assertEqual(row2.cost_excl_vat, 75)
        self.assertEqual(row2.item_descr, '2-day individual-rate ticket')
        self.assertEqual(row2.item_descr_extra, 'Saturday, Sunday')

        ticket2 = row2.item
        self.assertEqual(ticket1.owner, None)
        self.assertEqual(ticket2.rate, 'individual')
        self.assertEqual(ticket2.days(), ['Saturday', 'Sunday'])

    def test_order_for_self_to_order_for_self_and_others(self):
        order = factories.create_pending_order_for_self()
        actions.update_pending_order(
            order,
            billing_details={'name': 'Alice Apple', 'addr': 'Eadrax, Sirius Tau'},
            rate='individual',
            days_for_self=['fri', 'sat', 'sun'],
            email_addrs_and_days_for_others=[
                ('bob@example.com', ['fri', 'sat']),
                ('carol@example.com', ['sat', 'sun']),
            ]
        )

        self.assertEqual(order.status, 'pending')
        self.assertEqual(order.invoice_number, None)
        self.assertEqual(order.billing_name, 'Alice Apple')
        self.assertEqual(order.billing_addr, 'Eadrax, Sirius Tau')

        [row1, row2, row3] = order.all_order_rows()

        self.assertEqual(row1.cost_excl_vat, 105)
        self.assertEqual(row1.item_descr, '3-day individual-rate ticket')
        self.assertEqual(row1.item_descr_extra, 'Friday, Saturday, Sunday')

        ticket1 = row1.item
        self.assertEqual(ticket1.owner, order.purchaser)
        self.assertEqual(ticket1.rate, 'individual')
        self.assertEqual(ticket1.days(), ['Friday', 'Saturday', 'Sunday'])

        self.assertEqual(row2.cost_excl_vat, 75)
        self.assertEqual(row2.item_descr, '2-day individual-rate ticket')
        self.assertEqual(row2.item_descr_extra, 'Friday, Saturday')

        ticket2 = row2.item
        self.assertEqual(ticket2.owner, None)
        self.assertEqual(ticket2.rate, 'individual')
        self.assertEqual(ticket2.days(), ['Friday', 'Saturday'])

        self.assertEqual(row3.cost_excl_vat, 75)
        self.assertEqual(row3.item_descr, '2-day individual-rate ticket')
        self.assertEqual(row3.item_descr_extra, 'Saturday, Sunday')

        ticket3 = row3.item
        self.assertEqual(ticket3.owner, None)
        self.assertEqual(ticket3.rate, 'individual')
        self.assertEqual(ticket3.days(), ['Saturday', 'Sunday'])

    def test_individual_order_to_corporate_order(self):
        order = factories.create_pending_order_for_self()
        actions.update_pending_order(
            order,
            billing_details={'name': 'Sirius Cybernetics Corp.', 'addr': 'Eadrax, Sirius Tau'},
            rate='corporate',
            days_for_self=['fri', 'sat', 'sun'],
        )

        self.assertEqual(order.status, 'pending')
        self.assertEqual(order.invoice_number, None)
        self.assertEqual(order.billing_name, 'Sirius Cybernetics Corp.')
        self.assertEqual(order.billing_addr, 'Eadrax, Sirius Tau')

        [row] = order.all_order_rows()

        self.assertEqual(row.cost_excl_vat, 210)
        self.assertEqual(row.item_descr, '3-day corporate-rate ticket')
        self.assertEqual(row.item_descr_extra, 'Friday, Saturday, Sunday')

        ticket = row.item
        self.assertEqual(ticket.owner, order.purchaser)
        self.assertEqual(ticket.rate, 'corporate')
        self.assertEqual(ticket.days(), ['Friday', 'Saturday', 'Sunday'])

    def test_corporate_order_to_individual_order(self):
        order = factories.create_pending_order_for_self(rate='corporate')
        actions.update_pending_order(
            order,
            billing_details={'name': 'Alice Apple', 'addr': 'Eadrax, Sirius Tau'},
            rate='individual',
            days_for_self=['fri', 'sat', 'sun'],
        )

        self.assertEqual(order.status, 'pending')
        self.assertEqual(order.invoice_number, None)
        self.assertEqual(order.billing_name, 'Alice Apple')
        self.assertEqual(order.billing_addr, 'Eadrax, Sirius Tau')

        [row] = order.all_order_rows()

        self.assertEqual(row.cost_excl_vat, 105)
        self.assertEqual(row.item_descr, '3-day individual-rate ticket')
        self.assertEqual(row.item_descr_extra, 'Friday, Saturday, Sunday')

        ticket = row.item
        self.assertEqual(ticket.owner, order.purchaser)
        self.assertEqual(ticket.rate, 'individual')
        self.assertEqual(ticket.days(), ['Friday', 'Saturday', 'Sunday'])


class TicketInvitationTests(TestCase):
    def test_claim_ticket_invitation(self):
        factories.create_confirmed_order_for_others()
        bob = factories.create_user('Bob')

        invitation = TicketInvitation.objects.get(email_addr='bob@example.com')
        actions.claim_ticket_invitation(bob, invitation)

        self.assertIsNotNone(bob.get_ticket())
