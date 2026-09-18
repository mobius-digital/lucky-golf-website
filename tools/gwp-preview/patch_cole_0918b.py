"""Cole's round, 2026-09-18 afternoon:
FAQ photo was nested in the reviews band (fix), band crops, toast off the rail,
no green on 'added', no quantity steppers, a Mags sign-off to close the page."""
import io
ROOT = 'C:/Users/wetzl/Lucky Golf/Website/shopify/'
def edit(rel, pairs):
    p = ROOT + rel
    s = io.open(p, encoding='utf-8', newline='').read()
    for a, b in pairs:
        assert s.count(a) == 1, (rel, a[:70], s.count(a))
        s = s.replace(a, b, 1)
    io.open(p, 'w', encoding='utf-8', newline='').write(s)
    print('ok', rel)

FAQ_FIG = """      {%- if s.faq_photo != blank -%}
        <figure class="gwp-faq-ph">{{ s.faq_photo | image_url: width: 1200 | image_tag: widths: '600,1200', sizes: '(max-width:749px) 100vw, 40vw', loading: 'lazy', alt: s.faq_photo.alt }}</figure>
      {%- endif -%}
"""
SIGN = """
  <!-- ══════════ SIGN-OFF · Mags closes the page ══════════ -->
  {%- if s.sign_line != blank -%}
    <section class="gwp-sign">
      <div class="lg-wrap">
        {%- if s.sign_eyebrow != blank -%}<p class="lg-eyebrow">{{ s.sign_eyebrow }}</p>{%- endif -%}
        <h2 class="lg-d1 gwp-sign-h">{{ s.sign_line }}</h2>
        {%- if s.sign_sub != blank -%}<p class="lg-lede gwp-sign-sub">{{ s.sign_sub }}</p>{%- endif -%}
        <a class="lg-btn lg-btn-line" href="#gwp-clubs" data-scroll-to="gwp-clubs">{{ s.sign_cta }} <span aria-hidden="true">&rarr;</span></a>
        <div class="gwp-sign-mags" aria-hidden="true"><img src="{{ 'gwp-mags.webp' | file_url }}" alt="" width="96" height="60" loading="lazy"></div>
      </div>
    </section>
  {%- endif -%}
"""

edit('sections/gwp-promo.liquid', [
    # 1. the FAQ photo goes back where it belongs (it had landed inside the reviews band)
    ("""        </div>
      </div>
""" + FAQ_FIG + """      </div>
    </section>
  {%- endif -%}

  <!-- ══════════ FAQ""", """        </div>
      </div>
    </section>
  {%- endif -%}

  <!-- ══════════ FAQ"""),
    ("""          {%- endfor -%}
        </div>
      </div>
    </section>
  {%- endif -%}

  <!-- ══════════ PHONE CART BAR""", """          {%- endfor -%}
        </div>
      </div>
""" + FAQ_FIG + """      </div>
    </section>
  {%- endif -%}
""" + SIGN + """
  <!-- ══════════ PHONE CART BAR"""),
    # 2. one club per golfer: no quantity steppers
    ("""                <div class="gwp-qty" role="group" aria-label="How many">
                  <button type="button" data-qty="-1" aria-label="One fewer">&minus;</button>
                  <output data-qty-out>1</output>
                  <button type="button" data-qty="1" aria-label="One more">+</button>
                </div>
""", ""),
    # 3. schema
    ("""    { "type": "header", "content": "Toasts" },""",
     """    { "type": "header", "content": "Sign-off" },
    { "type": "text", "id": "sign_eyebrow", "label": "Eyebrow", "default": "Ends Friday, Sept 25" },
    { "type": "text", "id": "sign_line", "label": "Line", "info": "Leave empty to hide the sign-off.", "default": "The hat's free. So's the polo." },
    { "type": "text", "id": "sign_sub", "label": "Sub", "default": "Legend has it Mags hasn't paid for a hat in years. This week you get to find out how that feels." },
    { "type": "text", "id": "sign_cta", "label": "Button", "default": "Pick your club" },

    { "type": "header", "content": "Toasts" },"""),
])

edit('templates/page.gwp-promo.json', [
    ('''        "faq_photo": "shopify://shop_images/gwp-faq-cup.webp"''',
     '''        "faq_photo": "shopify://shop_images/gwp-faq-cup.webp",
        "sign_eyebrow": "Ends Friday, Sept 25",
        "sign_line": "The hat's free. So's the polo.",
        "sign_sub": "Legend has it Mags hasn't paid for a hat in years. This week you get to find out how that feels.",
        "sign_cta": "Pick your club"'''),
])

edit('assets/gwp-promo.css', [
    # toast: off the rail. Desktop: bottom centre. Phones: the bars live at the bottom, so it stays up top.
    (""".gwp-toast{position:fixed;left:50%;top:14px;translate:-50% 0;z-index:100;margin:0;""",
     """.gwp-toast{position:fixed;left:50%;bottom:28px;translate:-50% 0;z-index:100;margin:0;"""),
    ("""@media (prefers-reduced-motion:reduce){.gwp-toast-mags{animation:none}}""",
     """@media (prefers-reduced-motion:reduce){.gwp-toast-mags{animation:none}}
@media (max-width:749px){.gwp-toast{bottom:auto;top:14px}}"""),
    # added: ink, not the state green (green read as a stray colour on the gold/white page)
    (""".lg-btn[data-done],.lg-btn-line[data-done]{background-image:none;background:var(--lg-ok);color:var(--lg-page);border-color:var(--lg-ok)}""",
     """.lg-btn[data-done],.lg-btn-line[data-done]{background-image:none;background:var(--lg-ink);color:var(--lg-page);border-color:var(--lg-ink)}"""),
    (""".gwp-gift[data-state="claimed"]{border-color:var(--lg-ok)}""",
     """.gwp-gift[data-state="claimed"]{border-color:var(--lg-gold)}"""),
    # band: the shoot is 3:2, so the tiles are 3:2. No more portrait crops of landscape frames.
    (""".gwp-band-ph{display:grid;grid-template-columns:2fr 1fr 1fr;gap:6px;height:clamp(300px,34vw,460px)}
.gwp-band-f{margin:0;overflow:hidden;min-width:0}""",
     """.gwp-band-ph{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:6px}
.gwp-band-f{margin:0;overflow:hidden;min-width:0;aspect-ratio:3/2}"""),
    ("""  .gwp-band-ph{grid-template-columns:1fr 1fr;height:auto}
  .gwp-band-f{aspect-ratio:1}
  .gwp-band-f.w2{grid-column:1/-1;aspect-ratio:16/10}""",
     """  .gwp-band-ph{grid-template-columns:1fr 1fr}
  .gwp-band-f.w2{grid-column:1/-1}"""),
    # FAQ photo: whole frame, not a tall crop
    (""".gwp-faq-ph{margin:0;border-radius:var(--rc,18px);overflow:hidden;aspect-ratio:4/5}""",
     """.gwp-faq-ph{margin:0;border-radius:var(--rc,18px);overflow:hidden;aspect-ratio:3/2}"""),
    ("""@media (max-width:749px){ .gwp-faq-grid.has-ph{grid-template-columns:1fr} .gwp-faq-ph{aspect-ratio:4/3} }""",
     """@media (max-width:749px){ .gwp-faq-grid.has-ph{grid-template-columns:1fr} }
@media (min-width:750px) and (max-width:1080px){ .gwp-faq-grid.has-ph{grid-template-columns:1fr} .gwp-faq-ph{max-width:640px} }

/* sign-off: Mags closes the page on a gold line */
.gwp-sign{padding:clamp(56px,8vw,112px) 0 clamp(40px,6vw,72px);text-align:center;border-top:1px solid var(--lg-rule)}
.gwp-sign .lg-eyebrow{justify-content:center}
.gwp-sign-h{max-width:16ch;margin:14px auto 0;text-wrap:balance}
.gwp-sign-sub{max-width:46ch;margin:16px auto 28px;color:var(--lg-ink-64)}
.gwp-sign-mags{position:relative;margin-top:44px;height:60px}
.gwp-sign-mags::before{content:'';position:absolute;left:0;right:0;top:50%;height:2px;background:var(--lg-foil)}
.gwp-sign-mags img{position:relative;display:block;margin:0 auto;width:96px;height:auto;background:var(--lg-page);padding:0 16px;box-sizing:content-box}
.gwp[data-yardage="on"] .gwp-sign .lg-eyebrow{counter-increment:none}
.gwp[data-yardage="on"] .gwp-sign .lg-eyebrow::before{content:none}"""),
])
