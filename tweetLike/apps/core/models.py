from django.db import models

class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

        # By default, any model that inherits from 'TimestampedModel' 
        # Should be ordered in reverse-chronological order.
        # We can override this on a per-model basis as needed,
        # but reverse-chronological is good default ordering for 
        # most models.
        ordering = ['-created_at','-updated_at']