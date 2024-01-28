<!-- Views/Components/tableau.php -->
<?php
function afficheTableau($tab) {
    if (is_array($tab) && count($tab) > 0) {
        echo '<table>';
        echo '<tr>'; // Les entêtes des colonnes

        foreach ($tab[0] as $colonne => $valeur) {
            echo "<th>$colonne</th>";
        }
        echo "</tr>\n";

        foreach ($tab as $ligne) {
            echo '<tr>';
            foreach ($ligne as $entete => $cellule) {
                if ($entete == "Image") {
                    echo '<td><img class="image_table" src="img/' . $cellule . '" alt="' . $cellule . '"/></td>';
                } else if ($entete == "Prix") {
                    echo "<td>$cellule €</td>";
                } else {
                    echo "<td>$cellule</td>";
                }
            }
            echo "</tr>\n";
        }
        echo '</table>';
    } else {
        echo "Aucune donnée à afficher.";
    }
}
?>
