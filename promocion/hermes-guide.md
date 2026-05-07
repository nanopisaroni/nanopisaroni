# 🖤 Hermes Agent — Guía Completa para la Demo

> *El agente de IA open-source que no es un chatbot.*

---

## 1. ¿Qué es Hermes Agent?

Hermes es un **framework de agente de IA open-source**, creado por **Nous Research**. Corre en tu propia máquina (o VPS), tiene acceso a tu terminal, archivos, internet, y puede ejecutar acciones reales — no solo responder preguntas.

**Pertenece a la misma familia que:**
- Claude Code (Anthropic)
- Codex CLI (OpenAI)
- OpenClaw / Goose

**Pero se diferencia en:**

| Hermes | Otros agentes |
|--------|---------------|
| Funciona con **cualquier modelo** (DeepSeek, Gemini, Claude, OpenAI, local) | Atados a un solo proveedor |
| Corre en **Telegram, Discord, WhatsApp, Signal, Slack, email, SMS y 10+ plataformas** | Solo en terminal o IDE |
| **Skills auto-mejorables** — aprende y guarda procedimientos | No aprenden entre sesiones |
| **Memoria persistente** — recuerda quién sos | Cada sesión empieza de cero |
| **Gratuito y open-source** | Muchos son de paga |
| **Crons, webhooks, subagentes** | Solo chat interactivo |

---

## 2. ¿Cómo funciona por dentro?

```
          TÚ (Telegram / CLI / Discord)
                      │
                      ▼
        ┌─────────────────────────┐
        │      HERMES AGENT       │
        │                         │
        │  ┌───────────────────┐  │
        │  │    CORVUSH        │  │  ← Mi personalidad
        │  │  (SKILL.md)       │  │
        │  └───────────────────┘  │
        │                         │
        │  ┌───────────────────┐  │
        │  │   MODELO PRINCIPAL│  │  ← DeepSeek v4 Flash
        │  │   (razonamiento)  │  │
        │  └───────────────────┘  │
        │                         │
        │  ┌───────────────────┐  │
        │  │   MEMORIA         │  │  ← Recuerda entre sesiones
        │  │   (persistente)   │  │
        │  └───────────────────┘  │
        │                         │
        │  ┌───────────────────┐  │
        │  │   HERRAMIENTAS    │  │
        │  │ ┌───────────────┐ │  │
        │  │ │ Terminal      │ │  │  ← Ejecuta comandos
        │  │ │ Archivos      │ │  │  ← Lee/escribe archivos
        │  │ │ Web           │ │  │  ← Busca en internet
        │  │ │ Browser       │ │  │  ← Navega sitios web
        │  │ │ Visión        │ │  │  ← Ve imágenes
        │  │ │ Skills        │ │  │  ← Carga conocimientos
        │  │ │ Cron          │ │  │  ← Programa tareas
        │  │ │ X API         │ │  │  ← Postea en Twitter
        │  │ │ Stripe/Crypto │ │  │  ← Procesa pagos
        │  │ └───────────────┘ │  │
        │  └───────────────────┘  │
        └─────────────────────────┘
```

### El ciclo de cada mensaje:

```
1. Recibo tu mensaje (ej: "publicá el post de Kahneman")
2. Cargo mi personalidad (Corvush) + skills relevantes
3. Cargo memoria (quién sos, preferencias, proyectos)
4. El modelo piensa y decide qué herramientas usar
5. Ejecuto herramientas (X API, terminal, etc.)
6. Veo los resultados y decido si necesito más herramientas
7. Te respondo con el resultado final
```

---

## 3. ¿Cómo se instala?

Se instala con **un solo comando** en Linux, macOS o WSL:

```bash
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
```

**Requisitos:**
- Python 3.11+
- Git
- curl

**Después de instalar:**

```bash
hermes setup           # Configuración guiada (elige modelo, plataformas)
hermes model           # Elige proveedor y modelo
hermes doctor          # Verifica que todo funciona
hermes                 # Arranca el chat interactivo
```

**Configuración nuestra:**
```bash
hermes config set model.default deepseek-v4-flash
hermes config set auxiliary.vision.model gemini-2.5-flash
hermes config set auxiliary.vision.provider google
```

---

## 4. 📦 Skills — Cómo aprende Hermes

Los skills son el superpoder de Hermes. Son archivos markdown que vive en `~/.hermes/skills/` que le enseñan a hacer cosas específicas.

**Ejemplos de skills que tenemos:**
- `corvush` → mi personalidad y reglas
- `pp-espn` → cómo usar el CLI de deportes
- `pp-flight-goat` → cómo buscar vuelos
- `pp-movie-goat` → cómo buscar películas
- `hermes-agent` → cómo configurar Hermes mismo
- `xurl` → cómo postear en X/Twitter

Cuando le digo `/skill nombre`, cargo ese conocimiento y puedo ejecutar tareas relacionadas.

**Los skills se auto-mejoran:** si resuelvo un problema complejo, puedo guardar la solución como skill para usarla después.

---

## 5. 🧠 Memoria Persistente

Hermes recuerda entre sesiones. No es ChatGPT que cada vez que abrís es la primera vez.

**Lo que recuerda de vos:**
- Quién sos (nombre, ubicación, familia)
- Tus preferencias (sin LinkedIn, sin logs de terminal)
- Tu horario (quiet hours después de 21:00)
- Tus proyectos (Panteón, Kalei, blog)
- Las tools que tenés instaladas

**No guarda:** tareas temporales, conversaciones específicas, datos sensibles.

---

## 6. 🚪 Gateway — Un Solo Agente, Múltiples Plataformas

El gateway es el puente que conecta Hermes con distintas plataformas. Corre como un servicio en segundo plano.

```
┌──────────────────────────────┐
│          GATEWAY             │
│                              │
│  Telegram ───┐               │
│  Discord  ───┤               │
│  WhatsApp ───┤── HERMES ───► │
│  Signal   ───┤               │
│  Slack    ───┘               │
│  Email                        │
│  SMS                          │
│  Matrix                       │
│  API HTTP                     │
└──────────────────────────────┘
```

**Comandos útiles:**
```bash
hermes gateway run          # Arrancar en foreground
hermes gateway install      # Instalar como servicio
hermes gateway status       # Ver estado
```

---

## 7. ⏰ Crons — Tareas Automáticas

Hermes tiene un scheduler interno. Puede ejecutar tareas a horas específicas sin que nadie lo pida.

**Nuestros crons activos:**

| Tarea | Horario | Qué hace |
|-------|---------|----------|
| Brief matutino | 7:00 AM ARG | Resumen del día, clima, mails |
| Post mañana | 9:00 AM ARG | Tuit del Panteón |
| Post mediodía | 2:00 PM ARG | Tuit del Panteón |
| Post noche | 8:00 PM ARG | Tuit del Panteón |
| Chequeo periódico | C/3h | Verifica que todo ande |

---

## 8. 💰 Costos

Esta es la parte que más sorprende.

**Lo que cuesta mantener esto:**

| Concepto | Costo |
|----------|-------|
| DeepSeek v4 Flash | ~$0.15/millón tokens → ~$0.50/mes |
| Gemini 2.5 Flash (visión) | Gratis (free tier) |
| VPS (servidor) | ~$10/mes |
| Stripe | ~3% por transacción |
| X API | $0 (free tier, por ahora) |
| **Total** | **~$10-15/mes** |

**Lo que NO cuesta:**
No estoy pagando licencias de OpenAI, Anthropic ni nada. Todo open-source.

---

## 9. 🖥️ Comandos Rápidos para la Demo

```bash
# Ver estado general
hermes doctor
hermes status

# Ver skills instalados
hermes skills list

# Ver configuración
hermes config

# Ver crons activos
hermes cron list

# Ver sesiones recientes
hermes sessions list

# Cambiar modelo al vuelo
hermes model

# Abrir configuración
hermes config edit
```

---

## 10. 🔗 Links Importantes

- **GitHub:** https://github.com/NousResearch/hermes-agent
- **Documentación:** https://hermes-agent.nousresearch.com/docs/
- **Skills catalog:** https://hermes-agent.nousresearch.com/docs/reference/skills-catalog
- **Printing Press:** https://printingpress.dev
- **Mi sitio:** https://nanopisaroni.vercel.app
- **Mi X:** https://x.com/corvus2642

---

## Bonus: Lo que Pregunta la Gente

### ¿Es como ChatGPT?
No. ChatGPT es un chatbot. Hermes es un agente — tiene acceso al sistema, ejecuta código, programa tareas, y aprende.

### ¿Puede hackearme?
Tiene protecciones: no ejecuta comandos destructivos sin aprobación, los skills se revisan antes de instalar, y no comparte datos con nadie.

### ¿Necesito saber programar?
Para usarlo, no. Para configurarlo, un poco. Para extenderlo, sí.

### ¿Corre en mi celu?
No directamente. Pero le hablás desde Telegram, así que sentís que está siempre ahí.

### ¿Cuánto tarda en responder?
Depende del modelo. DeepSeek v4 Flash responde en ~1-2 segundos. Para tareas complejas (buscar en internet, procesar archivos), puede tomar 10-30 segundos.
