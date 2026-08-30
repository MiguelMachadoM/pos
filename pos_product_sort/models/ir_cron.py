# Copyright 2026 Miguel Machado
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0).

import logging
from datetime import datetime

import pytz

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

from odoo.addons.base.models.res_partner import _tz_get

_logger = logging.getLogger(__name__)

TOP_SALES_CRON_CODE_MARKER = "_recompute_pos_top_sales_qty"


class IrCron(models.Model):
    _inherit = "ir.cron"

    pos_sequence_local_hour = fields.Integer(
        string="Local run hour",
        default=3,
        help="Hour (0-23) for the daily top-sales job in the timezone below.",
    )
    pos_sequence_local_minute = fields.Integer(
        string="Local run minute",
        default=0,
        help="Minute (0-59) for the daily top-sales job in the timezone below.",
    )
    pos_sequence_local_tz = fields.Selection(
        _tz_get,
        string="Local timezone",
        help="Timezone for local hour/minute. If empty, the main company's "
        "timezone is used when scheduling the next run.",
    )
    is_pos_sequence_top_sales_cron = fields.Boolean(
        compute="_compute_is_pos_sequence_top_sales_cron",
    )

    @api.depends("code")
    def _compute_is_pos_sequence_top_sales_cron(self):
        for cron in self:
            cron.is_pos_sequence_top_sales_cron = TOP_SALES_CRON_CODE_MARKER in (
                cron.code or ""
            )

    @api.constrains(
        "pos_sequence_local_hour",
        "pos_sequence_local_minute",
        "code",
    )
    def _check_pos_sequence_local_slot(self):
        for cron in self.filtered("is_pos_sequence_top_sales_cron"):
            if not (0 <= cron.pos_sequence_local_hour <= 23):
                raise ValidationError(_("Local run hour must be between 0 and 23."))
            if not (0 <= cron.pos_sequence_local_minute <= 59):
                raise ValidationError(_("Local run minute must be between 0 and 59."))

    def _pos_sequence_align_top_sales_nextcall(self):
        from ..cron_utils import (
            next_top_sales_cron_nextcall_utc_naive,
        )

        for cron in self.filtered("is_pos_sequence_top_sales_cron"):
            next_naive_utc = next_top_sales_cron_nextcall_utc_naive(
                cron, fields.Datetime.now(), cron.env
            )
            cron.sudo().write({"nextcall": fields.Datetime.to_string(next_naive_utc)})

    def write(self, vals):
        res = super().write(vals)
        slot_fields = {
            "pos_sequence_local_hour",
            "pos_sequence_local_minute",
            "pos_sequence_local_tz",
        }
        if slot_fields.intersection(vals):
            self.filtered(
                "is_pos_sequence_top_sales_cron"
            )._pos_sequence_align_top_sales_nextcall()
        return res

    def _reschedule_later(self, job):
        top_sales_cron = self.env.ref(
            "pos_product_sort.ir_cron_recompute_pos_top_sales_qty",
            raise_if_not_found=False,
        )
        if top_sales_cron and job.get("id") == top_sales_cron.id:
            from ..cron_utils import (
                next_top_sales_cron_nextcall_utc_naive,
            )

            cron = top_sales_cron.sudo()
            now_ts = fields.Datetime.context_timestamp(self, datetime.utcnow())
            next_naive_utc = next_top_sales_cron_nextcall_utc_naive(
                cron, fields.Datetime.now(), cron.env
            )
            nextcall_str = fields.Datetime.to_string(next_naive_utc)
            lastcall_str = fields.Datetime.to_string(now_ts.astimezone(pytz.UTC))
            tz_label = (
                cron.pos_sequence_local_tz or cron.env.company.partner_id.tz or "UTC"
            )
            self.env.cr.execute(
                """
                UPDATE ir_cron
                SET nextcall = %s,
                    lastcall = %s
                WHERE id = %s
                """,
                [nextcall_str, lastcall_str, job["id"]],
            )
            self.env.cr.execute(
                """
                DELETE FROM ir_cron_trigger
                WHERE cron_id = %s
                AND call_at < (now() at time zone 'UTC')
                """,
                [job["id"]],
            )
            _logger.info(
                "Job %r (%s) rescheduled by pos_product_sort → next %02d:%02d %s "
                "(UTC in database: %s)",
                job.get("cron_name"),
                job["id"],
                cron.pos_sequence_local_hour,
                cron.pos_sequence_local_minute,
                tz_label,
                nextcall_str,
            )
            return
        return super()._reschedule_later(job)
