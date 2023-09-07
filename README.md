# Datenarchitektur Wetterdaten

## Einleitung

Die Wetterdaten der Wetterstation liegen als Dateien auf einem Share des DWD vor.
Dabei werden Daten wie Windgeschwindigkeit, Windrichtung etc. in einer Datei gespeichert.
Zudem werden Metainformationen vorenthalten, die in einer anderen Datei gespeichert sind.

In diesem Projekt sollen die Daten der Wetterstation in eine Datenbank geladen werden. Dazu muss zunächst ein Datenmodell erstellt werden, welches die Daten der Wetterstation abbildet.

Diese Daten sollen in einer Relationale Datenbank gespeichert werden und normalisiert sein.

## Installation

Um das Projekt zu installieren, muss zunächst das Repository geklont werden.

```bash
git clone https://github.com/mhabedank/dwd-weather-data-ingestion.git
```

Anschließend sollte Peotry, so es nicht schon vorhanden ist, installiert werden.

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

Nun kann das Projekt installiert werden.

```bash
poetry install
```

Um die Skripte auszuführen, müssen Umgebungsvariablen gesetzt werden.
Dazu kann die Datei `.env.example` kopiert und angepasst werden.

Die Umgebungsvariable PROJECT_DIR ist der absolute Pfad zu dem Project Ordner (der Ordnern, in dem sich die Datei `pyproject.toml` befindet).

## Datenmodell

Das Datenmodell soll die folgenden Regeln der Normalisierung einhalten:

- 1. Normalform: Jede Spalte enthält nur atomare Werte.
- 2. Normalform: Jedes Nichtschlüsselattribut ist voll funktional abhängig vom Primärschlüssel.
- 3. Normalform: Es gibt keine transitiven Abhängigkeiten zwischen Nichtschlüsselattributen und dem Primärschlüssel.
- Boyce-Codd-Normalform: Jede Determinante ist ein Schlüsselkandidat.
- 4. Normalform: Es gibt keine mehrwertigen Abhängigkeiten.

Daraus ergibt sich das folgende ER Diagramm:

![ER Diagramm](assets/ER-diagram.png)


## Object Relation Mapping

Um die Daten in Python zugänglich zu machen, wird ein s.g.
Object Relation Mapping (ORM) verwendet. Dabei werden die Datenbanktabellen in Python Klassen abgebildet.
Um dies zu realisieren, wird die Bibliothek PeeWee verwendet.

Die Klassen werden im Modul `src.models` definiert.

## File Wrapper

Um die Daten aus den Dateien zu lesen, wurden verschiedene Wrapper implementiert.
Diese dienen dazu, die Logik, um die Daten aus den Dateien zu lessen
zu kapsel. Dabei gibt es zwei verschiedene Module. Im Modul
`src.file_wrapper.meta_data` werden Klassen zum Auslesen der Meta-Daten implementiert.
Im Modul `src.file_wrapper.weather_data` werden sind die Klassen für die Wetterdaten, in diesem Fall
der Windgeschwindigkeit hinterlegt.

## Geodaten

Es werden Geodaten, die die Staatsgrenzen der Bundesländer abbilden, verwendet. Diese werden aus einem Gitrepository geladen
und später zum Filtern verwendet.

# Durchführen des ETL Prozesses

Um den ETL Prozess durchzuführen, müssen lediglich die Notebooks im Ordner `notebooks` ausgeführt in der
Reihenfolge ausgeführt werden, in der sie nummeriert sind. Weitere Details stehen in diesen Dateien.

Grob sind die Schritte wie folgt:  
**1) Download der Rohdaten**: In den Notebooks 1 bis 3 werden die Rohdaten in Form von gezippten Dateien heruntergeladen.  
**2) Extrahieren der Rohdaten**: Im Notebook 4 werden die Rohdaten extrahiert.  
**3) Laden der Daten in Parquet-Dateien**: Im Notebook 5 werden die Daten Parquet-Dateien geladen, um zu für den 
upload in die Datenbank zur Verfügung zu stellen.  
**4)Laden der Daten in die Datenbank**: Im Notebook 6 werden die Daten in die Datenbank geladen.  
**5) Zugriff auf die Daten**: Im Notebook 7 wird ein Beispiel für den Zugriff auf die Daten gezeigt.  

# Web-API
im Notebook 8 wird eine Web-API implementiert, die die Daten aus der Datenbank über das Web zur Verfügung stellt.
Implementiert ist dabei eine abgespeckte RESTfulAPI, die lediglich lesenden Zugriff auf die Daten bietet
und ein erweiterter Endpunkt, der es möglich macht, basierend auf einer Geoposition und einem Radius in KM nach Stationen zu suchen.