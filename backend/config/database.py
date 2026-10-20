"""
EV Share - MongoDB Database Connection Module
Connects to MongoDB using MongoEngine.
Falls back to mongomock if live server is unreachable in development.
"""
import logging
import os
import sys
import pymongo
import mongoengine
import mongomock

logger = logging.getLogger(__name__)

_DB_CONNECTION = None
_IS_MOCK_DB = False

def get_db_status():
    global _IS_MOCK_DB
    return {
        "is_mock": _IS_MOCK_DB,
        "connected": _DB_CONNECTION is not None,
    }

def connect_db():
    global _DB_CONNECTION, _IS_MOCK_DB
    
    if _DB_CONNECTION is not None:
        return _DB_CONNECTION
        
    uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017/ev_share")
    db_name = os.getenv("MONGODB_DATABASE", "ev_share")
    
    mongoengine.disconnect_all()
    
    # Check if testing or explicit mock requested
    if os.getenv("USE_MOCK_DB", "").lower() in ("true", "1", "yes"):
        logger.info("[DB] Explicit mock requested. Connecting via mongomock.")
        _DB_CONNECTION = mongoengine.connect(
            db_name,
            host="mongodb://localhost",
            mongo_client_class=mongomock.MongoClient,
            alias="default"
        )
        _IS_MOCK_DB = True
        return _DB_CONNECTION

    try:
        # Test connection with 1500ms timeout
        client = pymongo.MongoClient(uri, serverSelectionTimeoutMS=1500)
        client.admin.command("ping")
        _DB_CONNECTION = mongoengine.connect(db=db_name, host=uri, alias="default")
        _IS_MOCK_DB = False
        logger.info(f"[DB] Successfully connected to live MongoDB: {uri}")
    except Exception as exc:
        logger.warning(
            f"[DB] Live MongoDB unreachable at {uri} ({exc}). "
            "Falling back to in-memory mongomock for reliable local development and testing."
        )
        _DB_CONNECTION = mongoengine.connect(
            db_name,
            host="mongodb://localhost",
            mongo_client_class=mongomock.MongoClient,
            alias="default"
        )
        _IS_MOCK_DB = True
        
    # Auto-seed mock database if empty during web execution
    if _IS_MOCK_DB and "pytest" not in sys.modules and not any("test" in arg for arg in sys.argv):
        try:
            from accounts.documents import User
            if User.objects.count() == 0:
                import seed_data
                seed_data.seed_database()
        except Exception as seed_exc:
            logger.warning(f"[DB] Auto-seed failed: {seed_exc}")

    return _DB_CONNECTION

