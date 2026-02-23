"""
Liste des communes par département pour générer des données réalistes
"""

# Communes principales par département
COMMUNES_PAR_DEPARTEMENT = {
    'Paris': [
        'Paris 1er', 'Paris 2e', 'Paris 3e', 'Paris 4e', 'Paris 5e',
        'Paris 6e', 'Paris 7e', 'Paris 8e', 'Paris 9e', 'Paris 10e',
        'Paris 11e', 'Paris 12e', 'Paris 13e', 'Paris 14e', 'Paris 15e',
        'Paris 16e', 'Paris 17e', 'Paris 18e', 'Paris 19e', 'Paris 20e'
    ],
    'Hauts-de-Seine': [
        'Nanterre', 'Boulogne-Billancourt', 'Courbevoie', 'Neuilly-sur-Seine',
        'Levallois-Perret', 'Issy-les-Moulineaux', 'Clichy', 'Colombes',
        'Rueil-Malmaison', 'Puteaux', 'Antony', 'Asnières-sur-Seine',
        'Clamart', 'Montrouge', 'Suresnes', 'Châtenay-Malabry', 'Meudon',
        'Fontenay-aux-Roses', 'Garches', 'Sceaux'
    ],
    'Val-de-Marne': [
        'Créteil', 'Vitry-sur-Seine', 'Champigny-sur-Marne', 'Saint-Maur-des-Fossés',
        'Ivry-sur-Seine', 'Maisons-Alfort', 'Fontenay-sous-Bois', 'Villejuif',
        'Vincennes', 'Nogent-sur-Marne', 'Le Kremlin-Bicêtre', 'Alfortville',
        'Charenton-le-Pont', 'Cachan', 'Thiais', 'Choisy-le-Roi', 'Saint-Maurice',
        'Bry-sur-Marne', 'Joinville-le-Pont', 'Chennevières-sur-Marne'
    ],
    'Essonne': [
        'Évry-Courcouronnes', 'Corbeil-Essonnes', 'Massy', 'Savigny-sur-Orge',
        'Sainte-Geneviève-des-Bois', 'Viry-Châtillon', 'Athis-Mons', 'Palaiseau',
        'Yerres', 'Draveil', 'Ris-Orangis', 'Grigny', 'Brunoy', 'Les Ulis',
        'Montgeron', 'Étampes', 'Longjumeau', 'Brétigny-sur-Orge', 'Gif-sur-Yvette',
        'Orsay'
    ],
    'Seine-et-Marne': [
        'Meaux', 'Chelles', 'Melun', 'Pontault-Combault', 'Savigny-le-Temple',
        'Champs-sur-Marne', 'Torcy', 'Combs-la-Ville', 'Le Mée-sur-Seine',
        'Bussy-Saint-Georges', 'Roissy-en-Brie', 'Lagny-sur-Marne', 'Ozoir-la-Ferrière',
        'Fontainebleau', 'Montereau-Fault-Yonne', 'Mitry-Mory', 'Noisiel',
        'Dammarie-les-Lys', 'Villeparisis', 'Provins'
    ],
    'Yvelines': [
        'Versailles', 'Sartrouville', 'Mantes-la-Jolie', 'Saint-Germain-en-Laye',
        'Poissy', 'Montigny-le-Bretonneux', 'Conflans-Sainte-Honorine', 'Les Mureaux',
        'Plaisir', 'Houilles', 'Trappes', 'Chatou', 'Le Chesnay-Rocquencourt',
        'Guyancourt', 'Rambouillet', 'Élancourt', 'Maisons-Laffitte', 'Viroflay',
        'Vélizy-Villacoublay', 'Achères', 'Marly-le-Roi', 'Carrières-sous-Poissy'
    ]
}

# Code postal par département
CODES_POSTAUX = {
    'Paris': '75',
    'Hauts-de-Seine': '92',
    'Val-de-Marne': '94',
    'Essonne': '91',
    'Seine-et-Marne': '77',
    'Yvelines': '78'
}


def get_commune(departement):
    """
    Retourne une commune aléatoire pour un département donné
    
    Args:
        departement: Nom du département (ex: 'Yvelines', 'Val-de-Marne')
    
    Returns:
        str: Nom de la commune
    """
    import random
    
    if departement in COMMUNES_PAR_DEPARTEMENT:
        return random.choice(COMMUNES_PAR_DEPARTEMENT[departement])
    
    # Fallback si département inconnu
    return departement


def get_departement_from_code(code):
    """
    Retourne le nom du département à partir du code postal
    
    Args:
        code: Code département (ex: '75', '92')
    
    Returns:
        str: Nom du département
    """
    for dept, dept_code in CODES_POSTAUX.items():
        if dept_code == code:
            return dept
    return None


def get_code_postal(departement):
    """
    Retourne le code postal d'un département
    
    Args:
        departement: Nom du département
    
    Returns:
        str: Code postal (ex: '75', '92')
    """
    return CODES_POSTAUX.get(departement, '00')
