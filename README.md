# Python_User-Management
[![Build Status](https://travis-ci.org/jonbulica99/Python_User-Management.svg?branch=master)](https://travis-ci.org/jonbulica99/Python_User-Management)
[![codebeat badge](https://codebeat.co/badges/85bd7a0a-6d0b-4fcb-ac5b-e8ea9e7f6fa0)](https://codebeat.co/projects/github-com-jonbulica99-python_user-management-master)


![Übersicht der Webapp](https://github.com/jonbulica99/Python_User-Management/raw/master/docs/overview.png "Übersicht der Webapp")
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


## Unit-Tests
Diese können mittels folgenden Befehles ausgeführt werden:
```bash
python3 -m unittests
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

- [x] Nutzer haben einen Status ("Present", "Deactivatet",  "Deleted"). Entsprechend dem Status ist auf den Zielsystemen der Nutzer vorhanden, deaktiviert oder gelöscht. Beim Löschen soll auch das Homeverzeichnis des Users gelöscht werden.
- [x] Die öffentlichen SSH-Keys der Nutzer sind in der Datenbank vorhanden und werden beim Anlegen des Nutzers als "authorized keys" auf dem Zielsystem gespeichert.
- [x] Die Tests werden automatisiert in einer Continous Integration Umgebung ausgeführt.
- [x] Sie haben einen Integrationstest geschrieben, der z. B. das Linuxsystem oder die Datenbank „mockt“.

## Refactoring

### Unit-Tests werden automatisch ausgeführt

#### Problem

Test mussten einzeln ausgefürht werden.

#### Lösung

Um dies zu vereinfachen, haben wir uns entschieden, dies durch eine `__main__`-Datei zu ersetzten. 
Die Funktion der Datei beinhaltet, dass alle Dateien im `tests`-Verzeichniss überprüft werden.
Inhaltende Test werden ausgeführt.
Somit wurde es vereinheitlicht, daher müssen wir für unseren CI nur einen Behfehl ausführen.

### Duplizierter Code

#### Problem

Wir haben in den ersten 5 Zeilen eines Codeblockes entdeckt, dass der Code weitestgehend identisch ist.

#### Lösung

Um dieses Problem zu beheben, haben wir eine wietere Klasse namens `BaseObject` hinzugefügt.
Der Inhalt der Zeilen wird somit vererbt, dadurch sparen wir Code. Außerdem müssen somit weitere Änderungen nur an einer 
stelle angepasst werden.

### Windows-Unterstützung für `crypt`

#### Problem

Das Python-Modul `crypt` ist lediglich ein Wrapper für die native [CRYPT(3)](http://man7.org/linux/man-pages/man3/crypt.3.html) Implmentierung in *nix.
Dies bedeutet, dass der Server zwar auf Windows ausgeführt werden kann, es können jedoch keine Benutzer ausgerollt werden, weil dafür `crypt` erforderlich ist.

#### Lösung

Das erste, was einem auffällt, ist den entsprechenden `UserAdd`-Befehl so anzupassen, dass das Kennwort durch eine Subshell auf dem Client gehasht wird. Dies könnte folgendermaßen aussehen:

```python
# UserAdd
def get_encrypted_password(self, password):
    return "$(openssl passwd -crypt '{}')".format(password)
```

Dies würde zwar funktionieren, allerdings müsste in diesem Fall das Kennwort im Plaintext übertragen und ausgeführt werden. Sicherheitstechnisch ist dies keine gute Idee.

Daher haben wir uns für eine reine Python-Implementierung entschieden: `pcrypt`. Da diese laut Entwickler 5 Mal so langsam als die native ist, wird es nur dann verwendet, wenn Letzteres nicht vorhanden ist.

### `__supported_os__` Variable

#### Problem

Da alle Commands `BaseCommand` erben, wird beim Initialisieren (durch `__generate()`) anhand der Variable `__supported_os__` automatisch geprüft, ob diese für das ausführende System geeignet sind.

Dabei wird nicht definiert, ob das System den Befehl ausführen kann, sondern lediglich ob es in der Lage ist, diesen mittels `get_template()` zu generieren.

`__supported_os__` ist eine Variable des jeweiligen Moduls, und wird somit nicht vererbt.

#### Lösung

Durch [obiges Refactoring](#windows-unterstützung-für-crypt) beinhaltet `__supported_os__` für jeden Command die selben Betriebssysteme. Daher wurde `__supported_os__` zu einer Klassen-Variable von `BaseCommand`. Child-Klassen können diese immer noch überschreiben, müssen sie jedoch nicht immer explizit definieren, wenn sie den Standardwert erhalten soll.

Somit sparen wir Codezeilen, sowohl beim jeweiligen Modul, als auch bei der `__init__`-Funktion jeder Command-Klasse.
