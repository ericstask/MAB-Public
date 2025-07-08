from django.db import models

class ClientRelationsPermissions(models.Model):
    """
    Dummy model for defining custom permission related to Client Relations.
    """

    class Meta:
        managed = False  # don't create the model in the database
        permissions = [
            ("access_client_relations", "Can access the Client Relations section"),
        ]
        