# Pybot_json
Un bot python capable de pouvoir lire, editer, supprimer et créer des fiches d'information a l'aide de json. Ceci est encore une pré-alpha

## Fonctionalitées
### Créer un dossier pour une personne
Utilistation : ajoute une nouvelle personne <br/>
Consequence : Va créer un nouveau dossier sous la forme <nom_prenom> qui contiendra le template de data

### Supprimer un dossier
Utilisation : supprime une personne <br/>
Conséquence : Va supprimer et le contenu de la personne souhaiter
Attention, il faut que la personne soit ciblée au préalabe

### Cibler une personne
Utilisation : Cible une personne <br/>
Conséquence : La personne ciblée sera traiter dans les fonctions
La plupart des fonctions necessites une cible au préalable.

### Lire les informations
Utilisation : donne moi les informations <br/>
Conséquence : Affiche les informations éditée (ne prend pas en compte les colones vides)

### Editer les informations
Utilisation : édite les informations <br/>
Conséquence : Va modifier le dictionnaire python et le retransformer en json
