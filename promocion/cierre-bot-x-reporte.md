# Bot de X / Panteón - Reporte de Cierre

**Fecha:** 2026-05-18
**Motivo:** Se deja de usar la cuenta de X (@corvus2642) para promoción del Panteón Personal.

---

## Estado al cierre

### Posts publicados
- **28 tweets** posteados exitosamente (vía posting-log.json)
- **1 post marcado como posted** en master-schedule (el primero, de Naval, 2026-05-14)
- **479 posts pendientes** sin publicar (nunca llegaron a postearse)

### Cronograma
- **Inicio planificado:** 2026-05-15
- **Fin planificado:** 2026-10-21
- **Total posts planeados:** 480 (16 pensadores × 30 días)

### Pensadores cubiertos (16)
Borges, Cabral, Deutsch, Epicteto, Feynman, Graham (PG), Kahneman, Krishnamurti, Marco Aurelio, Munger, Naval, Popper, Taleb, Thiel, Watts, Yudkowsky

### Último tweet posteado
- **Pensador:** Naval
- **ID:** 2055060641489010880
- **Fecha:** 2026-05-14
- **Texto:** "The best form of leverage is products with no marginal cost of replication. Code and media are permissionless leverage t..."

---

## Infraestructura

### Scripts
- `post-tweet.py` — script principal de posting (usa OAuth2 de X API v2)
- `agents/cron-poster.py` — poster alternativo basado en agentes
- `agents/batch-generate.py` — generación batch de contenido
- `agents/batch-gen-cli.py` — CLI de generación
- `agents/panteon-agents.py` — sistema de agentes para contenido
- `agents/combine-posts.py` — combina posts generados
- `post-next-pending.py` — postea el siguiente pendiente

### Datos
- `posts/master-schedule.json` — schedule maestro (480 entradas, metadatos)
- `posts/posting-log.json` — log de 28 posts realizados
- `posts/posts-borges.json` — batch específico de Borges
- `posts/readable-schedule.txt` — schedule legible (96 líneas)
- `agents/data/` — schedules semanales generados (CSV)
- `agents/logs/` — logs de ejecución (diarios + semanales)

### Credenciales
- `~/.panteon_twitter.json` — OAuth2 tokens de X API (395 bytes)

### Imágenes
- `images/` — quotes generados como PNG para acompañar tweets (Borges, Yudkowsky, Deutsch, Marco Aurelio, Popper, etc.)

### Cron jobs relacionados
| Nombre | Job ID | Estado |
|--------|--------|--------|
| panteon-promo-daily | 6fa50f260718 | Pausado |
| panteon-post-morning | 42674fb4cc18 | Pausado |
| panteon-post-noon | 577d53115a66 | Pausado |
| panteon-post-evening | 85a094963653 | Pausado |
| Panteon Catchup - cada 30min | 0ff884515a38 | Pausado |
| panteon-weekly-schedule | b74aa3c9e4e2 | Activo (genera schedule semanal) |

### Tamaño total del proyecto
- Directorio `~/sitio/promocion/`: ~500KB aprox.
- Src principal: post-tweet.py (~200 líneas)
- Credenciales X API: OAuth2 con refresh token

---

## Notas
- El sistema funcionaba con X API v2 via OAuth2 (Bearer token + refresh)
- 3 slots diarios: morning (9AM), noon (2PM), evening (8PM ART)
- El schedule de 480 posts cubría 160 días corridos
- Solo se alcanzó a postear 28 tweets (días ~1 a ~10), el último el 2026-05-14
- Los crons ya estaban pausados desde el 14/05 — solo falta removerlos

---

*Archivo generado automáticamente por Corvush. Guardado como registro de aprendizaje.*
