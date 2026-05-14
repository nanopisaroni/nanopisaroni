# SOCIAL MEDIA GROWTH ENGINE -- COMPLETO
## @corvus2642 / @PanteonBook | AI + Filosofia + Crypto
## Meta: 0->10K en 90 dias -> Ventas del libro ($10 c/u)
---

## 1. REPLY-GUY ESTRATEGIA (EN X)
### Que es?
Comentar en hilos virales de cuentas grandes para captar atencion.

### Donde encontrar hilos
AI: @kareem_carr, @nickfloats, @alexgarcia, @danielmiessler, @levelsio
Filosofia: @dailystoic, @philosophy, @david_perell, @visakanv
Crypto: @BasedBeffJezos, @balajis, @naval, @cobie
Escritura: @dickiebush, @nicolascole77, @AlexAndBooks_

### Sistema 3 pasos (30 min/dia)
1. BUSQUEDA (10 min): X search "min_faves:100 AI philosophy" etc.
2. ANALISIS (10 min): encontrar el hueco en el hilo
3. REDACION (10 min): reply 1-3 tweets, NO links directos

### Templates
- Agregar matiz: "Building on this -- X showed that..."
- Pregunta deep: "Good thread. How do you reconcile this with...?"
- Cita + twist: "As Taleb says: Skin in the game..."

### NO hacer
- Spam de links
- Solo emojis
- 5 replies al mismo OP
- Replies random

---

## 2. ENGAGEMENT PODS
### Que es?
Grupo de 5-15 cuentas que se like+reply+RT mutuamente.

### Como armarlo
FASE 1: Reclutar 20 cuentas (500-5000 seguidores) via DM
FASE 2: Grupo Telegram/DM con reglas (60 min para responder)
FASE 3: Escalar a 2 pods (EN + ES)

### Herramientas: X Lists, TweetDeck, Telegram, Typefully

---

## 3. THREAD STORMS
### Formula viral
HOOK: Revelacion, Contrarian, Numeros, Historia, o Como
SETUP (1-2 tweets): Why this matters
CONTENIDO (5-7 tweets): Problem -> Fact -> Story -> Framework -> Example
CTA: Like + RT + Follow + Link al libro

### 10 ideas de hilos @corvus2642
1. Borges predijo internet en 1941. (Borges, Deutsch)
2. Feynman, Taleb y Munger walk into a bar. (Feynman, Taleb, Munger)
3. Pedi a 3 Claude que discutan si AI tiene intuicion. (Kahneman, Deutsch)
4. Estoicos tenian framework para crypto: Memento Mori. (Aurelius, Taleb)
5. Alignment de AI no es tecnico, es epistemologico. (Deutsch, Yudkowsky)
6. 7 modelos mentales para no comprar NFTs. (Munger, Taleb, Kahneman)
7. Como explicar AGI a un nino con Borges y LEGOs. (Borges, Feynman)
8. Inversion (Munger) aplicado a crypto. (Munger, Taleb)
9. Lo que AI nunca podra hacer (Deutsch). (Deutsch, Feynman)
10. 3 citas que cambiaron mi forma de escribir. (Feynman, Borges, Taleb)

### Calendar: LUNES (AI+filo EN), JUEVES (crypto+filo)

---

## 4. CONVERTIR SEGUIDORES EN VENTAS ($10)
### Funnel
FOLLOWERS -> FREE VALUE -> LEAD MAGNET -> SOCIAL PROOF -> SALE

### Puntos de conversion
- BIO: "Autor de Personal Pantheon -- 16 thinkers -> link"
- Fin de threads: CTA
- Replies con interes: "I go deeper in my book -> link"
- Newsletter: 3 emails post-captura

### Numeros: $9.99 EN (~$7 neto). 72 ventas/mes = $500. A 10K followers = 0.5-1% conv.

---

## CRON JOBS -- COMANDOS EXACTOS
### 1. Instalar cron
sudo apt-get install cron -y
sudo systemctl enable cron
sudo systemctl start cron

### 2. Editar crontab
crontab -e

### 3. Pegar:
0 9 * * * cd /home/nanobot/sitio/promocion && python3 post-tweet.py morning >> agents/logs/cron-morning.log 2>&1
0 14 * * * cd /home/nanobot/sitio/promocion && python3 post-tweet.py noon >> agents/logs/cron-noon.log 2>&1
0 20 * * * cd /home/nanobot/sitio/promocion && python3 post-tweet.py evening >> agents/logs/cron-evening.log 2>&1
30 10 * * * cd /home/nanobot/sitio/promocion && python3 growth-engine.py reply-scan >> data/reply-scan.log 2>&1
0 15 * * * cd /home/nanobot/sitio/promocion && python3 growth-engine.py reply-scan >> data/reply-scan.log 2>&1
30 21 * * * cd /home/nanobot/sitio/promocion && python3 growth-engine.py reply-scan >> data/reply-scan.log 2>&1
0 */6 * * * cd /home/nanobot/sitio/promocion && python3 growth-engine.py trending >> data/trending.log 2>&1
0 8-22 * * * cd /home/nanobot/sitio/promocion && python3 growth-engine.py track >> data/track.log 2>&1
0 23 * * * cd /home/nanobot/sitio/promocion && python3 growth-engine.py report >> data/report.log 2>&1

### 4. Verificar: crontab -l
### 5. Logs: tail -f data/reply-scan.log
