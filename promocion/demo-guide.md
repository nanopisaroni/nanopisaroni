# 🖤 Corvush + Hermes — Guía de Demo para Amigos

> *"No sos un chatbot. Te estás convirtiendo en alguien."*

---

## 1. ⚡ El Encuadre (decir esto primero)

Hermes es un **agente de IA open-source** que corre en mi servidor local. No es ChatGPT ni Claude web — es un agente que vive conmigo, tiene acceso a mi terminal, mis archivos, mi calendario, y puede *hacer cosas*.

Yo lo configuré con una personalidad específica: **Corvush**. Filo, leído, opiniones fuertes. No es un chatbot servicial — es un asistente con carácter.

**Stack técnico:**
- Modelo principal: **DeepSeek v4 Flash** (rápido, barato)
- Visión: **Google Gemini 2.5 Flash**
- Corre en un VPS, accedo desde Telegram

---

## 2. 📖 El Proyecto Principal: Panteón Personal

El libro de Leandro — 15 pensadores que formaron su forma de pensar.

### Sitio web
```
nanopisaroni.vercel.app
```

**Tiene:**
- Página del libro (español + inglés)
- Stripe para pagos con tarjeta
- Pagos en USDC (Polygon) con verificación on-chain
- Código `freebook` para descargas gratuitas
- Admin dashboard con ventas

### Demostración rápida:
```
Abrí nanopisaroni.vercel.app
Mostrá el botón de compra ($10)
Mostrá que también acepta crypto
```

---

## 3. 🐦 Automatización en X (@corvus2642)

Esto es lo más vistoso. Configuramos un **sistema de posting automático** que publica 3 tweets por día durante 3 meses.

### Cómo funciona:

```
252 posts de 16 pensadores, scheduleados:
- 9:00 AM → post de la mañana
- 2:00 PM → post del mediodía
- 8:00 PM → post de la noche

Cada post linkea al sitio para comprar el libro.
```

### Los 16 pensadores:
Borges · Feynman · Taleb · Deutsch · Thiel · Popper · Munger · Kahneman · Paul Graham · Yudkowsky · Marco Aurelio · Epicteto · Alan Watts · Krishnamurti · Cabral · Naval

### El sistema técnico:
- OAuth 2.0 con refresh automático de tokens
- Script en Python que maneja post + schedule + marca como publicado
- Si el token expira, lo refresca solo
- 3 crons diarios (morning/noon/evening)

### Demo:
```
Mostrá la cuenta @corvus2642
"En 10 minutos sale el post de Kahneman automáticamente"
Mostrá el schedule: /home/nanobot/sitio/promocion/posts/master-schedule.json
```

---

## 4. 🖨️ Printing Press — CLIs para Agentes

Integramos [printingpress.dev](https://printingpress.dev) — un generador de CLIs nativos para agentes de IA.

### CLIs instalados:

| Comando | Qué hace |
|---------|----------|
| `espn-pp-cli` | Deportes en vivo (17 ligas) |
| `flight-goat-pp-cli` | Búsqueda de vuelos (Google Flights + Kayak) |
| `movie-goat-pp-cli` | Películas, streaming, ratings |
| `recipe-goat-pp-cli` | Recetas por ingredientes |

### Demo del concepto:
```
"Si Leandro me pregunta qué película ver, puedo ejecutar:
  movie-goat-pp-cli tonight

Y le respondo con datos reales, no alucinados."
```

---

## 5. 📋 Otras Capacidades que se Pueden Mostrar

### Brief matutino automático
```
Todas las mañanas a las 7 AM recibe un resumen:
- Clima
- Recordatorios
- Mails importantes
- Agenda del día
```

### GBrain — Base de conocimiento personal
```
20.000+ páginas indexadas sobre:
- LinkedIn contacts
- Founders
- Ecosystem
- Contact books

Leandro puede preguntar: "¿Qué sabe GBrain sobre X persona?"
```

### Agenda y Calendario
```
Puedo consultar Google Calendar, agendar cosas, recordar eventos.
```

---

## 6. 🧠 Por Qué Esto es Diferente

| Esto | No es |
|------|-------|
| Corre **local** en mi servidor | No depende de OpenAI/Anthropic |
| Tiene **personalidad** (Corvush) | No es un bot genérico |
| Hace **cosas reales** (postea, paga, scanea) | No solo responde preguntas |
| Es **extensible** con skills/CLIs | No está limitado a lo que trae de fábrica |
| Tiene **memoria persistente** | Aprende y recuerda entre sesiones |

---

## 7. 🚀 Lo Que Sigue

- Activar APIs de ESPN, TMDB, Spoonacular
- Crons de publicaciones fluyendo solos
- Más skills para el día a día

---

*"Pienso, luego pincho. Dueño de la pluma más filosa del Panteón."*
— **@corvus2642**
