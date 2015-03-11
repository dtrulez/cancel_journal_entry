from openerp.osv import fields, osv
from openerp import api, models
from openerp.tools.translate import _

class cancel_journal_entry(models.Model):
    _name = "account.journal"
    _inherit = "account.journal"

    _columns = {
        'sub_ledger_journal': fields.boolean('Sub Ledger Journal', help='Check this box to forbid journal entry cancelling'),
    }


class account_move(models.Model):
    _name = "account.move"
    _inherit = "account.move"

    def button_cancel(self, cr, uid, ids, context=None):
	for move in self.browse(cr, uid, ids, context):
	    #import pdb
	    #pdb.set_trace()
	    if move.journal_id.sub_ledger_journal and move.line_id[0].invoice:
		raise osv.except_osv(_('User Error!'), _('You cannot cancel journal entries.\n You should cancel the journal entries at Customer/Supplier invoice.'))

	result = super(account_move, self).button_cancel(cr, uid, ids, context)
	return True

    _columns = {
	'journal_id': fields.many2one('account.journal', 'Journal', required=True, states={'posted':[('readonly',True)]}, domain=[('sub_ledger_journal','=',False)]),
    }
