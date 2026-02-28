"""
Prix réalistes des appartements par commune en Île-de-France
Basé sur les données de marché réelles (2026)
"""

# Prix au m² moyen par commune (en EUR)
PRIX_PAR_M2 = {
    # Paris (75) - très cher
    'Paris 1er': 15000,
    'Paris 2e': 14500,
    'Paris 3e': 13500,
    'Paris 4e': 14000,
    'Paris 5e': 12500,
    'Paris 6e': 13500,
    'Paris 7e': 14000,
    'Paris 8e': 15500,
    'Paris 9e': 12000,
    'Paris 10e': 10500,
    'Paris 11e': 11000,
    'Paris 12e': 10000,
    'Paris 13e': 9500,
    'Paris 14e': 11000,
    'Paris 15e': 10500,
    'Paris 16e': 13500,
    'Paris 17e': 11000,
    'Paris 18e': 9500,
    'Paris 19e': 8500,
    'Paris 20e': 8000,
    
    # Hauts-de-Seine (92) - cher
    'Nanterre': 5500,
    'Boulogne-Billancourt': 9000,
    'Courbevoie': 7500,
    'Neuilly-sur-Seine': 10000,
    'Levallois-Perret': 7000,
    'Issy-les-Moulineaux': 7500,
    'Clichy': 6000,
    'Colombes': 5500,
    'Rueil-Malmaison': 7000,
    'Puteaux': 7500,
    'Antony': 6500,
    'Asnières-sur-Seine': 6500,
    'Clamart': 6500,
    'Montrouge': 7000,
    'Suresnes': 7000,
    'Châtenay-Malabry': 6000,
    'Meudon': 6000,
    'Fontenay-aux-Roses': 6000,
    'Garches': 6500,
    'Sceaux': 6000,
    
    # Val-de-Marne (94) - modéré
    'Créteil': 4500,
    'Vitry-sur-Seine': 4000,
    'Champigny-sur-Marne': 4500,
    'Saint-Maur-des-Fossés': 5500,
    'Ivry-sur-Seine': 4500,
    'Maisons-Alfort': 5000,
    'Fontenay-sous-Bois': 5000,
    'Villejuif': 4500,
    'Vincennes': 6500,
    'Nogent-sur-Marne': 5500,
    'Le Kremlin-Bicêtre': 4500,
    'Alfortville': 4000,
    'Charenton-le-Pont': 4500,
    'Cachan': 4500,
    'Thiais': 4000,
    'Choisy-le-Roi': 3500,
    'Saint-Maurice': 5000,
    'Bry-sur-Marne': 5000,
    'Joinville-le-Pont': 5000,
    'Chennevières-sur-Marne': 4500,
    
    # Essonne (91) - moins cher
    'Évry-Courcouronnes': 3500,
    'Corbeil-Essonnes': 3000,
    'Massy': 4000,
    'Savigny-sur-Orge': 3500,
    'Sainte-Geneviève-des-Bois': 3500,
    'Viry-Châtillon': 3000,
    'Athis-Mons': 3000,
    'Palaiseau': 4500,
    'Yerres': 3500,
    'Draveil': 3500,
    'Ris-Orangis': 3000,
    'Grigny': 2500,
    'Brunoy': 3500,
    'Les Ulis': 3500,
    'Montgeron': 3000,
    'Étampes': 2500,
    'Longjumeau': 3500,
    'Brétigny-sur-Orge': 3000,
    'Gif-sur-Yvette': 4000,
    'Orsay': 4500,
    
    # Seine-et-Marne (77) - moins cher
    'Meaux': 3500,
    'Chelles': 3500,
    'Melun': 3000,
    'Pontault-Combault': 3500,
    'Savigny-le-Temple': 3000,
    'Champs-sur-Marne': 3500,
    'Torcy': 3500,
    'Combs-la-Ville': 3000,
    'Le Mée-sur-Seine': 2500,
    'Bussy-Saint-Georges': 3000,
    'Roissy-en-Brie': 3000,
    'Lagny-sur-Marne': 3000,
    'Ozoir-la-Ferrière': 3500,
    'Fontainebleau': 4000,
    'Montereau-Fault-Yonne': 2500,
    'Mitry-Mory': 3000,
    'Noisiel': 3500,
    'Dammarie-les-Lys': 2500,
    'Villeparisis': 3000,
    'Provins': 2000,
    
    # Yvelines (78) - moins cher
    'Versailles': 6000,
    'Sartrouville': 4000,
    'Mantes-la-Jolie': 2500,
    'Saint-Germain-en-Laye': 5500,
    'Poissy': 3500,
    'Montigny-le-Bretonneux': 3500,
    'Conflans-Sainte-Honorine': 3000,
    'Les Mureaux': 2500,
    'Plaisir': 3000,
    'Houilles': 4500,
    'Trappes': 3000,
    'Chatou': 5000,
    'Le Chesnay-Rocquencourt': 5500,
    'Guyancourt': 3500,
    'Rambouillet': 3500,
    'Élancourt': 3000,
    'Maisons-Laffitte': 5500,
    'Viroflay': 5500,
    'Vélizy-Villacoublay': 4500,
    'Achères': 3500,
    'Marly-le-Roi': 5500,
    'Carrières-sous-Poissy': 3500,
}


def get_prix_realiste(commune: str, surface: float) -> float:
    """
    Calculer un prix réaliste pour un appartement
    
    Args:
        commune: Nom de la commune
        surface: Surface en m²
        
    Returns:
        Prix estimé en EUR
    """
    # Obtenir le prix au m² pour la commune
    prix_m2 = PRIX_PAR_M2.get(commune, 5000)  # Défaut: 5000€/m²
    
    # Calculer le prix: base + variation aléatoire
    import random
    
    prix_base = prix_m2 * surface
    
    # Ajouter une variation de ±15% pour plus de réalisme
    variation = random.uniform(0.85, 1.15)
    prix_final = prix_base * variation
    
    return round(prix_final, 0)


def get_surface_realiste() -> float:
    """
    Générer une surface réaliste pour un appartement (30-120 m²)
    """
    import random
    return float(random.randint(30, 120))
