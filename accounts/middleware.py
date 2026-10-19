"""
MongoEngine Session Authentication Middleware
"""
import logging
from bson import ObjectId
from accounts.documents import User

logger = logging.getLogger(__name__)

class MongoAuthMiddleware:
    """
    Middleware that reads 'user_id' from the signed session,
    loads the User document from MongoDB, and attaches it to request.current_user.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user_id = request.session.get('user_id') or request.session.get('_mongo_user_id')
        user = None

        if user_id:
            try:
                user = User.objects(id=ObjectId(user_id), is_active=True).first()
                if not user:
                    # User deleted or suspended
                    request.session.flush()
            except Exception as exc:
                logger.error(f"[AUTH MIDDLEWARE] Error resolving user_id {user_id}: {exc}")
                user = None

        request.current_user = user
        response = self.get_response(request)
        return response
