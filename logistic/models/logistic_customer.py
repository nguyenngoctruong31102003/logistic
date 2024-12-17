from odoo import models, fields
import logging  # Nhập thư viện logging để ghi lại thông tin và lỗi
_logger = logging.getLogger(__name__)  # Tạo logger để ghi lại thông tin


class ResPartnerInherit(models.Model):
    _inherit = 'res.partner'