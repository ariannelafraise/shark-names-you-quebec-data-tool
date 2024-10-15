# Shark Names You - Quebec Data Python Tools 
A set of python tools for analyzing and transforming Données Québec's data on names (with pandas):  
> https://donneesquebec.ca/recherche/fr/dataset/banque-de-prenoms-garcons  
> https://donneesquebec.ca/recherche/fr/dataset/banque-de-prenoms-filles  
  
## Current tools:  
### `generate_lists.py`
Makes three lists: girls, boys and both. Takes a given number of most used names from both datasets
Renames the columns `Prenom_feminin` and `Prenom_masculin` to `Name`

Example output:
`girl_names.csv`
```csv
Name,Total  
STEPHANIE,21416  
CATHERINE,19981  
EMILIE,17341  
JESSICA,16863  
AUDREY,16759
...
```
