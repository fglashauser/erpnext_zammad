from .customer_service import CustomerService
from ..data import ZammadConnector
from ..zammad_settings import ZammadSettings
from .. import helpers
import frappe

class ArticleService:
    """Service for article related operations in Zammad.
    """
    def __init__(self, zammad_connector : ZammadConnector = None):
        """Initializes ArticleService.
        If zammad_connector is not provided, it will create a new one with default settings.
        
        Args:
            zammad_connector (ZammadConnector, optional): ZammadConnector instance. Defaults to None.
        """
        self.settings = ZammadSettings()
        self.zammad = zammad_connector if zammad_connector else ZammadConnector()
    
    
    def get_article(self, article_id: int):
        """Returns the Zammad article with the given id.
        
        Args:
            article_id (int): Article id.
        Returns:
            dict: Article.
        """
        if not article_id:
            return None

        # Get the article
        article = self.zammad.api.ticket_article.find(article_id)
        
        # Return the article
        return article