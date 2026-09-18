"""Swap the new on-body shoot (Sept 18, interim edit) into the imagery board.
Each photo is embedded ONCE as a CSS class, so the four page mocks reuse it."""
import io
p = 'C:/Users/wetzl/Lucky Golf/Website/tools/gwp-preview/build-imagery-board.cjs'
s = io.open(p, encoding='utf-8').read()
def r(a, b):
    global s
    assert a in s, a[:80]
    s = s.replace(a, b, 1)

# 1. load the shoot + emit CSS classes
r("/* ---------- one page mock", """const SHOOT_DIR = path.join(ROOT, 'design/img/shoot-0918');
const SHOOT = ['green-read-fit', 'fit-sunset', 'fit-sunset-down', 'swing-black-wedge', 'two-gold-wedges', 'black-hat-mallet',
  'two-hats-mallet', 'gold-wedge-bag', 'putt-sunset', 'from-the-cup', 'putter-in-hand', 'walk-off-green'];
const SHOOT_CSS = SHOOT.map(n => `.s-${n}{background-image:url(data:image/webp;base64,${fs.readFileSync(path.join(SHOOT_DIR, n + '.webp')).toString('base64')})}`).join('\\n');
const ph = (n, cls = '', pos = 'center') => `<div class="bgph s-${n} ${cls}" style="background-position:${pos}"></div>`;

/* ---------- one page mock""")

# 2. hero: the golfer reading the putt, in the hat + polo, gold putter
r("""  <section class="hero" style="background-image:url('${IMG.heroFairway}')">""",
  """  <section class="hero s-green-read-fit">""")
# 3. band: two gold wedges wide, the black hat + mallet, the wedge on the bag
r("""    <figure class="w2"><img src="${IMG.strykerCourse}" alt=""></figure>
    <figure><img src="${IMG.malletGreen}" alt=""></figure>
    <figure><img src="${IMG.noParking}" alt=""></figure>""",
  """    <figure class="w2">${ph('two-gold-wedges')}</figure>
    <figure>${ph('black-hat-mallet', '', '30% center')}</figure>
    <figure>${ph('gold-wedge-bag', '', '45% center')}</figure>""")
# 4. the fit: the real on-body shot replaces the empty slot
r("""    ${slot('The fit, worn', 'A golfer in the Lucky hat + polo, walking off the green, low sun. 4:5. This is the photo the whole offer is selling.', 'fit-photo')}""",
  """    <figure class="fit-ph">${ph('fit-sunset', '', '52% center')}<figcaption>The fit: hat + polo, both free over $140</figcaption></figure>""")
# 5. reviews over the sunset putt; FAQ closes on the ball coming out of the cup
r("""  <section class="reviews" style="background-image:url('${IMG.puttersGreen}')">""", """  <section class="reviews s-putt-sunset">""")
r("""    <figure class="faq-ph"><img src="${IMG.sand}" alt=""></figure>""", """    <figure class="faq-ph">${ph('from-the-cup', '', '40% center')}</figure>""")
# 6. rhythm strips use the shoot too
s = s.replace("""<div class="p" style="background-image:url('${IMG.heroFairway.replace('2000', '800')}')">Photo hero</div>""",
              """<div class="p s-green-read-fit" style="background-position:center 35%">Photo hero</div>""")
s = s.replace("""<div class="p" style="background-image:url('${IMG.strykerCourse.replace('1600', '800')}')">Photo band</div>""",
              """<div class="p s-two-gold-wedges">Photo band</div>""")
s = s.replace("""<div class="p" style="background-image:url('${IMG.puttersGreen.replace('2000', '800')}')">Reviews on a photo</div>""",
              """<div class="p s-putt-sunset">Reviews on a photo</div>""")

# 7. CSS: classes + photo boxes
r("""/* shot list */""", """.bgph{width:100%;height:100%;background-size:cover}
.hero,.reviews{background-size:cover}
.hero{background-position:62% 40%}
.reviews{background-position:center 60%}
.fit-ph{margin:0;aspect-ratio:4/5;border-radius:18px;overflow:hidden;position:relative}
.fit-ph figcaption{position:absolute;left:16px;bottom:16px;background:rgba(6,17,11,.72);color:#F4F3F0;font:700 12px Archivo;letter-spacing:.1em;text-transform:uppercase;padding:8px 12px;border-radius:8px}
.band figure{height:100%}
@container (max-width:600px){.hero{background-position:58% center}}
${SHOOT_CSS}
/* shot list */""")

# 8. copy: the subhead + the fit note no longer say "the one shot we don't have"
r("""<p class="hs">Real photos from your store. The dashed gold box is the one shot we don't have: the hat and polo actually worn. It's the most important image on the page because the fit is what the offer sells.</p>""",
  """<p class="hs">Built on the new shoot (interim edit). The hero is the hat, the polo and a gold putter in one frame, which is the whole offer. The fit section finally shows the gifts worn instead of floating on tiles.</p>""")

# 9. "have" grid leads with the shoot; the need list moves on
r("""<h2 class="h">Photos we have (already in your store)</h2>
<div class="have">""", """<h2 class="h">Photos we have</h2>
<p class="hs">Top row: the new shoot, interim edit. Below: what's already in your store.</p>
<div class="have">
  ${[['Reading the putt · hero', 'green-read-fit'], ['The fit, low sun', 'fit-sunset'], ['Head down, sun', 'fit-sunset-down'], ['Follow-through, black wedge', 'swing-black-wedge'],
     ['Two gold wedges', 'two-gold-wedges'], ['Black hat + mallet', 'black-hat-mallet'], ['Two hats + mallet', 'two-hats-mallet'], ['Gold wedge on the bag', 'gold-wedge-bag'],
     ['Putting at sunset', 'putt-sunset'], ['Out of the cup', 'from-the-cup'], ['Putter in hand', 'putter-in-hand'], ['Walking off', 'walk-off-green']]
    .map(([c, n]) => `<figure><div class="bgph s-${n}" style="aspect-ratio:1;border-radius:10px"></div><figcaption>${c}</figcaption></figure>`).join('')}""")

r("""<tr><td><span class="p1">1</span></td><td><b>The fit, worn.</b> Golfer in a Lucky hat + polo, walking off the green or pulling a club, low sun.</td><td>Promo hero option, "free stuff" section, apparel pages, ads</td><td>4:5 + 16:9 crop, 2 or 3 people/looks</td></tr>""",
  """<tr><td><span class="p2">done</span></td><td><b>The fit, worn.</b> Covered by the new shoot (one golfer, two looks). Still want a second person for range.</td><td>Promo hero, fit section, apparel pages, ads</td><td>Final edit from your creative director</td></tr>""")
io.open(p, 'w', encoding='utf-8').write(s)
print('patched')
