# README (fr) - TP2 PYTHON 

## Quelques particularités

- Lorsqu'on entraine pour une fenetre de taille 7, les coocurrences sont insérées dans la DB pour les distances de 1, 2, et 3 (fenetre 3,5,7).
Donc seulement besoin d'entrainer une fois a la taille maximale que l'on souhaitera utiliser. Quand on construit sa matrice, on peut prendre
les coocs. de notre choix selon la distance. 
- Lors de l'entrainement, on fait seulement des insertions de coocs du style : (id1, id2, distance, 1). La meme coocurrence id1, id2, distance peut apparaitre plusieurs fois a la même fréquence si la DB n'est pas "triée". Voir ci-dessous.
- Si la DB devient trop grosse/lente lorsqu'on exporte les coocs., on peut utiliser la fonction trimDB (__parametre -c__, pour compact, utilisé seul).
La fonction prend toutes les coocs. de la table, et compacte le tout dans un dictionnaire qui fait le décompte, lequel est ensuite réinséré dans la table num_coocs remise à neuf (from scratch). Idéal de le faire après plusieurs textes (10secondes a peu pres). Il en retourne une table num_coocs de meme taille (row count) que word_dict. L'operation ameliore considerablement le setup time de la matrice de coocs.
ex : `python main.py -c`
- Paramètre pour remettre la BD à zero: __--reset__
ex:
`python src/main.py --reset`
`Reset DB? Y for yes : Y`