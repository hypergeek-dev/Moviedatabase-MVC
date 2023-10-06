from django.db import connections
import logging

logger = logging.getLogger(__name__)

class DatabaseErrorHandler:
    def db_for_read(self, model, **hints):
        try:
    
            with connections['default'].cursor() as cursor:
                cursor.execute("SELECT 1;")
        except Exception as e:
            logger.exception("Database error: %s", e)
            return None 
        return None

    def db_for_write(self, model, **hints):
        try:
     
            with connections['default'].cursor() as cursor:
                cursor.execute("SELECT 1;")
        except Exception as e:
            logger.exception("Database error: %s", e)
            return None  
        return None
