fablab-inkscape-plugins
=======================

Collection de plugins inkscape utiles ans un fablab

## Utiles pour la decoupeuse laser

### Générateur de boite
Disponible dans `Extension > Fablab > Générer une boite à encoches`, ce generateur est une réimplementation pour inkscape du [générateur de boite en javascript](http://cyberweb.cite-sciences.fr/fablab/tools/svg-box-generator/). Il vous permet les formes svg necessaire a la contruction d'un boite correspondant au dimentions que vosu indiquerez.

### Générateur ligne d'encoche
Disponible dans `Extension > Fablab > Générer une ligne d'encoches`, c'est en fait un extrait du générateur de boite qui ne vous génère qu'une seule ligne d'encoches, ce qui peut être utile lors de la construction manuelle de structure plus complexes que de simple "boites". Deux ligne sont en fait générées qui correcposndent au deux arete s'emboitent l'une dans l'autre.

### Sortie de Fichiers .tsf (Trotec Spool File)
Les découpeuses laser TROTEC utilisent des fichiers tsf pour la découpe/gravure. La seule possibilité jusqu'ici était d'utiliser le driver d'impression fournis par Trotec (fermé, propriétaitre et compatible uniquement Window) pour générer ces fichiers. Ce plugin essaye de proposer un alternative permettant d'enregistrer votre document au format `.tsf` pour ces decoupeuses laser à partir d'inkscape et donc de n'importe quel OS (il reste obligatoire d'utiliser le Logiciel JobControl sous windows pour piloter la machine).

⚠ Ce plugin est pour le moment en version Beta, utilisable probablement non dépourvu de bugs. 

Quelques trucs à savoir : 
* Nécessite d'avoir image magick d'installé
* Testé sous GNU/Linux (mint,ubuntu,...) et un peu sous windows7 mais devrait fonctionner aussi sous freebsd et macosx
* Il donne acces à l'enregistrement de fichiers au format `.tsf`
* Aussi acessible via le menu `Extension > Fablab > Exporter en fichier Trotec Spool File (TSF)`
  * Il faut, dans ce cas, ne pas oublier de configurer le répertoire de spool (répertoire où seront exportées les fichier tsf)
  * Il est possible de cette façons d'exporter uniquement la selection en cochant la case appropriée
* Les notes prises durant l'analyse de la structure des fichiers tsf sont disponible (en français) [ici](http://carrefour-numerique.cite-sciences.fr/fablab/wiki/doku.php?id=machines:decoupe_laser:tsf)
* La generations des images noiréblanc utilisées pour la gravure n'ont pas été paufinées. À venir !

## Imprimante/découpeuse vinyle Roland type BN20
Plugin d'enregistrement au format EPS, incluant la gestion de la couleur "CutContour" utilisée pour decouper le vinyle.
Disponible dans `Enregistrer sous` et en selectionnant le type `Eps avec Couleur Roland CutContour (*.eps)`. 

Les traits de découpe doivent exclusivement être fait en lignes vectorielles de couleur rouge (RGB : #FF0000 ) sans transparence. 
C'est une bonne idée de ne pas utiliser cette couleur pour autre chose (modifier la légèrement si vous voulez du rouge, par exemple #FE0000, cela sera invisible à l'œil).</_param>


## Comment installer les plugins ?
Telecharger [les sources au format zip](https://github.com/bumblebeefr/fablab-inkscape-plugins/archive/master.zip), en extraire les fichiers `.py` et `.inx` et les copier dans le repertoire d'extentions d'inkscape : 
* Sous gnu/linux, FreeBSD : `~/.config/inkscape/extentions/` ou `/usr/share/inkscape/extentions/`
* Sous mac OSX : `/Applications/Inkscape.app/Contents/Resources/extensions/`
* Sous windows : `C:\Program Files\Inkscape\share\extensions\` ou `%AppData%\inkscape\extensions\`

Installer imagemagick (utilisé par le plugin d'export au format TSF pour découpeuses laser) :
* Sous gnu/linux, FreeBSD : Installer imagemagick avec votre gestionnaire de packets préféré, ou [télécharger le binaire prépackagé](http://www.imagemagick.org/script/binary-releases.php#unix)
* Sous mac OSX : Utiliser macport, homebrew ou [télécharger l'installeur prépackagé](http://www.imagemagick.org/script/binary-releases.php#macosx)
* Sous windows : [Télécharger l'installeur correspondant à votre version de windows](http://www.imagemagick.org/script/binary-releases.php#windows)
