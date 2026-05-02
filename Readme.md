# TraceLogger

A framework-agnostic structured logging system for Python, designed for consistency across scripts, workers, and web services.

---

## 🚀 Features

- **Structured logging** (JSON-ready)
- **Context propagation** using `contextvars`
- **Async-safe** design
- **Pluggable handlers** (console, file, external systems)
- **Framework-independent** core
- **Extensible** formatting pipeline

---

## 📦 Installation

```bash
pip install tracelogger
```

Durante el desarrollo:

```bash
pip install -e .
```

## ⚡ Quick Example

```python
from logging.logger import GetLogger, LogArea, LogCategory

Logger = GetLogger(LogArea.CORE, LogCategory.SYSTEM)

Logger.info("System started")
```

## 🧠 Context System

Inyecta datos contextuales dinámicamente:

```python
from logging.context import SetContext

SetContext(user_id=123, request_id="abc")

Logger.info("Processing request")
```

**Ejemplo de salida:**

```json
{
  "message": "Processing request",
  "user_id": 123,
  "request_id": "abc"
}
```

## 🏗️ Architecture

```text
logging/
│
├── core/
│   ├── queue.py
│   └── listener.py
│
├── handlers/
├── formatters/
│
├── logger.py
└── bootstrap.py
```

## 🎯 Design Goals

- Sin dependencia de frameworks (*No framework lock-in*)
- Comportamiento determinista
- Alto rendimiento bajo concurrencia
- Clara separación de responsabilidades

## 📚 Documentation

La documentación detallada y las decisiones de diseño están disponibles en:

`/docs`

## 🧪 Use Cases

- Scripts independientes
- Workers en segundo plano
- Servicios FastAPI / Flask
- Sistemas distribuidos

## 📌 Status

🚧 **In development**