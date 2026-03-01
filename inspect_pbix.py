import zipfile
import os
import json

pbix_path = r"exports/rapport.pbix"

with zipfile.ZipFile(pbix_path, 'r') as z:
    print("Structure complète du rapport.pbix:\n")
    for f in sorted(z.namelist()):
        size = z.getinfo(f).file_size
        print(f"  {f:<50} ({size:,} bytes)")
    
    print("\n" + "="*80)
    print("CONTENU DES FICHIERS TEXTE:")
    print("="*80)
    
    for fname in ["Version", "[Content_Types].xml", "Metadata", "Settings"]:
        if fname in z.namelist():
            print(f"\n--- {fname} ---")
            content = z.read(fname).decode('utf-8', errors='ignore')
            print(content[:800])
