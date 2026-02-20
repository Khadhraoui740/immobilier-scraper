"""
Système de notification par email
"""
import os
import logging
import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from config import EMAIL_CONFIG, SEARCH_CONFIG

load_dotenv()
logger = logging.getLogger(__name__)


class EmailNotifier:
    """Classe pour envoyer des alertes par email"""
    
    def __init__(self):
        self.smtp_server = EMAIL_CONFIG['smtp_server']
        self.smtp_port = EMAIL_CONFIG['smtp_port']
        self.from_email = EMAIL_CONFIG['from_email']
        self.recipient_email = EMAIL_CONFIG['email']
        self.password = os.getenv('EMAIL_PASSWORD')
        
        if not self.password:
            logger.warning("EMAIL_PASSWORD non configuré dans .env")
    
    def send_alert(self, properties, search_name="Propriétés correspondant à votre recherche"):
        """Envoyer une alerte avec les propriétés trouvées"""
        if not properties:
            logger.info("Aucune propriété à notifier")
            return False
        
        if not self.password:
            logger.error("Mot de passe email non configuré")
            return False
        
        try:
            subject = f"🏠 {len(properties)} nouvelle(s) propriété(s) trouvée(s) - {search_name}"
            
            html_content = self._build_html_email(properties)
            
            message = MIMEMultipart('alternative')
            message['Subject'] = subject
            message['From'] = self.from_email
            message['To'] = self.recipient_email
            
            # Envoyer en HTML
            message.attach(MIMEText(html_content, 'html'))
            
            # Connexion et envoi
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.from_email, self.password)
                server.sendmail(
                    self.from_email,
                    self.recipient_email,
                    message.as_string()
                )
            
            logger.info(f"Email envoyé à {self.recipient_email} avec {len(properties)} propriétés")
            return True
        
        except smtplib.SMTPException as e:
            logger.error(f"Erreur SMTP lors de l'envoi d'email: {e}")
            return False
        except Exception as e:
            logger.error(f"Erreur lors de l'envoi d'email: {e}")
            return False
    
    def _build_html_email(self, properties):
        """Construire le contenu HTML de l'email"""
        html = f"""
        <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; background-color: #f5f5f5; }}
                    .container {{ max-width: 900px; margin: 0 auto; background-color: #fff; padding: 20px; }}
                    .header {{ background-color: #2c3e50; color: white; padding: 20px; border-radius: 5px; margin-bottom: 20px; }}
                    .property {{ border: 1px solid #ddd; padding: 15px; margin-bottom: 15px; border-radius: 5px; }}
                    .property-title {{ font-size: 18px; font-weight: bold; color: #2c3e50; margin-bottom: 10px; }}
                    .property-details {{ display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin: 10px 0; }}
                    .detail-item {{ padding: 5px; background-color: #f9f9f9; border-left: 3px solid #3498db; padding-left: 10px; }}
                    .price {{ font-size: 20px; font-weight: bold; color: #27ae60; }}
                    .location {{ color: #7f8c8d; }}
                    .dpe {{ display: inline-block; padding: 5px 10px; border-radius: 3px; font-weight: bold; }}
                    .dpe-a {{ background-color: #27ae60; color: white; }}
                    .dpe-b {{ background-color: #52be80; color: white; }}
                    .dpe-c {{ background-color: #f39c12; color: white; }}
                    .dpe-d {{ background-color: #e74c3c; color: white; }}
                    .dpe-e {{ background-color: #c0392b; color: white; }}
                    .button {{ display: inline-block; padding: 10px 20px; background-color: #3498db; color: white; text-decoration: none; border-radius: 3px; margin-top: 10px; }}
                    .footer {{ margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; color: #7f8c8d; font-size: 12px; }}
                    .criteria {{ background-color: #ecf0f1; padding: 10px; border-radius: 3px; margin-bottom: 20px; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>🏠 Alerte Propriétés Immobilières</h1>
                        <p>{len(properties)} nouvelle(s) propriété(s) trouvée(s)</p>
                    </div>
                    
                    <div class="criteria">
                        <strong>Critères de recherche:</strong><br>
                        Budget: {SEARCH_CONFIG['budget_min']:,} € - {SEARCH_CONFIG['budget_max']:,} €<br>
                        Zones: {', '.join(SEARCH_CONFIG['zones'])}<br>
                        DPE maximum: {SEARCH_CONFIG['dpe_max']}
                    </div>
        """
        
        for prop in properties[:20]:  # Limiter à 20 propriétés par email
            dpe_class = f"dpe-{prop.get('dpe', 'g').lower()}"
            html += f"""
                    <div class="property">
                        <div class="property-title">{prop.get('title', 'Sans titre')}</div>
                        <div class="location">{prop.get('location', 'Localisation inconnue')}</div>
                        
                        <div class="property-details">
                            <div class="detail-item">
                                <strong>Prix:</strong><br>
                                <span class="price">{prop.get('price', 'N/A'):,} €</span>
                            </div>
                            <div class="detail-item">
                                <strong>Surface:</strong><br>
                                {prop.get('surface', 'N/A')} m²
                            </div>
                            <div class="detail-item">
                                <strong>Pièces:</strong><br>
                                {prop.get('rooms', 'N/A')}
                            </div>
                            <div class="detail-item">
                                <strong>DPE:</strong><br>
                                <span class="dpe {dpe_class}">{prop.get('dpe', 'N/A')}</span>
                            </div>
                        </div>
                        
                        <div class="detail-item">
                            <strong>Source:</strong> {prop.get('source', 'Inconnue')}
                        </div>
                        
                        <a href="{prop.get('url', '#')}" class="button">Voir l'annonce →</a>
                    </div>
            """
        
        html += f"""
                    <div class="footer">
                        <p>Email généré automatiquement le {datetime.now().strftime('%d/%m/%Y à %H:%M')}</p>
                        <p>Vous recevez cet email car vous êtes inscrit au système d'alertes immobilières.</p>
                    </div>
                </div>
            </body>
        </html>
        """
        
        return html
    
    def send_daily_report(self, stats, properties=None):
        """Envoyer un rapport quotidien"""
        if not self.password:
            logger.error("Mot de passe email non configuré")
            return False
        
        try:
            subject = f"📊 Rapport quotidien - Scraping immobilier {datetime.now().strftime('%d/%m/%Y')}"
            
            html_content = self._build_report_html(stats, properties or [])
            
            message = MIMEMultipart('alternative')
            message['Subject'] = subject
            message['From'] = self.from_email
            message['To'] = self.recipient_email
            
            message.attach(MIMEText(html_content, 'html'))
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.from_email, self.password)
                server.sendmail(
                    self.from_email,
                    self.recipient_email,
                    message.as_string()
                )
            
            logger.info(f"Rapport quotidien envoyé à {self.recipient_email}")
            return True
        
        except Exception as e:
            logger.error(f"Erreur lors de l'envoi du rapport: {e}")
            return False
    
    def _build_report_html(self, stats, recent_properties):
        """Construire le contenu HTML du rapport"""
        by_source = stats.get('by_source', {})
        by_status = stats.get('by_status', {})
        
        html = f"""
        <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; }}
                    .container {{ max-width: 900px; margin: 0 auto; background-color: #fff; padding: 20px; }}
                    .header {{ background-color: #34495e; color: white; padding: 20px; border-radius: 5px; margin-bottom: 20px; }}
                    table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
                    th, td {{ padding: 10px; text-align: left; border-bottom: 1px solid #ddd; }}
                    th {{ background-color: #34495e; color: white; }}
                    .stat-box {{ background-color: #ecf0f1; padding: 15px; border-radius: 5px; margin: 10px 0; }}
                    .stat-value {{ font-size: 24px; font-weight: bold; color: #2c3e50; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>📊 Rapport Quotidien</h1>
                        <p>{datetime.now().strftime('%d/%m/%Y')}</p>
                    </div>
                    
                    <h2>Statistiques Globales</h2>
                    <div class="stat-box">
                        <div>Total de propriétés:</div>
                        <div class="stat-value">{stats.get('total_properties', 0)}</div>
                    </div>
        """
        
        if by_source:
            html += "<h3>Par Source</h3><table><tr><th>Source</th><th>Nombre</th></tr>"
            for source, count in by_source.items():
                html += f"<tr><td>{source}</td><td>{count}</td></tr>"
            html += "</table>"
        
        if by_status:
            html += "<h3>Par Statut</h3><table><tr><th>Statut</th><th>Nombre</th></tr>"
            for status, count in by_status.items():
                html += f"<tr><td>{status}</td><td>{count}</td></tr>"
            html += "</table>"
        
        if stats.get('avg_price'):
            html += f"""
                    <h2>Statistiques Prix</h2>
                    <div class="stat-box">
                        <p>Prix moyen: <strong>{stats.get('avg_price'):,.0f} €</strong></p>
                        <p>Prix min: <strong>{stats.get('min_price'):,} €</strong></p>
                        <p>Prix max: <strong>{stats.get('max_price'):,} €</strong></p>
                    </div>
            """
        
        html += """
                </div>
            </body>
        </html>
        """
        
        return html
