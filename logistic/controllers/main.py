from odoo import http  # Module để xử lý HTTP requests
from odoo.http import request
import json  # Module để xử lý JSON

from odoo.exceptions import ValidationError
from odoo import _

class ContactsInformationAPI(http.Controller):
    
    # Định nghĩa class kế thừa từ http.Controller để tạo REST API
    
    # Quản lý người dùng (Tạo User người dùng)
    @http.route('/api/logistic.contacts/userManager', auth='user', type='json', methods=['POST'])
    def user_manager(self, **kwargs):
        """API để quản lý người dùng (người gửi hoặc người nhận) theo số điện thoại."""
        try:
            if 'sender_mobile' not in kwargs and 'receiver_mobile' not in kwargs:
                return {'status': 'error', 'message': 'Thiếu trường bắt buộc: sender_mobile hoặc receiver_mobile'}

            # Gọi phương thức manage_user từ model ContactsInformation
            vals = kwargs
            contact_model = request.env['logistic.contacts']
            contact_model.manage_user(vals)

            return {
                'status': 'success',
                'message': 'Quản lý người dùng đã hoàn thành thành công'
            }
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    # Kiểm tra tính ràng buộc dữ liệu
    @http.route('/api/logistic.contacts/checkProductInfo', auth='user', type='json', methods=['POST'])
    def check_product_info(self, **kwargs):
        """API để kiểm tra thông tin sản phẩm trước khi tạo hoặc cập nhật đơn hàng."""
        try:
            # Kiểm tra dữ liệu bắt buộc
            required_fields = ['product_name', 'product_weight', 'product_lengh', 'product_width', 'product_height']
            missing_fields = [field for field in required_fields if field not in kwargs or not kwargs[field]]

            if missing_fields:
                return {
                    'status': 'error',
                    'message': f"Vui lòng điền đầy đủ thông tin: {', '.join(missing_fields)}"
                }

            # Gọi phương thức _check_product_info từ model ContactsInformation
            contact_model = request.env['logistic.contacts']
            contact_model._check_product_info()

            return {
                'status': 'success',
                'message': 'Thông tin sản phẩm đã được kiểm tra thành công'
            }

        except ValidationError as e:
            return {
                'status': 'error',
                'message': f"Kiểm tra không hợp lệ: {str(e)}"
            }
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
        
    @http.route('/api/logistic.contacts', auth='user', type='json', methods=['POST'])
    def create_ID(self, **kwargs):
        """Tạo mới mã đơn hàng"""
        try:
            # Kiểm tra trường bắt buộc
            if 'id' not in kwargs:
                return {'status': 'error', 'message': 'Missing required field: id'}
            
            order_id = int(kwargs.get('id'))
            order_code = kwargs.get('order_code', None)

            # Lấy đơn hàng từ database
            order = request.env['logistic.contacts'].browse(order_id)
            
            if not order:
                return {'status': 'error', 'message': 'Không tìm thấy đơn hàng hiện tại'}

            # Kiểm tra nếu mã thẻ đã tồn tại trong một đơn hàng khác
            if order_code:
                existing_order = request.env['logistic.contacts'].search([
                    ('order_code', '=', order_code),
                    ('id', '!=', order_id)
                ])
                if existing_order:
                    return {
                        'status': 'error',
                        'message': f"Mã đơn hàng đã tồn tại ở đơn hàng có id là: '{existing_order.id}'"
                    }
            
            # Trả về thông tin đơn hàng nếu đã có mã thẻ
            if order.order_code and not order_code:
                return {
                    'status': 'success',
                    'message': 'Đơn hàng đã tồn tại',
                    'data': {
                        'order_code': order.order_code,
                    }
                }

            # Nếu chưa có order_code và có order_code mới, cập nhật thông tin
            if order_code:
                order.write({'order_code': order_code})
                return {
                    'status': 'success',
                    'message': 'Cập nhật mã đơn hàng thành công!',
                    'data': {
                        'order_code': order_code,
                    }
                }

            return {'status': 'error', 'message': 'Invalid operation'}
            
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
        
        
    @http.route('/api/logistic.contacts/getCountryId', type='json', auth='user')
    def get_country_id(self, country_name):
        country = request.env['res.country'].search([('name', '=', country_name)], limit=1)
        if not country:
            return {'status': 'error', 'message': f'Quốc gia "{country_name}" không tồn tại'}
        return {'status': 'success', 'data': {'country_id': country.id}}
    
    # Cập nhật lại `resId` sau khi kiểm tra người dùng
    # @http.route('/api/logistic.contacts/updateOrGetId', type='json', auth='user')
    # def update_ID(self, **kwargs):
    #     """overide here"""
    #     try:
    #         order_id = kwargs.get('id')
    #         if not order_id:
    #             return {'status': 'error', 'message': 'Thiếu trường ID'}
            
    #         order = request.env['logistic.contacts'].browse(int(order_id))
    #         if not order.exists():
    #             return {'status': 'error', 'message': 'Không tìm thấy đơn hàng'}
            
    #         return {'status': 'success', 'data': {'id': order.id}}
    #     except Exception as e:
    #         return {'status': 'error', 'message': f'Lỗi xảy ra: {str(e)}'}