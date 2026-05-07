#!/usr/bin/env python3
"""Complete update of panteon.html: add Naval, renumber, remove Conexiones, fix TOC."""

with open("/home/nanobot/sitio/panteon.html", "r") as f:
    html = f.read()

lines = html.split("\n")

# ===== 1. Find boundaries =====
pg_end = None
yud_start = None
conexiones_start = None

for i, line in enumerate(lines):
    if 'id="thinker-9"' in line:
        pg_id = i
    if 'id="thinker-10"' in line and yud_start is None:
        yud_start = i
    if "<h2>Conexiones entre ellos" in line:
        conexiones_start = i

# Find PG's closing </section> before Yudkowsky
for i in range(yud_start - 1, yud_start - 10, -1):
    if '</section>' in lines[i]:
        pg_end = i
        break

print(f"PG end: line {pg_end}, Yud start: line {yud_start}, Conexiones: line {conexiones_start}")

# ===== 2. Naval section HTML =====
naval_html = """<section class="thinker" id="thinker-10">
<h2><span class="num">#10</span> Naval Ravikant</h2>
<p><strong>Vida:</strong> Naval Ravikant naci\u00f3 en 1974 en Nueva Delhi, India. Su familia emigr\u00f3 a Estados Unidos cuando ten\u00eda 9 a\u00f1os, estableci\u00e9ndose en Brooklyn, Nueva York. Creci\u00f3 en un hogar modesto \u2014 su madre trabajaba incansablemente mientras su padre enfrentaba problemas de adicci\u00f3n. Esta experiencia temprana de escasez y resiliencia forj\u00f3 en Naval una mentalidad de autosuficiencia total. Estudi\u00f3 Ciencias de la Computaci\u00f3n y Econom\u00eda en Dartmouth College, gradu\u00e1ndose en 1995. En Dartmouth comenz\u00f3 a cuestionar el camino tradicional: no quer\u00eda ser un empleado corporativo, buscaba un camino hacia la libertad.</p>
<p>Su carrera comenz\u00f3 en los primeros d\u00edas de internet. Fund\u00f3 Epinions (1999), un sitio de rese\u00f1as de consumidores que eventualmente se fusion\u00f3 para formar Shopping.com, saliendo a bolsa en 2004. Pero donde realmente encontr\u00f3 su voz fue como inversor \u00e1ngel. Fue uno de los primeros inversores en Twitter (2006), Uber, Notion, Clubhouse, Opendoor, y cientos de startups m\u00e1s. Su fondo, AngelList, cambi\u00f3 para siempre la forma en que se invierte en startups, democratizando el acceso al capital de riesgo. Sin embargo, Naval es m\u00e1s conocido no por sus inversiones, sino por su filosof\u00eda.</p>
<p>A partir de 2018, Naval comenz\u00f3 a publicar hilos en Twitter que se volvieron virales: \u00abHow to Get Rich (without getting lucky)\u00bb, seguido de \u00abHow to Be Happy (without trying)\u00bb. Estas no eran gu\u00edas de autoayuda superficiales; eran aforismos densos y filos\u00f3ficos que condensaban a\u00f1os de lectura, meditaci\u00f3n, fracaso y aprendizaje. Hoy es una figura de culto en el mundo startup y un referente filos\u00f3fico para una generaci\u00f3n que busca alternativas al modelo de vida convencional. Vive entre San Francisco y Los \u00c1ngeles, practica meditaci\u00f3n vipassana, lee vorazmente y publica espor\u00e1dicamente en su podcast.</p>
<h3>Ideas centrales</h3>
<div class="idea"><h4><span class="num">1.</span> La riqueza se construye con apalancamiento, no con trabajo</h4>
<p>Naval sostiene que el trabajo duro no produce riqueza; el trabajo duro <em>con apalancamiento</em> s\u00ed. El apalancamiento viene en tres formas: capital (dinero de otros), trabajo (empleados), y productos sin costo marginal de reproducci\u00f3n (c\u00f3digo y medios). Para una persona sin capital, el camino m\u00e1s viable es construir c\u00f3digo o crear contenido \u2014 productos digitales que se replican a costo cero. "Trabaja duro, pero no trabajes por dinero. Trabaja por reputaci\u00f3n, por apalancamiento, por conocimiento espec\u00edfico."</p></div>
<div class="idea"><h4><span class="num">2.</span> La felicidad es una habilidad que se entrena</h4>
<p>Naval no ve la felicidad como un estado pasivo que ocurre cuando las circunstancias son favorables, sino como una habilidad activa que se cultiva. La felicidad es la ausencia de deseo, no la satisfacci\u00f3n de deseos. Cada vez que persigues un deseo, cre\u00e1s una tensi\u00f3n entre el presente y un futuro imaginado. La pr\u00e1ctica consiste en entrenar la mente para estar en paz con el momento presente. Esto conecta directamente con su pr\u00e1ctica budista y estoica.</p></div>
<div class="idea"><h4><span class="num">3.</span> Lee m\u00e1s que nadie, pero con un prop\u00f3sito</h4>
<p>Naval es un lector voraz (lee 1-2 horas diarias), pero no lee por leer. Su filosof\u00eda de lectura es: no termines libros malos, salta entre disciplinas, busca conexiones inesperadas. Lo que importa no es la cantidad de libros, sino la calidad de las preguntas que te hac\u00e9s mientras le\u00e9s. Recomienda leer ciencia, filosof\u00eda, historia y biograf\u00edas \u2014 evita la mayor\u00eda de los libros de negocios modernos, que llama "motivaci\u00f3n disfrazada de conocimiento".</p></div>
<div class="idea"><h4><span class="num">4.</span> El valor se construye con conocimiento espec\u00edfico</h4>
<p>El "specific knowledge" es algo que no se puede entrenar, no se puede ense\u00f1ar en una escuela, y no se puede externalizar. Es la intersecci\u00f3n \u00fanica entre tus talentos naturales, tus obsesiones y tu curiosidad. Nadie puede competir contigo en ser <em>t\u00fa</em>. El camino hacia la riqueza no es copiar lo que funciona para otros, sino descubrir lo que solo vos pod\u00e9s hacer, combinarlo con apalancamiento digital, y venderlo al mundo.</p></div>
<div class="idea"><h4><span class="num">5.</span> Jug\u00e1 juegos de suma positiva</h4>
<p>Naval distingue entre juegos de suma cero (donde uno gana y otro pierde: pol\u00edtica, deportes, estatus) y juegos de suma positiva (donde todos ganan: creaci\u00f3n de riqueza, tecnolog\u00eda, ciencia). Su consejo: busca jugar juegos donde todos los participantes se beneficien. El emprendimiento es un juego de suma positiva \u2014 cre\u00e1s valor para clientes, empleados, inversores y sociedad. En los juegos de suma positiva, pod\u00e9s colaborar incluso con tus competidores.</p></div>
<div class="idea"><h4><span class="num">6.</span> El poder de los medios marginales</h4>
<p>Una de las ideas m\u00e1s influyentes de Naval es que cualquiera con una perspectiva \u00fanica puede construir una audiencia global sin permiso de nadie. Los medios marginales (blogs, podcasts, newsletters, tuits) permiten que el talento encuentre su p\u00fablico directamente, sin pasar por los guardianes tradicionales. "En un mundo con medios marginales, no hay excusa para no compartir tu conocimiento."</p></div>
<div class="idea"><h4><span class="num">7.</span> La soledad es necesaria para pensar con claridad</h4>
<p>Naval valora profundamente la soledad no como aislamiento, sino como espacio mental sin ruido externo. La mayor\u00eda de las personas evitan estar solas consigo mismas porque confronta preguntas inc\u00f3modas. Pero es en la soledad donde se forman las ideas originales. Recomienda tener bloques largos de tiempo sin interrupciones, sin tel\u00e9fono, sin redes sociales. "Si no pod\u00e9s estar solo, no pod\u00e9s pensar por ti mismo."</p></div>
<div class="idea"><h4><span class="num">8.</span> La ausencia de deseo no es pasividad, es claridad</h4>
<p>Una de las ideas m\u00e1s malinterpretadas de Naval. No predica el ascetismo, sino la eliminaci\u00f3n del deseo <em>reactivo</em> \u2014 ese deseo que surge de compararte con otros o de la programaci\u00f3n social. Cuando elimin\u00e1s los deseos que no son realmente tuyos, queda espacio para lo que genuinamente importa. No se trata de no querer nada, sino de querer solo lo que realmente quer\u00e9s.</p></div>
<div class="idea"><h4><span class="num">9.</span> El tiempo es el \u00fanico activo no renovable</h4>
<p>Naval repite que el dinero es maleable (pod\u00e9s ganar m\u00e1s, perderlo y recuperarlo), las relaciones pueden repararse, la reputaci\u00f3n puede reconstruirse, pero el tiempo gastado no vuelve. Por eso valora tanto la libertad sobre la riqueza: la riqueza sin tiempo no es riqueza, es una prisi\u00f3n dorada. Su definici\u00f3n de "rico" no es tener mucho dinero, es poder hacer lo que quieras con tu tiempo.</p></div>
<h3>Obras clave</h3>
<p class="obra"><strong>The Almanack of Naval Ravikant (2020)</strong> \u2014 Compilaci\u00f3n de sus mejores tuits, hilos y entrevistas, curada por Eric Jorgenson. No fue escrita por Naval, pero es la mejor puerta de entrada a su pensamiento.</p>
<p class="obra"><strong>\u00abHow to Get Rich (without getting lucky)\u00bb</strong> \u2014 Hilo de Twitter de 2018 que se volvi\u00f3 viral con m\u00e1s de 1M de likes.</p>
<p class="obra"><strong>\u00abHow to Be Happy (without trying)\u00bb</strong> \u2014 Hilo complementario sobre filosof\u00eda de vida.</p>
<p class="obra"><strong>Podcast \u00abThe Naval Podcast\u00bb</strong> \u2014 Conversaciones largas y profundas sobre startups, filosof\u00eda, meditaci\u00f3n y lectura.</p>
<h3>Conecta con</h3>
<p>Peter Thiel \u2014 Ambos son inversores contrarians de startups. Thiel es m\u00e1s estrat\u00e9gico y pol\u00e9mico; Naval es m\u00e1s filos\u00f3fico y espiritual.</p>
<p>Marco Aurelio \u2014 El estoicismo de Naval es casi textual del emperador romano.</p>
<p>Alan Watts \u2014 Naval toma de Watts la idea de que la vida no es un viaje hacia una meta, sino una danza.</p>
<p>Jiddu Krishnamurti \u2014 La idea de que la acumulaci\u00f3n no es el camino hacia la paz viene directamente de Krishnamurti.</p>
<p>Nassim Nicholas Taleb \u2014 La antifragilidad, la asimetr\u00eda positiva, y el skin in the game son pilares de la filosof\u00eda inversora de Naval.</p>
<p>Paul Graham \u2014 Graham y Naval representan dos caras del mismo movimiento: el ensayo como forma de pensar, las startups como motor de innovaci\u00f3n.</p>
<h3>Frases/ideas pocket</h3>
<p>"La riqueza es lo que pod\u00e9s construir mientras dorm\u00eds."</p>
<p>"Jug\u00e1 juegos de suma positiva. S\u00e9 paciente. Todos se hacen ricos juntos."</p>
<p>"La felicidad es la ausencia de deseo."</p>
<p>"Le\u00e9 lo que am\u00e1s hasta que ames leer."</p>
<p>"El conocimiento espec\u00edfico no se puede ense\u00f1ar, se encuentra."</p>
<p>"La libertad es el objetivo. La riqueza es solo un medio."</p>
<p>"No confundas movimiento con progreso."</p>
<p>"El mejor inversor del mundo es el que puede decir 'no' a casi todo."</p>
</section>"""

naval_lines = naval_html.split("\n")

# ===== 3. Build new file =====
# Part A: Everything up to and including PG's closing </section>
new_lines = lines[:pg_end + 1]

# Part B: Naval section (as #10, thinker-10)
new_lines.append("")
new_lines.extend(naval_lines)
new_lines.append("")

# Part C: Yudkowsky onwards, renumbered
renumber_map = {10: 11, 11: 12, 12: 13, 13: 14, 14: 15, 15: 16}
renumber_order = [
    ("Eliezer Yudkowsky", 10, 11),
    ("Marco Aurelio", 11, 12),
    ("Epicteto", 12, 13),
    ("Alan Watts", 13, 14),
    ("Jiddu Krishnamurti", 14, 15),
    ("Facundo Cabral", 15, 16),
]

for i in range(yud_start, len(lines)):
    if i < conexiones_start:
        line = lines[i]
        new_line = line
        for name, old_n, new_n in renumber_order:
            new_line = new_line.replace(f'id="thinker-{old_n}"', f'id="thinker-{new_n}"')
            new_line = new_line.replace(f'<span class="num">#{old_n}</span>', f'<span class="num">#{new_n}</span>')
        new_lines.append(new_line)
    elif i == conexiones_start:
        # Skip Conexiones section entirely
        pass
    # Skip Conexiones lines
    # We need to find the footer and keep it

# Part D: Footer and after (if any content after Conexiones)
# Find the footer in the original file
footer_start = None
for i in range(conexiones_start, len(lines)):
    if "<footer>" in lines[i]:
        footer_start = i
        break

if footer_start:
    for i in range(footer_start, len(lines)):
        new_lines.append(lines[i])

# ===== 4. Fix TOC line =====
new_toc = '<a href="#thinker-1">#1 Jorge Luis Borges</a><a href="#thinker-2">#2 Richard Feynman</a><a href="#thinker-3">#3 Nassim Nicholas Taleb</a><a href="#thinker-4">#4 David Deutsch</a><a href="#thinker-5">#5 Peter Thiel</a><a href="#thinker-6">#6 Karl Popper</a><a href="#thinker-7">#7 Charlie Munger</a><a href="#thinker-8">#8 Daniel Kahneman</a><a href="#thinker-9">#9 Paul Graham</a><a href="#thinker-10">#10 Naval Ravikant</a><a href="#thinker-11">#11 Eliezer Yudkowsky</a><a href="#thinker-12">#12 Marco Aurelio</a><a href="#thinker-13">#13 Epicteto (y S\u00e9neca)</a><a href="#thinker-14">#14 Alan Watts</a><a href="#thinker-15">#15 Jiddu Krishnamurti</a><a href="#thinker-16">#16 Facundo Cabral</a>'

# Find and replace the old TOC
for i, line in enumerate(new_lines):
    if 'href="#thinker-1">#1' in line and 'href="#thinker-10"' in line:
        old_toc_content = line
        new_lines[i] = new_toc
        print(f"TOC updated at line {i+1}")
        break
    elif 'href="#thinker-1">#1' in line:
        # Old format, need to replace
        old_toc_content = line
        new_lines[i] = new_toc
        print(f"TOC updated at line {i+1} (old format)")
        break

# ===== 5. Write =====
output = "\n".join(new_lines)
with open("/home/nanobot/sitio/panteon.html", "w") as f:
    f.write(output)

# ===== 6. Verify =====
print(f"\nFinal: {len(new_lines)} lines")
# Count sections
import re
sections = re.findall(r'id="thinker-\d+"', output)
print(f"Thinker sections: {len(sections)}")
for s in sorted(set(sections)):
    print(f"  {s}")

# Check headings
for line in new_lines:
    if '<h2><span class="num">' in line:
        print(f"  Heading: {line.strip()}")

# Check for Conexiones
if "<h2>Conexiones entre ellos" in output:
    print("WARNING: Conexiones still present!")
else:
    print("Conexiones removed OK")

# Check for Naval's main section
if "Naval Ravikant" in output:
    naval_count = output.count("Naval Ravikant")
    print(f"Naval Ravikant mentioned {naval_count} times (should be >5)")
else:
    print("WARNING: Naval not found!")
