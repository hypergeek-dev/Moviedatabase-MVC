import logging

logger = logging.getLogger(__name__)

class DatabaseErrorHandler:
    def db_for_read(self, model, **hints):
        try:
            # Attempt to see if the database is available
            model.objects.last()
        except Exception as e:
            logger.exception("Database error: %s", e)
            return None  # Return None to use the default database
        return None

    def db_for_write(self, model, **hints):
        try:
            # Attempt to see if the database is available
            model.objects.last()
        except Exception as e:
            logger.exception("Database error: %s", e)
            return None  # Return None to use the default database
        return None
