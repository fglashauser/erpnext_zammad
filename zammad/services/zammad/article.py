from . import Service
import frappe

class Article(Service):
    """Service for article related operations in Zammad.
    """
    def get_article(self, article_id: int) -> dict | None:
        """Returns the Zammad article with the given id.
        
        Args:
            article_id (int): Article id.
        Returns:
            dict: Article.
        """
        if not article_id:
            return None

        # Get the article
        article = self.api.ticket_article.find(article_id)
        
        # Return the article
        return article
    

    def get_article_body(self, article_id: int) -> str | None:
        """Returns the body of the article with the given id.
        
        Args:
            article_id (int): Article id.
        Returns:
            str: Body.
        """
        # Get the article
        article = self.get_article(article_id)
        
        # Return the body
        return article.get('body', None) if article else None
    

    def get_ticket_description(self, ticket: dict) -> str | None:
        """Returns the description of the ticket with the given id.
        
        Args:
            ticket_id (int): Ticket id.
        Returns:
            str: Description.
        """
        return self.get_article_body(min(ticket.get('article_ids', []))) if ticket else None