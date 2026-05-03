# Logging System Target Architecture (Informe)

## 1. Objetivo General

Diseñar e implementar un sistema de logging moderno, robusto y escalable que cumpla con estándares actuales de observabilidad, garantizando:

- Seguridad en entornos concurrentes (multihilo y multiproceso)
- Bajo impacto en performance
- Estructuración consistente de logs
- Facilidad de integración con sistemas externos
- Compatibilidad total con el código legacy existente

El sistema debe evolucionar sin requerir cambios en los puntos actuales de uso (`get_logger(area, category)`).

---

## 2. Resultado Esperado (Estado Final)

El sistema de logging debe comportarse como una infraestructura desacoplada con las siguientes características:

### 2.1 Desacople total entre generación y escritura

- Los logs NO deben escribirse directamente desde el código de negocio
- Toda emisión de logs debe ser no bloqueante
- La escritura debe centralizarse en un único punto de consumo

Arquitectura objetivo:

```
[Application Code]
        ↓
   (Logger API)
        ↓
   QueueHandler
        ↓
   Shared Queue
        ↓
   QueueListener (worker único)
        ↓
[Handlers: File / Console / External Systems]
```

---

### 2.2 Compatibilidad con concurrencia real

El sistema debe:

- Ser seguro en entornos multihilo (thread-safe)
- Ser seguro en entornos multiproceso (process-safe)

Debe evitar:

- Corrupción de logs
- Condiciones de carrera
- Duplicación de handlers
- Pérdida de mensajes

---

### 2.3 Configuración centralizada

- Toda la configuración de logging debe inicializarse UNA sola vez
- Los loggers individuales no deben gestionar handlers directamente
- Debe existir un punto único de bootstrap del sistema

---

### 2.4 Logging estructurado (Structured Logging)

Todos los logs deben poder representarse en formato estructurado (JSON), con un esquema consistente.

Ejemplo:

```json
{
  "timestamp": "...",
  "level": "INFO",
  "logger": "AREA.CATEGORY",
  "message": "...",
  "context": {
    "request_id": "...",
    "user_id": "...",
    "service": "..."
  }
}
```

Esto permite:

- Indexación
- Búsqueda eficiente
- Integración con herramientas externas

---

### 2.5 Enriquecimiento de contexto (Context Propagation)

El sistema debe permitir adjuntar contexto dinámico automáticamente:

- request_id
- trace_id
- user_id
- metadata relevante

Sin necesidad de pasarlo manualmente en cada log.

Debe soportar:

- Ejecución async
- Multithreading

Tecnología objetivo:

- `contextvars`

---

### 2.6 Performance y no bloqueo

- El código de negocio nunca debe bloquear por operaciones de logging
- El formateo y escritura deben ocurrir fuera del thread principal
- El uso de IO debe estar completamente desacoplado

---

### 2.7 Manejo de outputs (Handlers)

El sistema debe soportar múltiples destinos de salida:

- Consola (desarrollo)
- Archivo (producción)
- Sistemas externos (futuro)

Debe permitir:

- Activación/desactivación por configuración
- Selección de formato (plain text vs JSON)

---

### 2.8 Rotación y persistencia

- Implementar rotación de logs (por tamaño o tiempo)
- Definir políticas de retención
- Evitar crecimiento ilimitado de archivos

---

### 2.9 Extensibilidad

El sistema debe estar preparado para integrar:

- ELK Stack (Elasticsearch, Logstash, Kibana)
- Grafana Loki
- Datadog
- OpenTelemetry

Sin requerir rediseños estructurales.

---

## 3. Restricciones de Diseño

### 3.1 Compatibilidad legacy (CRÍTICO)

No se debe modificar el contrato público existente:

```python
get_logger(area, category)
```

Esto implica:

- No cambiar la firma (parámetros, tipos, valor de retorno)
- No requerir modificaciones en el código consumidor existente
- No introducir efectos colaterales incompatibles con el comportamiento actual

Se permite:

- Modificar completamente la implementación interna
- Reemplazar la infraestructura subyacente (handlers, transporte, formateo, almacenamiento)
- Mejorar performance, concurrencia y capacidades del sistema

Extensiones:

- Deben ser completamente backward-compatible o explícitamente opt-in
- No deben alterar el comportamiento esperado por el código existente

Evolución:

- Debe permitirse la coexistencia entre comportamiento legacy y nuevas capacidades
- No se deben introducir migraciones forzadas

---

### 3.2 Definición de contrato observable

Se considera parte del contrato:

- La forma de invocación del logger (`get_logger`)
- La disponibilidad y estabilidad del logger retornado
- La semántica de niveles (`DEBUG`, `INFO`, etc.)

No se considera parte del contrato (puede evolucionar):

- El formato exacto del log (texto vs JSON)
- El destino de los logs (archivo, consola, sistemas externos)
- La estructura interna del mensaje

Nota:

> El formato de salida de logs no se considera parte del contrato público salvo que esté explícitamente documentado como tal.

---

## 4. Formato de Logs (Estado Actual vs Objetivo)

### 4.1 Estado actual

Formato plano:

```
2026-04-30 14:00:34,371 - DEBUG - database.system - (57, ('03737', 'RES...', 'SL'))
```

Problemas:

- No estructurado → difícil de parsear
- Dependencia de representación interna de objetos Python
- Sin contexto enriquecido
- Difícil integración con herramientas externas
- Ambigüedad semántica

---

### 4.2 Objetivo: Structured Logging (JSON)

El sistema debe migrar a un formato estructurado basado en JSON.

Ejemplo objetivo:

```json
{
  "timestamp": "2026-04-30T14:00:34.371Z",
  "level": "DEBUG",
  "logger": "database.system",
  "message": "Article processed",
  "data": {
    "index": 57,
    "code": "03737",
    "description": "RES. SMD 002.2 K_OHM ENCAP 1206 01%",
    "category": "SL"
  }
}
```

---

### 4.3 Campos estándar

Campos obligatorios:

- `timestamp`
- `level`
- `logger`
- `message`

Campos opcionales:

- `data`
- `context`
- `error`

---

### 4.4 Compatibilidad con modo legacy

Regla de comportamiento:

```
if extra["data"] exists:
    usar schema estructurado
else:
    fallback a formato legacy
```

Esto garantiza transición sin ruptura.

---

### 4.5 Lineamientos de diseño

- `message` debe ser semántico
- Los datos deben ir en `data`
- Evitar serialización manual dentro del mensaje

---

## 5. Métricas de Éxito

El sistema será considerado correcto si:

- No hay pérdida de logs bajo carga concurrente
- No hay duplicación de mensajes
- El overhead es mínimo
- Los logs son fácilmente consumibles por herramientas externas
- La API permanece intacta

---

## 6. Roadmap de Implementación
### Fase 1 — Infraestructura concurrente (CRÍTICA)

**Objetivo:**
Desacoplar completamente la generación de logs de su escritura (IO), garantizando seguridad en entornos multihilo y multiproceso.

**Tareas:**

* Implementar `QueueHandler` para todos los loggers
* Implementar `QueueListener` centralizado
* Crear una cola compartida (thread-safe / multiprocess-ready)
* Redirigir todos los handlers actuales al listener

**Reglas:**

* `get_logger` no debe cambiar
* Ningún logger debe escribir directamente a archivo o consola

**Criterio de aceptación:**

* No hay corrupción de logs en concurrencia
* No hay duplicación de handlers
* Mejora de performance bajo carga

---

### Fase 2 — Centralización de configuración

**Objetivo:**
Eliminar la configuración distribuida y consolidar la inicialización del sistema.

**Tareas:**

* Crear módulo de bootstrap (`logging.bootstrap`)
* Centralizar:

  * creación de handlers
  * selección de formatters
  * configuración (niveles, flags)

**Reglas:**

* La inicialización ocurre una sola vez
* `get_logger` solo obtiene instancias, no configura

**Criterio de aceptación:**

* Ningún logger instancia handlers directamente
* Toda la configuración está controlada desde un único punto

---

### Fase 3 — Context propagation (framework-agnostic)

**Objetivo:**
Incorporar contexto enriquecido sin acoplar el sistema a frameworks específicos.

**Tareas:**

* Implementar sistema basado en `contextvars`
* Definir API interna:

  * `set_context(...)`
  * `get_context()`
* Definir contexto base automático (process_id, thread_id, etc.)

**Comportamiento:**

* Sin contexto explícito → logs válidos con contexto mínimo
* Con contexto → enriquecimiento automático

**Integraciones opcionales:**

* Middleware para FastAPI (u otros frameworks)

**Criterio de aceptación:**

* El sistema funciona sin dependencias externas
* El contexto se agrega automáticamente cuando está disponible

---

### Fase 4 — Structured Logging (JSON)

**Objetivo:**
Migrar a un esquema estructurado manteniendo compatibilidad con logs existentes.

**Tareas:**

* Rediseñar `JsonFormatter`
* Implementar lógica de compatibilidad:

```
if extra["data"] exists:
    usar schema estructurado
else:
    fallback a formato legacy
```

* Definir y documentar schema estándar

**Reglas:**

* Nunca romper logs existentes
* Siempre generar output válido

**Criterio de aceptación:**

* Logs nuevos cumplen el schema estructurado
* Logs legacy siguen funcionando sin cambios

---

### Fase 5 — Migración progresiva del código

**Objetivo:**
Eliminar gradualmente logs no estructurados.

**Tareas:**

* Identificar puntos críticos del sistema
* Migrar:

```python
logger.debug(obj)
```

a:

```python
logger.debug("Event description", extra={"data": {...}})
```

**Criterio de aceptación:**

* Incremento progresivo de logs estructurados
* Sin regresiones funcionales

---

### Fase 6 — Observabilidad e integración externa (opcional)

**Objetivo:**
Preparar el sistema para integrarse con herramientas externas.

**Tareas:**

* Validar compatibilidad del schema con:

  * ELK / OpenSearch
  * Grafana Loki
  * Datadog
* Ajustar campos si es necesario

**Criterio de aceptación:**

* Logs consumibles directamente por sistemas externos
* No requiere transformaciones adicionales

---

## 7. Consideraciones de contexto (CRÍTICO)

**Objetivo:**
Garantizar que el sistema de logging sea completamente independiente del framework de ejecución.

**Requisitos:**

El sistema debe funcionar correctamente en:

- Scripts standalone
- Workers / procesos batch
- Servicios HTTP (ej. FastAPI)

**Estrategia:**

- Definir un **contexto base automático** (process_id, thread_id, etc.)
- Incorporar contexto dinámico mediante `contextvars`
- Mantener las integraciones con frameworks como **opcionales y desacopladas**

---

## 8. Estrategia de integración

**Objetivo:**
Permitir adopción progresiva del sistema sin impacto disruptivo.

**Lineamientos:**

- El sistema se implementa como una **librería independiente**
- La inicialización se realiza mediante un **bootstrap explícito**
- El sistema debe ser **plug-and-play**

**Migración:**

- Reemplazo progresivo del sistema legacy
- Posibilidad de coexistencia temporal entre ambos sistemas
- Sin requerir modificaciones profundas en el código consumidor

---

## 9. Prompt IA Friendly

Use this as a base prompt:

```
I have a Python logging system with a public function:

get_logger(area, category)

This function is part of a legacy contract and MUST NOT change (signature or usage).

I am evolving this system into a production-grade logging architecture with the following requirements:

[Core Architecture]
- Queue-based logging (QueueHandler + QueueListener)
- Full support for multithreading and multiprocessing
- Centralized bootstrap configuration (single initialization point)
- Non-blocking log emission

[Structured Logging]
- JSON-based structured logging
- Explicit separation between:
  - message (semantic string)
  - data (structured payload via extra["data"])
- Backward compatibility:
  - If extra["data"] is not provided, fallback to legacy behavior

[Context System]
- Context propagation using contextvars
- Must work with and without web frameworks (e.g. FastAPI)
- Automatic enrichment when context is available
- No manual parameter passing in log calls

[Constraints]
- Do not modify existing logger usage (get_logger)
- Maintain backward compatibility with legacy logs
- Prefer Python standard library
- Ensure high performance under concurrency
- Avoid duplicated handlers or race conditions

[Additional Requirements]
- Support log rotation
- Allow optional integration with external observability systems (ELK, Loki, etc.)
- Keep the system modular (queue, context, formatters, bootstrap)

[Expected Output]
Provide a solution that:
- Fits into this architecture
- Does not break existing behavior
- Is production-ready (not just conceptual)

Help me design or implement: [specific part]
```

---

## 10. Conclusión

El objetivo es construir una infraestructura de logging con las siguientes propiedades:

- **Escalable:** soporta carga y concurrencia real
- **Confiable:** sin pérdida ni corrupción de logs
- **Observable:** logs estructurados y consumibles externamente
- **Desacoplada:** independiente del código de negocio y frameworks
- **Compatible:** mantiene el contrato legacy sin ruptura

Esto posiciona el sistema de logging como un componente de infraestructura crítico, alineado con estándares modernos de sistemas en producción.
