# Canvas Stitcher

Tool in Python per ricostruire automaticamente un diagramma completo a partire da esportazioni parziali.

L’app non permette di esportare direttamente l’intero canvas in alta risoluzione. 

Per utilizzare il prgetto è necessario dunque:
- esportare manualmente più porzioni dell’area di lavoro
- trasferire le porzioni nell'area del progetto

Lo script le unisce in un’unica immagine tramite OpenCV (cv2.Stitcher)

Il tool supporta:
- stitching di immagini “raw” da una cartella
- estensione incrementale di una composizione già esistente
- gestione dell’ordine di composizione (prima o dopo l’immagine già composta)
- configurazione via CLI
	
	
# Perché esiste

Nasce con l'obiettivo di esportare appunti universitari da DrawNote, software comodo per diagrammi su canvas infinita, in quanto l’export completo non è pratico.

Questo tool permette di:
- ricostruire diagrammi di grandi dimensioni
- mantenere qualità elevata
- evitare screenshot manuali e ricomposizioni in editor esterni

# Come funziona

Il processo svolge:
	1. Esportazione manuale delle sezioni in JPG dall’app
	2. Trasferimento automatico al PC (via script/Termux)
	3. Stitching tramite OpenCV
	4. Output finale in un’unica immagine composta

# Stack tecnico

- Python
- OpenCV
- CLI basata su argparse

# Stato del progetto

Funzionante, migliorabile.

Possibili sviluppi futuri:
- stitching incrementale con salvataggio di keypoints
- modalità di composizione deterministica (senza feature detection)
- gestione automatica delle griglie di esportazione
- packaging come tool installabile (pip)
