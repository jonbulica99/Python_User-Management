# Python_User-Management

## Aufsetzung Step-by-Step

1. Repo inkl. Submodule durch Eingabe folgender Befehle klonen:
```bash
git clone https://github.com/jonbulica99/Python_User-Management
cd ./Python_User-Management
git submodule update --init --recursive
```

2. Pip-Abhängigkeiten installieren (eventuell in virtueller Umgebung):
```bash
python3 -m pip install -r requirements.txt
```

3. Frontend [herunterladen](https://github.com/jonbulica99/Python_User-Management/releases) und nach `./supreme/dist` entpacken.

4. App- und Datenbank-Einstellungen unter `config/main.ini` anpassen.

5. Programm mittels `python3 main.py` starten. Standardmäßig wird vSupreme unter [localhost:8090](http://localhost:8090) angeboten.

6. Profit?

## TODO
1. Use-Case-Diagramm
2. Klassendiagramm


## Unit-Tests
Diese können mittels folgenden Befehles ausgeführt werden:
```bash
python3 -m unittests.test_backend
```
Hierfür wird das Python-Modul `unittest` benötigt.

## Aufgabenstellung und Anforderungen

Für die Verwaltung von Nutzern sollen Sie eine Datenbank erstellen und ergmöglichen, dass die Nutzer automatisiert auf einem Linux-Server angelegt werden. Je nach Ausbausstufe soll mehr als ein Server sowie Gruppe und Nuzter konfiguriert werden.


### Must have

- [x] Es existiert eine Datenbank, in der Nutzer verwaltet werden.
- [x] Die Nutzer der Datenbank werden automatisiert in das Linux-Zielsystem eingepflegt. 
- [x] Für jeden Nutzer wird ein Standardpasswort vergeben. 
- [x] Der Nutzer wird beim ersten Login aufgefordert, das Passwort zu ändern.
- [x] Sie haben mindestens drei automatisierte Unit-Tests.  
- [x] Sie verwenden GIT (oder ein anderes VCS).
- [x] Sie nutzen Logging.


### Should have

- [x] Es existiert eine Datenbank in welcher Nutzer, Gruppen und Server verwaltet werden.
- [x] Sie verwenden verschiedene Module.
- [x] Sie verfolgen einen OOP Ansatz.
- [x] Sie können einen Nutzer auf mindestens zwei Systemen ausrollen.
- [x] Ein Nutzer kann einer Gruppe zugeordnet werden. 
- [x] Vor dem Anlegen eines Nutzers oder einer Gruppe wird geprüft, ob der Nutzer oder die Gruppe existiert. Falls der Nutzer oder die Gruppe existiert, wird nicht versucht, den Nutzer oder die Gruppe anzulegen.
- [x] Sie haben mindestens fünf automatisierte Unit-Tests.


### Could have

- [x] Nutzer haben einen Status („Present“, „Deactivatet“,  „Deleted“). Entsprechend dem Status ist auf den Zielsystemen der Nutzer vorhanden, deaktiviert oder gelöscht. Beim Löschen soll auch das Homeverzeichnis des Users gelöscht werden.
- [x] Die öffentlichen SSH-Keys der Nutzer sind in der Datenbank vorhanden und werden beim Anlegen des Nutzers als "authorized keys" auf dem Zielsystem gespeichert.
- [ ] Die Tests werden automatisiert in einer Continous Integration Umgebung ausgeführt.
  Kein Bock auf diese.
- [x] Sie haben einen Integrationstest geschrieben, der z. B. das Linuxsystem oder die Datenbank „mockt“.
