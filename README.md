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

## TODO
1. connection protocols (?) > ssh
    * connection manager
2. user manager 
    * https://github.com/ansible/ansible/blob/stable-2.7/lib/ansible/modules/system/user.py ¯\\_(ツ)_/¯

9999999. unittests


## Unit-Tests
Diese können mittels folgenden Befehles ausgeführt werden:
```bash
python3 -m unittests.test_backend
```
Hierfür wird `unittest` benötigt.

## Aufgabenstellung und Anforderungen

Für die Verwaltung von Nutzern sollen Sie eine Datenbank erstellen und ergmöglichen, dass die Nutzer automatisiert auf einem Linux-Server angelegt werden. Je nach Ausbausstufe soll mehr als ein Server sowie Gruppe und Nuzter konfiguriert werden.


### Must have

- [x] Es existiert eine Datenbank, in der Nutzer verwaltet werden.
- [ ] Die Nutzer der Datenbank werden automatisiert in das Linux-Zielsystem eingepflegt. 
- [ ] Für jeden Nutzer wird ein Standardpasswort vergeben. 
- [x] Der Nutzer wird beim ersten Login aufgefordert, das Passwort zu ändern.
- [ ] Sie haben mindestens drei automatisierte Unit-Tests.  
- [x] Sie verwenden GIT (oder ein anderes VCS).
- [x] Sie nutzen Logging.


### Should have

- [x] Es existiert eine Datenbank in welcher Nutzer, Gruppen und Server verwaltet werden.
- [x] Sie verwenden verschiedene Module.
- [x] Sie verfolgen einen OOP Ansatz.
- [ ] Sie können einen Nutzer auf mindestens zwei Systemen ausrollen.
- [ ] Ein Nutzer kann einer Gruppe zugeordnet werden. 
- [ ] Vor dem Anlegen eines Nutzers oder einer Gruppe wird geprüft, ob der Nutzer oder die Gruppe existiert. Falls der Nutzer oder die Gruppe existiert, wird nicht versucht, den Nutzer oder die Gruppe anzulegen.
- [ ] Sie haben mindestens fünf automatisierte Unit-Tests.


### Could have

- [ ] Nutzer haben einen Status („Present“, „Deactivatet“,  „Deleted“). Entsprechend dem Status ist auf den Zielsystemen der Nutzer vorhanden, deaktiviert oder gelöscht. Beim Löschen soll auch das Homeverzeichnis des Users gelöscht werden.
- [ ] Die öffentlichen SSH-Keys der Nutzer sind in der Datenbank vorhanden und werden beim Anlegen des Nutzers als „authorized keys“ auf dem Zielsystem gespeichert.
- [ ] Die Tests werden automatisiert in einer Continous Integration Umgebung ausgeführt.
- [ ] Sie haben einen Integrationstests geschrieben, der z. B. das Linuxsystem oder die Datenbank „mockt“.
