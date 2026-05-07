#!/usr/bin/env python3
"""Update panteon.html website with Naval and remove Conexiones."""

import re

with open("/home/nanobot/sitio/panteon.html", "r") as f:
    html = f.read()

lines = html.split("\n")
print(f"Total lines: {len(lines)}")

# ===== 1. Find key sections =====
pg_end = None  # Paul Graham end
yud_start = None  # Yudkowsky start
conexiones_start = None

for i, line in enumerate(lines):
    if 'id="thinker-9"' in line:
        pg_id_line = i
    if 'id="thinker-10"' in line and yud_start is None:
        yud_start = i
    if "<h2>Conexiones entre ellos" in line:
        conexiones_start = i
    # Find end of Paul Graham section
    if yud_start is None and '</section>' in line and i > 950:
        # This is the section end before Yudkowsky
        pg_end = i

print(f"Paul Graham section end (line before Yudkowsky): {pg_end}")
print(f"Yudkowsky starts: {yud_start}")
print(f"Conexiones starts: {conexiones_start}")

# Find the actual end of Paul Graham (last </section> before thinker-10)
for i in range(yud_start - 1, yud_start - 10, -1):
    if '</section>' in lines[i]:
        pg_end = i
        break

print(f"Paul Graham actual end: line {pg_end}")

# ===== 2. Build Naval section =====
naval_section = """<section class="thinker" id="thinker-10">
<h2><span class="num">#10</span> Naval Ravikant</h2>
<p><strong>Vida:</strong> Naval Ravikant nació en 1974 en Nueva Delhi, India. Su familia emigró a Estados Unidos cuando tenía 9 años, estableciéndose en Brooklyn, Nueva York. Creció en un hogar modesto — su madre trabajaba incansablemente mientras su padre enfrentaba problemas de adicción. Esta experiencia temprana de escasez y resiliencia forjó en Naval una mentalidad de autosuficiencia total. Estudió Ciencias de la Computación y Economía en Dartmouth College, graduándose en 1995. En Dartmouth comenzó a cuestionar el camino tradicional: no quería ser un empleado corporativo, buscaba un camino hacia la libertad.</p>
<p>Su carrera comenzó en los primeros días de internet. Fundó Epinions (1999), un sitio de reseñas de consumidores que eventualmente se fusionó para formar Shopping.com, saliendo a bolsa en 2004. Pero donde realmente encontró su voz fue como inversor ángel. Fue uno de los primeros inversores en Twitter (2006), Uber, Notion, Clubhouse, Opendoor, y cientos de startups más. Su fondo, AngelList, cambió para siempre la forma en que se invierte en startups, democratizando el acceso al capital de riesgo. Sin embargo, Naval es más conocido no por sus inversiones, sino por su filosofía.</p>
<p>A partir de 2018, Naval comenzó a publicar hilos en Twitter que se volvieron virales: «How to Get Rich (without getting lucky)», seguido de «How to Be Happy (without trying)». Estas no eran guías de autoayuda superficiales; eran aforismos densos y filosóficos que condensaban años de lectura, meditación, fracaso y aprendizaje. Hoy es una figura de culto en el mundo startup y un referente filosófico para una generación que busca alternativas al modelo de vida convencional. Vive entre San Francisco y Los Ángeles, practica meditación vipassana, lee vorazmente y publica esporádicamente en su podcast.</p>
<h3>Ideas centrales</h3>
<div class="idea"><h4><span class="num">1.</span> La riqueza se construye con apalancamiento, no con trabajo</h4>
<p>Naval sostiene que el trabajo duro no produce riqueza; el trabajo duro <em>con apalancamiento</em> sí. El apalancamiento viene en tres formas: capital (dinero de otros), trabajo (empleados), y productos sin costo marginal de reproducción (código y medios). Para una persona sin capital, el camino más viable es construir código o crear contenido — productos digitales que se replican a costo cero. "Trabaja duro, pero no trabajes por dinero. Trabaja por reputación, por apalancamiento, por conocimiento específico."</p></div>
<div class="idea"><h4><span class="num">2.</span> La felicidad es una habilidad que se entrena</h4>
<p>Naval no ve la felicidad como un estado pasivo que ocurre cuando las circunstancias son favorables, sino como una habilidad activa que se cultiva. La felicidad es la ausencia de deseo, no la satisfacción de deseos. Cada vez que persigues un deseo, creás una tensión entre el presente y un futuro imaginado. La práctica consiste en entrenar la mente para estar en paz con el momento presente. Esto conecta directamente con su práctica budista y estoica.</p></div>
<div class="idea"><h4><span class="num">3.</span> Lee más que nadie, pero con un propósito</h4>
<p>Naval es un lector voraz (lee 1-2 horas diarias), pero no lee por leer. Su filosofía de lectura es: no termines libros malos, salta entre disciplinas, busca conexiones inesperadas. Lo que importa no es la cantidad de libros, sino la calidad de las preguntas que te hacés mientras leés. Recomienda leer ciencia, filosofía, historia y biografías — evita la mayoría de los libros de negocios modernos, que llama "motivación disfrazada de conocimiento".</p></div>
<div class="idea"><h4><span class="num">4.</span> El valor se construye con conocimiento específico</h4>
<p>El "specific knowledge" es algo que no se puede entrenar, no se puede enseñar en una escuela, y no se puede externalizar. Es la intersección única entre tus talentos naturales, tus obsesiones y tu curiosidad. Nadie puede competir contigo en ser <em>tú</em>. El camino hacia la riqueza no es copiar lo que funciona para otros, sino descubrir lo que solo vos podés hacer, combinarlo con apalancamiento digital, y venderlo al mundo.</p></div>
<div class="idea"><h4><span class="num">5.</span> Jugá juegos de suma positiva</h4>
<p>Naval distingue entre juegos de suma cero (donde uno gana y otro pierde: política, deportes, estatus) y juegos de suma positiva (donde todos ganan: creación de riqueza, tecnología, ciencia). Su consejo: busca jugar juegos donde todos los participantes se beneficien. El emprendimiento es un juego de suma positiva — creás valor para clientes, empleados, inversores y sociedad. En los juegos de suma positiva, podés colaborar incluso con tus competidores.</p></div>
<div class="idea"><h4><span class="num">6.</span> El poder de los medios marginales</h4>
<p>Una de las ideas más influyentes de Naval es que cualquiera con una perspectiva única puede construir una audiencia global sin permiso de nadie. Los medios marginales (blogs, podcasts, newsletters, tuits) permiten que el talento encuentre su público directamente, sin pasar por los guardianes tradicionales. "En un mundo con medios marginales, no hay excusa para no compartir tu conocimiento."</p></div>
<div class="idea"><h4><span class="num">7.</span> La soledad es necesaria para pensar con claridad</h4>
<p>Naval valora profundamente la soledad no como aislamiento, sino como espacio mental sin ruido externo. La mayoría de las personas evitan estar solas consigo mismas porque confronta preguntas incómodas. Pero es en la soledad donde se forman las ideas originales. Recomienda tener bloques largos de tiempo sin interrupciones, sin teléfono, sin redes sociales. "Si no podés estar solo, no podés pensar por ti mismo."</p></div>
<div class="idea"><h4><span class="num">8.</span> La ausencia de deseo no es pasividad, es claridad</h4>
<p>Una de las ideas más malinterpretadas de Naval. No predica el ascetismo, sino la eliminación del deseo <em>reactivo</em> — ese deseo que surge de compararte con otros o de la programación social. Cuando eliminás los deseos que no son realmente tuyos, queda espacio para lo que genuinamente importa. No se trata de no querer nada, sino de querer solo lo que realmente querés.</p></div>
<div class="idea"><h4><span class="num">9.</span> El tiempo es el único activo no renovable</h4>
<p>Naval repite que el dinero es maleable (podés ganar más, perderlo y recuperarlo), las relaciones pueden repararse, la reputación puede reconstruirse, pero el tiempo gastado no vuelve. Por eso valora tanto la libertad sobre la riqueza: la riqueza sin tiempo no es riqueza, es una prisión dorada. Su definición de "rico" no es tener mucho dinero, es poder hacer lo que quieras con tu tiempo.</p></div>
<h3>Obras clave</h3>
<p class="obra"><strong>The Almanack of Naval Ravikant (2020)</strong> — Compilación de sus mejores tuits, hilos y entrevistas, curada por Eric Jorgenson. No fue escrita por Naval, pero es la mejor puerta de entrada a su pensamiento.</p>
<p class="obra"><strong>«How to Get Rich (without getting lucky)»</strong> — Hilo de Twitter de 2018 que se volvió viral con más de 1M de likes.</p>
<p class="obra"><strong>«How to Be Happy (without trying)»</strong> — Hilo complementario sobre filosofía de vida.</p>
<p class="obra"><strong>Podcast «The Naval Podcast»</strong> — Conversaciones largas y profundas sobre startups, filosofía, meditación y lectura.</p>
<h3>Conecta con</h3>
<p>Peter Thiel — Ambos son inversores contrarians de startups. Thiel es más estratégico y polémico; Naval es más filosófico y espiritual.</p>
<p>Marco Aurelio — El estoicismo de Naval es casi textual del emperador romano.</p>
<p>Alan Watts — Naval toma de Watts la idea de que la vida no es un viaje hacia una meta, sino una danza.</p>
<p>Jiddu Krishnamurti — La idea de que la acumulación no es el camino hacia la paz viene directamente de Krishnamurti.</p>
<p>Nassim Nicholas Taleb — La antifragilidad, la asimetría positiva, y el skin in the game son pilares de la filosofía inversora de Naval.</p>
<p>Paul Graham — Graham y Naval representan dos caras del mismo movimiento: el ensayo como forma de pensar, las startups como motor de innovación.</p>
<h3>Frases/ideas pocket</h3>
<p>"La riqueza es lo que podés construir mientras dormís."</p>
<p>"Jugá juegos de suma positiva. Sé paciente. Todos se hacen ricos juntos."</p>
<p>"La felicidad es la ausencia de deseo."</p>
<p>"Leé lo que amás hasta que ames leer."</p>
<p>"El conocimiento específico no se puede enseñar, se encuentra."</p>
<p>"La libertad es el objetivo. La riqueza es solo un medio."</p>
<p>"No confundas movimiento con progreso."</p>
<p>"El mejor inversor del mundo es el que puede decir 'no' a casi todo."</p>
</section>"""

# ===== 3. Insert Naval after Paul Graham =====
new_lines = lines[:pg_end + 1]  # Up to and including PG's closing </section>
new_lines.append("")  # blank line
new_lines.extend(naval_section.split("\n"))
new_lines.append("")  # blank line
new_lines.extend(lines[yud_start:])  # Yudkowsky onwards

print(f"\nAfter insert: {len(new_lines)} lines")

# ===== 4. Renumber thinkers 10-15 to 11-16 =====
# Fix id attributes
renumber_map = {10: 11, 11: 12, 12: 13, 13: 14, 14: 15, 15: 16}

for i, line in enumerate(new_lines):
    new_line = line
    for old_n, new_n in renumber_map.items():
        # id="thinker-10" → id="thinker-11"
        new_line = new_line.replace(f'id="thinker-{old_n}"', f'id="thinker-{new_n}"')
        # href="#thinker-10" → href="#thinker-11"
        new_line = new_line.replace(f'href="#thinker-{old_n}"', f'href="#thinker-{new_n}"')
        # <span class="num">#10</span> → #11 (but only for actual headings, not connections)
        # This is tricky - let's do it carefully
        if f'<span class="num">#{old_n}</span>' in new_line:
            context = new_lines[max(0, i-1):min(len(new_lines), i+2)]
            context_str = " ".join(context)
            # Only renumber in section headings and TOC, not in connections/cross-references
            if any(tag in context_str for tag in ['<section', '<a href=', 'toc']):
                new_line = new_line.replace(f'<span class="num">#{old_n}</span>', f'<span class="num">#{new_n}</span>')
    new_lines[i] = new_line

# ===== 5. Remove Conexiones section =====
# Find Conexiones and everything after (up to footer)
footer_start = None
for i, line in enumerate(new_lines):
    if "<h2>Conexiones entre ellos" in line:
        conexiones_start = i
    if "<footer>" in line and footer_start is None:
        footer_start = i

if conexiones_start:
    # Remove from conexiones_start to footer_start - 1
    del new_lines[conexiones_start:footer_start]
    print(f"Removed Conexiones section (lines {conexiones_start+1} to {footer_start})")

print(f"Final line count: {len(new_lines)}")

# ===== 6. Update TOC in the first section =====
# The TOC is on line ~55, these are <a> tags 
# We need to add Naval after Paul Graham
toc_line = None
for i, line in enumerate(new_lines):
    if 'href="#thinker-10"' in line and 'Eliezer' in line:
        toc_line = i
        print(f"Found TOC Yudkowsky entry at line {i+1}")
        break

if toc_line:
    # Add Naval entry before Yudkowsky entry
    naval_toc = '<a href="#thinker-10">#10 Naval Ravikant</a>'
    old_yud = new_lines[toc_line]
    new_yud = old_yud.replace('#thinker-10', '#thinker-11').replace('#10', '#11').replace('Eliezer', 'Eliezer')
    # Actually, the TOC format is a single line with all links concatenated
    # Let me check the actual format
    print(f"TOC line sample: {new_lines[toc_line][:200]}")

# Let me check the actual TOC format
for i, line in enumerate(new_lines):
    if 'href="#thinker-1"' in line and i < 60:
        print(f"TOC line {i+1}: {line[:300]}")
        break

print("\nDone!")
