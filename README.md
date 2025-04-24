# Agenten mit PydanticAI

# Agenten

Agenten sind die primäre Schnittstelle für die Interaktion mit großen Sprachmodellen (LLMs). 
Ein Agent fungiert als Container für verschiedene Komponenten, einschließlich:

* **System-Prompts**: Anweisungen für das LLM, definiert als statische Zeichenketten oder dynamische Funktionen, die ein `RunContext`-Objekt als Eingabe nehmen und eine Zeichenkette zurückgeben.

* **Funktionswerkzeuge**: Funktionen, die das LLM aufrufen kann, um zusätzliche Informationen zu erhalten oder Aktionen durchzuführen.

* **Strukturierte Ergebnistypen**: Datentypen (Pydantic-Modelle), die das LLM am Ende einer Ausführung zurückgeben muss.

* **Abhängigkeitstypen**: Daten oder Dienste, die von System-Prompt-Funktionen, Werkzeugen und Ergebnisvalidatoren verwendet werden können.

* **LLM-Modelle**: Das LLM, das der Agent verwenden wird. Dies kann bei der Erstellung des Agenten oder zur Laufzeit festgelegt werden.

Agenten sind auf Wiederverwendbarkeit ausgelegt und werden typischerweise einmal instanziiert und in einer gesamten Anwendung wiederverwendet.

## System-Prompts

System-Prompts sind Anweisungen, die dem LLM vom Entwickler bereitgestellt werden.

Sie können sein:

* **Statische System-Prompts**: Definiert bei der Erstellung des Agenten unter Verwendung des Parameters `system_prompt` des Agent-Konstruktors.

* **Dynamische System-Prompts**: Definiert durch Funktionen, die mit `@agent.system_prompt` dekoriert sind. Diese können Laufzeitinformationen, wie z. B. Dependencies, über das `RunContext`-Objekt abrufen.

Ein einzelner Agent kann sowohl statische als auch dynamische System-Prompts verwenden, die in der Reihenfolge angehängt werden, in der sie zur Laufzeit definiert sind. 

**Beispiel: first.py**

## Funktionen

Funktionen ermöglichen es Large Language Models (LLMs), auf externe Informationen zuzugreifen oder Aktionen durchzuführen, die innerhalb des System-Prompts selbst nicht verfügbar sind. Werkzeuge können auf verschiedene Arten registriert werden:

* **`@agent.tool`-Decorator**: Für Werkzeuge, die über das `RunContext` Objekt Zugriff auf den Kontext des Agenten benötigen.
* **`@agent.tool_plain`-Decorator**: Für Werkzeuge, die keinen Zugriff auf den Kontext des Agenten benötigen.
* **`tools`-Schlüsselwortargument im `Agent`-Konstruktor**: Kann einfache Funktionen oder Instanzen der `Tool`-Klasse entgegennehmen und ermöglicht so mehr Kontrolle über die Werkzeugdefinitionen.

Funktionsparameter werden aus der Funktionssignatur extrahiert und zum Aufbau des JSON-Schemas des Werkzeugs verwendet. 
Die Docstrings der Funktionen werden verwendet, um die Beschreibungen des Werkzeugs und die Parameterbeschreibungen innerhalb des Schemas zu generieren.

**Beispiel: second.py**

## Dependencies

Dependencies stellen Daten und Dienste für die System-Prompts, Werkzeuge und Ergebnisvalidatoren des Agenten über ein Dependency-Injection-System bereit. Auf Abhängigkeiten wird über das `RunContext` Objekt zugegriffen. Sie können jeden Python-Typ haben, aber `dataclasses` sind eine praktische Möglichkeit, mehrere Abhängigkeiten zu verwalten.

**Beispiel: third.py**

## Ergebnisse

Ergebnisse sind die endgültigen Werte, die von einer Agentenausführung zurückgegeben werden. Sie sind in `RunResult` (für synchrone und asynchrone Ausführungen) oder `StreamedRunResult` (für gestreamte Ausführungen) verpackt und ermöglichen den Zugriff auf Nutzungsdaten und den Nachrichtenverlauf. Ergebnisse können einfacher Text oder strukturierte Daten sein und werden mit Pydantic validiert.

Ergebnisvalidatoren, die über den `@agent.result_validator`-Decorator hinzugefügt werden, bieten eine Möglichkeit, weitere Validierungslogik hinzuzufügen, insbesondere wenn die Validierung IO erfordert und asynchron ist.

**Beispiel: forth.py**

## Hauptmerkmale

PydanticAI bietet mehrere Hauptmerkmale, die es zu einer überzeugenden Wahl für die Entwicklung von KI-Anwendungen machen:

* **Modellagnostisch**: PydanticAI unterstützt eine Vielzahl von LLMs, darunter OpenAI, Anthropic, Gemini, Ollama, Groq und Mistral. Es bietet auch eine einfache Schnittstelle zur Implementierung der Unterstützung für andere Modelle.
* **Typsicherheit**: Entwickelt, um nahtlos mit statischen Typ-Checkern wie [mypy](http://mypy-lang.org/) und [pyright](https://github.com/microsoft/pyright) zusammenzuarbeiten. Es ermöglicht die Typüberprüfung von Abhängigkeiten und Ergebnistypen.
* **Python-zentriertes Design**: Nutzt vertraute Python-Kontrollfluss- und Agentenkompositionen, um KI-Projekte zu erstellen, wodurch die Anwendung von Standard-Python-Praktiken erleichtert wird.
* **Strukturierte Antworten**: Verwendet [Pydantic](https://docs.pydantic.dev/latest/) zur Validierung und Strukturierung von Modellausgaben, um konsistente Antworten zu gewährleisten.
* **Dependency-Injection-System**: Bietet ein Dependency-Injection-System, um den Komponenten eines Agenten Daten und Dienste bereitzustellen, was die Testbarkeit und iterative Entwicklung verbessert.
* **Gestreamte Antworten**: Unterstützt das Streaming von LLM-Ausgaben mit sofortiger Validierung, was schnelle und genaue Ergebnisse ermöglicht.


## Arbeiten mit Agenten

### Agenten ausführen

Agenten können auf verschiedene Arten ausgeführt werden:

* **`run_sync()`**: Für synchrone Ausführung.
* **`run()`**: Für asynchrone Ausführung.
* **`run_stream()`**: Für das Streaming von Antworten.

**Beispiel: fifth.py**

### Konversationen

Eine Agentenausführung kann eine gesamte Konversation darstellen, aber Konversationen können auch aus mehreren Ausführungen bestehen, insbesondere wenn der Zustand zwischen Interaktionen beibehalten werden muss. Sie können Nachrichten aus vorherigen Ausführungen mithilfe des `message_history`-Arguments übergeben, um eine Konversation fortzusetzen.

**Beispiel: sixth.py**

### Nutzungsbeschränkungen

PydanticAI bietet eine `settings.UsageLimits` Struktur, um die Anzahl der Tokens und Anfragen zu begrenzen. Sie können diese Einstellungen über das `usage_limits`-Argument an die `run`-Funktionen übergeben.

**Beispiel: sixth.py**

### Modelleinstellungen

Die `settings.ModelSettings` Struktur ermöglicht es Ihnen, das Verhalten des Modells durch Parameter wie `temperature`, `max_tokens` und `timeout` feinabzustimmen. Sie können diese über das `model_settings`-Argument in den `run`-Funktionen anwenden.

**Beispiel: sixth.py**


## Funktion Tools im Detail

### Tool Registrierung

Tools können auf drei Arten registriert werden:

* Mittels des Decorators `@agent.tool` (für Tools, die Zugriff auf den Agentenkontext benötigen).
* Mittels des Decorators `@agent.tool_plain` (für Tools, die keinen Zugriff auf den Agentenkontext benötigen).
* Durch Übergabe einer Liste von Werkzeugen an das `tools`-Argument beim Erstellen einer `Agent`-Instanz. Dies ermöglicht die Verwendung einfacher Funktionen oder Instanzen der `Tool`-Klasse.

**Beispiel: seventh.py**

### Toolschema

Die Beschreibungen der Werkzeugparameter werden automatisch aus den Docstrings der entsprechenden Python-Funktionen extrahiert und dem JSON-Schema des Werkzeugs hinzugefügt. Verfügt ein Werkzeug über lediglich einen Parameter, der im JSON-Schema als einzelnes Objekt repräsentiert werden kann, wird das Schema vereinfacht, um direkt dieses Objekt darzustellen.

**Beispiel: seventh.py**

### Dynamische Tools

Tools können mithilfe einer optionalen `prepare`-Funktion dynamisch angepasst werden. Diese Funktion wird vor jedem Schritt der Agentenausführung aufgerufen. Sie ermöglicht es, die Definition des Werkzeugs für den aktuellen Schritt zu modifizieren oder das Werkzeug für diesen spezifischen Schritt sogar vollständig auszuschließen.

**Beispiel: seventh.py**


## Nachrichten und Chat-Verlauf


### Zugriff auf Nachrichten

Auf die Nachrichten, die während einer Agentenausführung ausgetauscht wurden, kann einfach über die Methoden `all_messages()` und `new_messages()` der Objekte `RunResult` und `StreamedRunResult` zugegriffen werden.

**Beispiel: eighth.py**

### Nachrichtenwiederverwendung

Um Konversationen über mehrere Agentenausführungen hinweg fortzusetzen, können Sie die Nachrichten der vorherigen Ausführungen an den Parameter `message_history` übergeben. Ist `message_history` gesetzt und enthält Nachrichten, wird für die aktuelle Ausführung kein neuer System-Prompt generiert.

**Beispiel: eighth.py**

### Nachrichtenformat

Das Nachrichtenformat ist so gestaltet, dass es unabhängig vom verwendeten Sprachmodell ist. Dies ermöglicht die nahtlose Wiederverwendung von Nachrichten in verschiedenen Agenten oder sogar innerhalb desselben Agenten, wenn Sie unterschiedliche Modelle ausprobieren möchten.

**Beispiel: eighth.py**