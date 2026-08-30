# Copyright 2026 Miguel Machado
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0).

"""Daily ir.cron slot at a configurable local time (company or cron timezone)."""

from datetime import timedelta, timezone
from zoneinfo import ZoneInfo

from odoo import fields

UTC = timezone.utc

DEFAULT_TOP_SALES_CRON_HOUR = 3
DEFAULT_TOP_SALES_CRON_MINUTE = 0


def _resolve_cron_timezone(cron, env):
    """IANA timezone name for the top-sales cron slot."""
    tz_name = cron.pos_sequence_local_tz if cron else None
    if not tz_name:
        tz_name = env.company.partner_id.tz or env.user.tz or "UTC"
    try:
        return ZoneInfo(tz_name)
    except Exception:
        return ZoneInfo("UTC")


def next_top_sales_cron_nextcall_utc_naive(cron, reference=None, env=None):
    """
    Next daily run at the cron's local hour/minute in its timezone, as UTC-naive
    datetime (Odoo ``ir.cron.nextcall`` convention).
    """
    if env is None:
        env = cron.env
    if reference is None:
        reference = fields.Datetime.now()
    hour = cron.pos_sequence_local_hour if cron else DEFAULT_TOP_SALES_CRON_HOUR
    minute = cron.pos_sequence_local_minute if cron else DEFAULT_TOP_SALES_CRON_MINUTE
    tz = _resolve_cron_timezone(cron, env)
    if isinstance(reference, str):
        ref_naive_utc = fields.Datetime.from_string(reference)
    else:
        aware = reference.replace(tzinfo=UTC) if reference.tzinfo is None else reference
        ref_naive_utc = aware.astimezone(UTC).replace(tzinfo=None)
    ref_aware_utc = ref_naive_utc.replace(tzinfo=UTC)
    local_now = ref_aware_utc.astimezone(tz)
    target_local = local_now.replace(
        hour=hour,
        minute=minute,
        second=0,
        microsecond=0,
    )
    if target_local <= local_now:
        target_local += timedelta(days=1)
    return target_local.astimezone(UTC).replace(tzinfo=None)


def align_top_sales_ir_cron(env, force_nextcall=True):
    """Refresh top-sales cron timezone default and recompute nextcall."""
    cron = env.ref(
        "pos_product_sort.ir_cron_recompute_pos_top_sales_qty",
        raise_if_not_found=False,
    )
    if not cron:
        return
    vals = {
        "interval_number": 1,
        "interval_type": "days",
    }
    if not cron.pos_sequence_local_tz:
        company_tz = env.company.partner_id.tz
        if company_tz:
            vals["pos_sequence_local_tz"] = company_tz
    if force_nextcall and cron.active:
        vals["nextcall"] = fields.Datetime.to_string(
            next_top_sales_cron_nextcall_utc_naive(cron, fields.Datetime.now(), env)
        )
    cron.sudo().write(vals)
