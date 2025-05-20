import firebase_admin
from firebase_admin import credentials, messaging
from typing import List, Dict, Any, Optional
from models import FCMToken

class FCMHelper:
    """Lớp hỗ trợ gửi thông báo qua Firebase Cloud Messaging API v1."""
    
    # Đường dẫn đến file chứa khóa service account
    SERVICE_ACCOUNT_KEY_PATH = "duong-ef747-firebase-adminsdk-r6np1-855dec2ead.json"
    
    # Biến lưu trạng thái khởi tạo
    _initialized = False
    
    @classmethod
    def _ensure_initialized(cls):
        """Đảm bảo Firebase Admin SDK đã được khởi tạo."""
        if not cls._initialized:
            cred = credentials.Certificate(cls.SERVICE_ACCOUNT_KEY_PATH)
            firebase_admin.initialize_app(cred)
            cls._initialized = True
    
    @classmethod
    def send_notification(cls,
                         tokens: List[str], 
                         title: str, 
                         body: str, 
                         data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Gửi thông báo đến một hoặc nhiều token FCM.
        
        Args:
            tokens: Danh sách token FCM
            title: Tiêu đề thông báo
            body: Nội dung thông báo
            data: Dữ liệu bổ sung cho thông báo (optional)
            
        Returns:
            Dict: Phản hồi từ FCM
        """
        cls._ensure_initialized()
        
        if not tokens:
            return {"success": False, "error": "No FCM tokens provided"}
        
        # Tạo thông báo
        notification = messaging.Notification(
            title=title,
            body=body
        )
        
        # Kết quả
        success_count = 0
        failure_count = 0
        response_details = []
        
        # Gửi thông báo đến từng token
        for token in tokens:
            try:
                message = messaging.Message(
                    notification=notification,
                    data=data,
                    token=token
                )
                
                # Gửi thông báo
                response = messaging.send(message)
                success_count += 1
                response_details.append({"token": token, "success": True, "message_id": response})
            except Exception as e:
                failure_count += 1
                response_details.append({"token": token, "success": False, "error": str(e)})
        
        return {
            "success": success_count > 0,
            "success_count": success_count,
            "failure_count": failure_count,
            "total": len(tokens),
            "details": response_details
        }
    
    @classmethod
    def send_notification_to_user(cls, 
                                 db, 
                                 user_id: int, 
                                 title: str, 
                                 body: str, 
                                 notification_id: int = None,
                                 type: str = None,
                                 image_url: str = None) -> Dict[str, Any]:
        """
        Gửi thông báo đến một người dùng cụ thể.
        
        Args:
            db: Database session
            user_id: ID của người dùng
            title: Tiêu đề thông báo
            body: Nội dung thông báo
            notification_id: ID của thông báo trong DB (optional)
            type: Loại thông báo (optional)
            image_url: URL của hình ảnh (optional)
            
        Returns:
            Dict: Phản hồi từ FCM
        """
        # Lấy danh sách FCM token của user
        tokens = db.query(FCMToken.token).filter(FCMToken.user_id == user_id).all()
        tokens = [token[0] for token in tokens]
        
        if not tokens:
            return {"success": False, "error": "User has no FCM tokens"}
        
        # Chuẩn bị dữ liệu
        data = {
            "title": title,
            "message": body
        }
        
        if notification_id:
            data["notification_id"] = str(notification_id)
        
        if type:
            data["type"] = type
            
        if image_url:
            data["image_url"] = image_url
        
        # Gửi thông báo
        return cls.send_notification(tokens, title, body, data)