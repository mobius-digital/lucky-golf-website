"""Hero gift photos: optional pickers, falling back to the gift product's first variant."""
import io
ROOT = "C:/Users/wetzl/Lucky Golf/Website/"
def patch(p, pairs):
    s = io.open(ROOT + p, encoding='utf-8').read()
    for a, b in pairs:
        assert a in s, (p, a[:70]); s = s.replace(a, b, 1)
    io.open(ROOT + p, 'w', encoding='utf-8').write(s)

patch('shopify/sections/gwp-promo.liquid', [
("""    assign hat_img = hat.variants.first.image | default: hat.featured_image
    assign polo_img = polo.variants.first.image | default: polo.featured_image""",
"""    assign hat_img = s.hero_hat_image | default: hat.variants.first.image | default: hat.featured_image
    assign polo_img = s.hero_polo_image | default: polo.variants.first.image | default: polo.featured_image"""),
("""    { "type": "text", "id": "both_free_tag", "label": "Row 2 tag", "default": "Both free" },""",
"""    { "type": "text", "id": "both_free_tag", "label": "Row 2 tag", "default": "Both free" },
    { "type": "image_picker", "id": "hero_hat_image", "label": "Hero hat photo (optional)", "info": "Blank = the free hat's first variant photo. Use the black and gold hat." },
    { "type": "image_picker", "id": "hero_polo_image", "label": "Hero polo photo (optional)", "info": "Blank = the free polo's first variant photo." },"""),
])
# the preview uses the same two photos the page should (black/gold hat, Gold Dust polo)
patch('tools/gwp-preview/build3.cjs', [
("const HATIMG = GIFTS.hat.variants[0].img, POLOIMG = GIFTS.polo.variants[0].img;",
 "/* stands in for the two hero image pickers */\nconst HATIMG = P['black-gold-classic-lucky-hat'].images[0].src, POLOIMG = P['gold-dust-classic-polo'].images[0].src;"),
])
print('ok')
