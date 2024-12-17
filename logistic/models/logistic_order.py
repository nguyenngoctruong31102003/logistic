from odoo import _, models, fields, api
from odoo.exceptions import ValidationError, AccessError

import logging      # Nhập thư viện logging để ghi lại thông tin và lỗi
_logger = logging.getLogger(__name__)   # Tạo logger để ghi lại thông tin

class ContactsInformation(models.Model):
    _name= 'logistic.contacts'
    name = fields.Char(string='Đơn Hàng')
    
    sender_id = fields.Many2one("res.users", string='Người gửi')  
    receiver_id = fields.Many2one("res.users", string='Người nhận') 

# ---------------------------------------------------------------------------------------------
    # Thông tin sản phẩm gửi
    # Tên hàng gửi
    product_name = fields.Char(string='Tên hàng hóa', required=True)
    
    # Ảnh sản phẩm gửi
    product_template_image = fields.Binary(string='Ảnh sản phẩm')

    # ID Đơn Hàng
    order_code = fields.Char(
        string='Mã Đơn Hàng', 
        readonly=True,
        # required=True,
        # copy=False,
        # default= 'New'
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
    
    
# ---------------------------------------------------------------------------------------------
    # Thông tin người gửi
    sender_name = fields.Char(string='Người gửi')
    sender_mobile = fields.Char(string='Số Điện Thoại',help='Vui lòng nhập đúng số điện thoại')
    sender_email = fields.Char(string='Email')
    # Địa chỉ
    sender_street = fields.Char(string='Địa Chỉ',help='Vui lòng nhập đúng địa chỉ')
    sender_city = fields.Selection(
        selection=[
            ('hanoi', 'Hà Nội'),
            ('hochiminh', 'Hồ Chí Minh'),
            ('danang', 'Đà Nẵng'),
            ('haiphong', 'Hải Phòng'),
            ('cantho', 'Cần Thơ'),
            ('bacgiang', 'Bắc Giang'),
            ('backan', 'Bắc Kạn'),
            ('bariavungtau', 'Bà Rịa - Vũng Tàu'),
            ('bentre', 'Bến Tre'),
            ('binhduong', 'Bình Dương'),
            ('binhphuoc', 'Bình Phước'),
            ('binhthuan', 'Bình Thuận'),
            ('caobang', 'Cao Bằng'),
            ('cantho', 'Cần Thơ'),
            ('daklak', 'Đắk Lắk'),
            ('daknong', 'Đắk Nông'),
            ('dienbien', 'Điện Biên'),
            ('dongnai', 'Đồng Nai'),
            ('dongthap', 'Đồng Tháp'),
            ('gialai', 'Gia Lai'),
            ('hatinh', 'Hà Tĩnh'),
            ('haugiang', 'Hậu Giang'),
            ('hoabinh', 'Hòa Bình'),
            ('hungyen', 'Hưng Yên'),
            ('khanhhoa', 'Khánh Hòa'),
            ('kiengiang', 'Kiên Giang'),
            ('konturng', 'Kon Tum'),
            ('laocai', 'Lào Cai'),
            ('langson', 'Lạng Sơn'),
            ('laocai', 'Lào Cai'),
            ('lamdong', 'Lâm Đồng'),
            ('longan', 'Long An'),
            ('namdinh', 'Nam Định'),
            ('nghean', 'Nghệ An'),
            ('ninhbinh', 'Ninh Bình'),
            ('ninhthuan', 'Ninh Thuận'),
            ('phuquoc', 'Phú Quốc'),
            ('phutho', 'Phú Thọ'),
            ('quangbinh', 'Quảng Bình'),
            ('quangnam', 'Quảng Nam'),
            ('quangngai', 'Quảng Ngãi'),
            ('quangninh', 'Quảng Ninh'),
            ('quangtri', 'Quảng Trị'),
            ('saka', 'Sơn La'),
            ('tayninh', 'Tây Ninh'),
            ('thanhhoa', 'Thanh Hóa'),
            ('thodinh', 'Thái Dương'),
            ('thaitin', 'Thái Tiên'),
            ('thainguyen', 'Thái Nguyên'),
            ('tieucgai', 'Tiền Giang'),
            ('tràvinh', 'Trà Vinh'),
            ('tuyenquang', 'Tuyên Quang'),
            ('vinhphuc', 'Vĩnh Phúc'),
            ('vinhlong', 'Vĩnh Long'),
        ],
        string="Thành Phố",)
    sender_country_id = fields.Many2one('res.country', string='Quốc Gia', default=241)
# ---------------------------------------------------------------------------------------------
    # Thông tin người nhận
    receiver_name = fields.Char(string='Người nhận')
    receiver_mobile = fields.Char(string='Số Điện Thoại',help='Vui lòng nhập đúng số điện thoại')
    receiver_email = fields.Char(string='Email')
    # Địa chỉ
    receiver_street = fields.Char(string='Địa Chỉ',help='Vui lòng nhập đúng địa chỉ')
    receiver_city = fields.Selection(
        selection=[
            ('hanoi', 'Hà Nội'),
            ('hochiminh', 'Hồ Chí Minh'),
            ('danang', 'Đà Nẵng'),
            ('haiphong', 'Hải Phòng'),
            ('cantho', 'Cần Thơ'),
            ('bacgiang', 'Bắc Giang'),
            ('backan', 'Bắc Kạn'),
            ('bariavungtau', 'Bà Rịa - Vũng Tàu'),
            ('bentre', 'Bến Tre'),
            ('binhduong', 'Bình Dương'),
            ('binhphuoc', 'Bình Phước'),
            ('binhthuan', 'Bình Thuận'),
            ('caobang', 'Cao Bằng'),
            ('cantho', 'Cần Thơ'),
            ('daklak', 'Đắk Lắk'),
            ('daknong', 'Đắk Nông'),
            ('dienbien', 'Điện Biên'),
            ('dongnai', 'Đồng Nai'),
            ('dongthap', 'Đồng Tháp'),
            ('gialai', 'Gia Lai'),
            ('hatinh', 'Hà Tĩnh'),
            ('haugiang', 'Hậu Giang'),
            ('hoabinh', 'Hòa Bình'),
            ('hungyen', 'Hưng Yên'),
            ('khanhhoa', 'Khánh Hòa'),
            ('kiengiang', 'Kiên Giang'),
            ('konturng', 'Kon Tum'),
            ('laocai', 'Lào Cai'),
            ('langson', 'Lạng Sơn'),
            ('laocai', 'Lào Cai'),
            ('lamdong', 'Lâm Đồng'),
            ('longan', 'Long An'),
            ('namdinh', 'Nam Định'),
            ('nghean', 'Nghệ An'),
            ('ninhbinh', 'Ninh Bình'),
            ('ninhthuan', 'Ninh Thuận'),
            ('phuquoc', 'Phú Quốc'),
            ('phutho', 'Phú Thọ'),
            ('quangbinh', 'Quảng Bình'),
            ('quangnam', 'Quảng Nam'),
            ('quangngai', 'Quảng Ngãi'),
            ('quangninh', 'Quảng Ninh'),
            ('quangtri', 'Quảng Trị'),
            ('saka', 'Sơn La'),
            ('tayninh', 'Tây Ninh'),
            ('thanhhoa', 'Thanh Hóa'),
            ('thodinh', 'Thái Dương'),
            ('thaitin', 'Thái Tiên'),
            ('thainguyen', 'Thái Nguyên'),
            ('tieucgai', 'Tiền Giang'),
            ('tràvinh', 'Trà Vinh'),
            ('tuyenquang', 'Tuyên Quang'),
            ('vinhphuc', 'Vĩnh Phúc'),
            ('vinhlong', 'Vĩnh Long'),
        ],
        string="Thành Phố",)
    receiver_country_id = fields.Many2one('res.country', string='Quốc Gia', default=241)
       
# ---------------------------------------------------------------------------------------------
    
    # Tạo mới User cho người dùng khi tạo Contact
    # Override phương thức create
    @api.model
    def create(self, vals):
        """Override create method to manage sender and receiver creation logic."""
        # Quản lý thông tin người dùng
        self.manage_user(vals)
        
        contact = super(ContactsInformation, self).create(vals)
        
        contact.name = "Đơn Hàng" +  str(contact.id)
        
        # Kiểm tra ràng buộc trong biểu mẫu
        self._check_product_info()
        
        contact._create_logistic_product()
    
        _logger.info(contact.name)
        return contact
    
    # -------------------------------AutoFill thông tin Khách hàng--------------------
    @api.onchange('sender_mobile')
    def _onchange_sender_mobile(self):
        if self.sender_mobile:
            # Tìm người dùng dựa trên số điện thoại
            sender_user = self.env['res.users'].search([('mobile', '=', self.sender_mobile)], limit=1)
            if sender_user:
                # Nếu tồn tại, điền thông tin
                self.sender_name = sender_user.name
                self.sender_email = sender_user.email
                self.sender_street = sender_user.partner_id.street
                self.sender_city = sender_user.partner_id.city
                self.sender_country_id = sender_user.partner_id.country_id

    @api.onchange('receiver_mobile')
    def _onchange_receiver_mobile(self):
        if self.receiver_mobile:
            # Tìm người dùng dựa trên số điện thoại
            receiver_user = self.env['res.users'].search([('mobile', '=', self.receiver_mobile)], limit=1)
            if receiver_user:
                # Nếu tồn tại, điền thông tin
                self.receiver_name = receiver_user.name
                self.receiver_email = receiver_user.email
                self.receiver_street = receiver_user.partner_id.street
                self.receiver_city = receiver_user.partner_id.city
                self.receiver_country_id = receiver_user.partner_id.country_id
    # --------------------------------------------------------------------------------
    
    # Quản lý thông tin người dùng
    def manage_user(self, vals):
        user = self.env.user  # Lấy user hiện tại
        client_group = self.env.ref('logistic.group_client') 
        
        # Kiểm tra quyền của user
        if user.has_group('logistic.group_employee') or user.has_group('logistic.group_user_pos'):
            # Nếu người dùng có quyền Employee hoặc là nhóm user_pos, kiểm tra số điện thoại của người gửi
            if 'sender_mobile' in vals:
                sender_mobile = vals['sender_mobile']
                
                # Kiểm tra người dùng tồn tại hay chưa
                sender_user = self.env['res.users'].search([('login', '=', sender_mobile)], limit=1)
                if not sender_user:
                    sender_user = self.env['res.users'].create({
                        'image_1920': vals.get('sender_profile_image', ''),
                        'name': vals.get('sender_name', ''),
                        'mobile': sender_mobile,
                        'login': sender_mobile,
                        'password': sender_mobile,  # Mật khẩu mặc định SDT
                        'email': vals.get('sender_email', ''),
                        'street': vals.get('sender_street', ''),
                        'city': vals.get('sender_city', ''),
                        'country_id': vals.get('sender_country_id', ''),
                        
                    })
                    # Thêm người dùng vào nhóm khách hàng
                    # sender_user.action_reset_password() # Yêu cầu đổi mật khẩu lần đầu
                
                # Phân quyền Client cho người gửi
                if client_group not in sender_user.groups_id:
                    sender_user.write({'groups_id': [(4, client_group.id)]})
                
                vals['sender_id'] = sender_user.id  # Gắn người gửi vào contact
        # ---------------------------------------------------------------------------    
            # Kiểm tra số điện thoại của người nhận 
            if 'receiver_mobile' in vals:
                receiver_mobile = vals['receiver_mobile'] 
                
                # Nếu chưa có người dùng thì tạo mới người dùng cho người nhận
                receiver_user = self.env['res.users'].search([('login', '=', receiver_mobile)], limit=1)
                if not receiver_user:
                    receiver_user = self.env['res.users'].create({
                        'name': vals.get('receiver_name', ''),
                        'mobile': receiver_mobile,
                        'login': receiver_mobile,
                        'password': receiver_mobile,  # Mật khẩu mặc định là SDT 
                        'email': vals.get('receiver_email', ''),
                        'street': vals.get('receiver_street', ''),
                        'city': vals.get('receiver_city', ''),
                        'country_id': vals.get('receiver_country_id', ''),
                    })
                    # receiver_user.action_reset_password() # Yêu cầu đổi mật khẩu lần đầu
                
                # Phân quyền Client cho người nhận
                if client_group not in receiver_user.groups_id:
                    receiver_user.write({'groups_id': [(4, client_group.id)]})
                    
                vals['receiver_id'] = receiver_user.id  # Gắn người nhận vào contact
    
    
    # Phương thức khi lưu thông tin đơn hàng, đảm bảo trạng thái thay đổi tương ứng
    def write(self, vals):
        """Xử lý việc thay đổi trạng thái khi đơn hàng được lưu."""
        res = super(ContactsInformation, self).write(vals)
                
        # Lưu thông tin kiện hàng
        self._create_logistic_product()
        
        if any(key in vals for key in ['product_name', 'product_weight', 'product_lengh', 'product_width', 'product_height']):
            self._create_logistic_product()
        
        _logger.info(f"Cập nhật logistic.contacts với ID: {self.id}")
        return res
    
        
    # Kiểm tra ràng buộc trong biểu mẫu
    @api.constrains('product_name', 'product_weight', 'product_lengh', 'product_width', 'product_height')
    def _check_product_info(self):
        """Kiểm tra ràng buộc dữ liệu."""
        for record in self:
            required_fields = ['product_name', 'product_weight', 'product_lengh', 'product_width', 'product_height']
            missing_fields = [field for field in required_fields if not getattr(record, field, None)]
            if missing_fields:
                raise ValidationError(_("Vui lòng điền đầy đủ thông tin: %s.") % ", ".join(missing_fields))
    
    
    # Phương thức xử lý khi nhấn nút "Gửi hàng" trong popup
    def confirm_shipping(self):
        """Xử lý xác nhận gửi hàng."""
        try:
                        
            # Thực hiện hiệu ứng thông báo
            effect = {
                'fadeout': 'slow',
                'message': _("Đơn hàng đã được gửi thành công!"),
                'type': 'rainbow_man',  # Loại thông báo
            }

            # Trả về hành động mở một form mới
            return {
                'effect': effect,  # Hiển thị thông báo
                'type': 'ir.actions.act_window',
                'res_model': 'logistic.contacts',  # Mở form model hiện tại
                'view_mode': 'form',
                'view_id': self.env.ref('logistic.form_view_logistic_contacts').id,
                'target': 'current',  # Mở form mới trong cùng tab
            }
        except Exception as e:
            _logger.error(f"Lỗi xác nhận gửi hàng: {str(e)}")
            raise ValidationError(_("Lỗi khi gửi hàng: ") + str(e))
    
    def _create_logistic_product(self):
        """Tạo thông tin kiện hàng trong logistic.products nếu chưa tồn tại."""
        for record in self:
            # Kiểm tra xem đã có bản ghi logistic.products liên kết chưa
            existing_product = self.env['logistic.products'].search([('contact_id', '=', record.id)], limit=1)
            
            if existing_product:
                # Cập nhật thông tin nếu đã tồn tại
                existing_product.write({
                    'order_code': record.order_code,
                    'sender_name': record.sender_name,
                    'sender_street': record.sender_street,
                    'receiver_name': record.receiver_name,
                    'receiver_street': record.receiver_street,
                    'product_name': record.product_name,
                    'product_weight': record.product_weight,
                    'product_lengh': record.product_lengh,
                    'product_width': record.product_width,
                    'product_height': record.product_height,
                    'properties_of_goods': record.properties_of_goods,
                    'sender_id': record.sender_id.id,
                    'receiver_id': record.receiver_id.id,
                })
                _logger.info(f"Cập nhật logistic.products cho contact_id: {record.id}")
            else:
                # Tạo mới nếu chưa tồn tại
                self.env['logistic.products'].create({
                    'contact_id': record.id,
                    'order_code': record.order_code,
                    'sender_name': record.sender_name,
                    'sender_street': record.sender_street,
                    'receiver_name': record.receiver_name,
                    'receiver_street': record.receiver_street,
                    'product_name': record.product_name,
                    'product_weight': record.product_weight,
                    'product_lengh': record.product_lengh,
                    'product_width': record.product_width,
                    'product_height': record.product_height,
                    'properties_of_goods': record.properties_of_goods,
                    'sender_id': record.sender_id.id,
                    'receiver_id': record.receiver_id.id,
                })
                _logger.info(f"Tạo mới logistic.products cho contact_id: {record.id}")
    
    # Lọc các đơn hàng cho từng người dùng có liên hệ
    @api.model
    def read(self, fields=None, load='_classic_read'):
        # Lấy số điện thoại của người dùng hiện tại
        user_mobile = self.env.user.mobile

        # Kiểm tra nếu người dùng là admin (admin có thể xem tất cả đơn hàng)
        is_admin = self.env.user.has_group('logistic.group_employee') or self.env.user.has_group('logistic.group_user_pos')

        # Lấy các bản ghi đơn hàng (Contact)
        records = super(ContactsInformation, self).read(fields, load)

        # Nếu là admin, cho phép xem tất cả các đơn hàng
        if is_admin:
            return records

        # Lọc các bản ghi mà người dùng hiện tại có quyền truy cập
        accessible_records = []
        for record in records:
            # Kiểm tra nếu người dùng là người gửi hoặc người nhận của đơn hàng này
            if (
                record['sender_mobile'] == user_mobile or 
                record['receiver_mobile'] == user_mobile
            ):
                accessible_records.append(record)

        # Nếu không có đơn hàng hợp lệ, ném lỗi truy cập
        if not accessible_records:
            raise AccessError("Bạn không có quyền truy cập vào đơn hàng này.")

        return accessible_records