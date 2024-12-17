from odoo import _, models, fields, api
from odoo.exceptions import ValidationError, AccessError

import logging  # Nhập thư viện logging để ghi lại thông tin và lỗi
_logger = logging.getLogger(__name__)  # Tạo logger để ghi lại thông tin

class LogisticProduct(models.Model):
    _name = 'logistic.products'
    
    # liên hệ với model "logistic.contacts" để lưu thông tin hàng hóa
    contact_id = fields.Many2one("logistic.contacts", string="Liên Hệ")
    
    # Thông tin người gửi
    sender_id = fields.Many2one("res.users", string="Người gửi")
    # Thông tin người nhận
    receiver_id = fields.Many2one("res.users", string="Người nhận")
    
#    ------------------------------------------------------------------ 
    
    sender_name = fields.Char(string='Người gửi')
    sender_street = fields.Char(string="Địa Chỉ")
    
    receiver_name = fields.Char(string="Người nhận")
    receiver_street = fields.Char(string="Địa Chỉ")    
    
# ----------------------------------------------------------------------
    # Thông tin sản phẩm gửi
    # Tên hàng gửi
    product_name = fields.Char(string='Tên hàng hóa', required=True)
    
    # ID Đơn Hàng
    order_code = fields.Char(
        string='Mã Đơn Hàng', 
        readonly=True,
    )
        
    # Khối lượng thùng hàng (Đơn vị Kilogram)
    product_weight = fields.Float(
        string='Khối lượng (kg)', 
        required=True,
        help='Khối lượng của thùng hàng, tính bằng kilogram (kg).'
    )
    
    # Kích thước thùng hàng (Dài, Rộng, Cao)
    product_lengh = fields.Float(
        string='Chiều dài (cm)', 
        required=True,
        help='Chiều dài của thùng hàng, tính bằng cm.'
    )
    product_width = fields.Float(
        string='Chiều rộng (cm)', 
        required=True,
        help='Chiều rộng của thùng hàng, tính bằng cm.'
    )
    product_height = fields.Float(
        string='Chiều cao (cm)', 
        required=True,
        help='Chiều cao của thùng hàng, tính bằng cm.'
    )
    
    # Loại hàng đặc biệt
    properties_of_goods = fields.Selection([
        ('None', 'Không tùy chọn'),
        ('Fragile', 'Dễ vỡ'),
        ('Expensive goods', 'Giá trị cao'),
        ('Frozen goods', 'Hàng đông lạnh'),
        ('Liquid', 'Chất Lỏng'),
    ], string='Loại hàng hóa', required=True, default='None')
    
    def get_sent_products(self):
        """Lấy các hàng hóa gửi của người dùng hiện tại."""
        user_id = self.env.user.id
        return self.env['logistic.products'].search([('sender_id', '=', user_id)])

    def get_received_products(self):
        """Lấy các hàng hóa nhận của người dùng hiện tại."""
        user_id = self.env.user.id
        return self.env['logistic.products'].search([('receiver_id', '=', user_id)])