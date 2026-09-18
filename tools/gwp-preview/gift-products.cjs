/* The two gift products, built from the live catalogue (Admin API pull, 2026-09-18).
   - Same SKU as the real item, so the warehouse (Ceries OMS) ships the real hat/polo
   - Stock = the real item's stock at Ceries OMS right now (Cole: "mirror real stock")
   - Priced at the real price; an automatic discount makes them free at $90 / $140,
     so a direct link can't be used to get one without buying (Cole picked this).
   - UNLISTED: buyable, but not in search, collections or recommendations. */
const fs = require('fs');
const LOC = 'gid://shopify/Location/98054963477'; // Ceries OMS, where all stock sits
const HATS = [ // order = order on the page; black/gold first (the hero hat)
  ['Black | Gold Classic', 'HAT-5P-SB-CLSC-BLK-GLD', 73, 'https://cdn.shopify.com/s/files/1/2286/3149/files/10_96db47c0-e327-4f91-b46b-2f1caced97cf.webp'],
  ['White | Gold Classic', 'HAT-5P-SB-CLSC-WHT-GLD', 89, 'https://cdn.shopify.com/s/files/1/2286/3149/files/79.webp'],
  ['Black Patch', 'HAT-5P-SB-IBTBL-BL', 89, 'https://cdn.shopify.com/s/files/1/2286/3149/files/39.webp'],
  ['White Patch', 'HAT-5P-SB-IBTBL-WHT', 84, 'https://cdn.shopify.com/s/files/1/2286/3149/files/89.webp'],
  ['White Cursive', 'HAT-5P-SB-CRSV-WHT', 102, 'https://cdn.shopify.com/s/files/1/2286/3149/files/49.webp'],
  ['Tan Cursive', 'HAT-5P-SB-CRSV-TAN', 83, 'https://cdn.shopify.com/s/files/1/2286/3149/files/1_9c446716-791d-48c1-be9d-9e805bda751a.webp'],
  ['Baby Blue Cursive', 'HAT-5P-SB-CRSV-BBLU-MONO', 119, 'https://cdn.shopify.com/s/files/1/2286/3149/files/30_203d7c7f-8680-4d32-bf41-18d0d4877086.webp'],
  ['Cream Upside Down', 'HAT-5P-SB-UPDN-CRM', 84, 'https://cdn.shopify.com/s/files/1/2286/3149/files/69.webp'],
  ['White Upside Down', 'HAT-5P-SB-UPDN-WHT', 92, 'https://cdn.shopify.com/s/files/1/2286/3149/files/59.webp'],
  ['White/Black Upside Down', 'HAT-5P-SB-UPDN-WHTBLK', 82, 'https://cdn.shopify.com/s/files/1/2286/3149/files/20.webp']
];
const SIZES = ['Small', 'Medium', 'Large', 'XL', 'XXL', '3XL'];
const POLOS = [ // [name, sku stem, stock per size S..3XL, image]
  ['Gold Dust', 'LGA-CP-GoldDust', [5, 22, 19, 5, 0, 0], 'https://cdn.shopify.com/s/files/1/2286/3149/files/PaintSplatter1.webp'],
  ['Signature Black', 'LGA-CP-SignatureBlack', [4, 24, 7, 1, 4, 1], 'https://cdn.shopify.com/s/files/1/2286/3149/files/Classicpolowithlogointhecollar1.webp'],
  ['Shadow', 'LGA-CP-Shadow', [6, 22, 13, 0, 0, 0], 'https://cdn.shopify.com/s/files/1/2286/3149/files/Graycamofour-leafclover1.webp'],
  ['Contour', 'LGA-CP-Contour', [5, 20, 8, 0, 3, 3], 'https://cdn.shopify.com/s/files/1/2286/3149/files/TopographyStyle1.webp'],
  ['Marble', 'LGA-CP-Marble', [6, 27, 20, 0, 0, 0], 'https://cdn.shopify.com/s/files/1/2286/3149/files/GoldMirage1.webp'],
  ['Gold Carnation', 'LGA-CP-GoldCarnation', [5, 17, 20, 3, 0, 2], 'https://cdn.shopify.com/s/files/1/2286/3149/files/WhiteCarnation1.webp'],
  ['Frost', 'LGA-CP-Frost', [7, 21, 15, 4, 4, 3], 'https://cdn.shopify.com/s/files/1/2286/3149/files/Whitecome1.webp'],
  ['Cruiser', 'LGA-CP-Cruiser', [5, 22, 15, 4, 1, 0], 'https://cdn.shopify.com/s/files/1/2286/3149/files/Golfcart1.webp'],
  ['Azalea', 'LGA-CP-Azalea', [3, 16, 6, 0, 0, 0], 'https://cdn.shopify.com/s/files/1/2286/3149/files/Flower1.webp'],
  ['Nightshade', 'LGA-CP-Nightshade', [6, 21, 15, 6, 2, 2], 'https://cdn.shopify.com/s/files/1/2286/3149/files/Blackwhiteflower1.webp'],
  ['Swirl Blade', 'LGA-BP-Swirl', [6, 26, 21, 8, 3, 0], 'https://cdn.shopify.com/s/files/1/2286/3149/files/GoldTwist1.webp'],
  ['Spot Blade', 'LGA-BP-Spot', [6, 19, 18, 8, 3, 1], 'https://cdn.shopify.com/s/files/1/2286/3149/files/FreshMint1.webp'],
  ['Blackout Blade', 'LGA-BP-Blackout', [4, 14, 4, 1, 0, 0], 'https://cdn.shopify.com/s/files/1/2286/3149/files/StrokePlay1.webp']
];
const img = (src, alt) => ({ originalSource: src, contentType: 'IMAGE', alt });
const stock = q => [{ locationId: LOC, name: 'available', quantity: q }];
const common = { vendor: 'Lucky Golf', productType: 'Gift', status: 'UNLISTED', tags: ['gwp-gift', 'hidden'],
  seo: { title: 'Free with your order', description: 'A gift that comes free with a qualifying order.' } };

const hat = { ...common, title: 'Free Hat (Gift)', handle: 'free-hat-gift',
  descriptionHtml: '<p>Free with any order of $90 or more, through Friday, Sept 25.</p>',
  productOptions: [{ name: 'Hat', values: HATS.map(h => ({ name: h[0] })) }],
  files: HATS.map(h => img(h[3], h[0] + ' hat')),
  variants: HATS.map((h, i) => ({ optionValues: [{ optionName: 'Hat', name: h[0] }], price: '29.00', sku: h[1], position: i + 1,
    inventoryPolicy: 'DENY', inventoryItem: { tracked: true, sku: h[1] }, inventoryQuantities: stock(h[2]), file: img(h[3], h[0] + ' hat') })) };

const polo = { ...common, title: 'Free Polo (Gift)', handle: 'free-polo-gift',
  descriptionHtml: '<p>Free with any order of $140 or more, through Friday, Sept 25.</p>',
  productOptions: [{ name: 'Polo', values: POLOS.map(p => ({ name: p[0] })) }, { name: 'Size', values: SIZES.map(s => ({ name: s })) }],
  files: POLOS.map(p => img(p[3], p[0] + ' polo')),
  variants: POLOS.flatMap((p, pi) => SIZES.map((s, si) => ({
    optionValues: [{ optionName: 'Polo', name: p[0] }, { optionName: 'Size', name: s }], price: '67.00', sku: p[1] + '-' + s,
    position: pi * 6 + si + 1, inventoryPolicy: 'DENY', inventoryItem: { tracked: true, sku: p[1] + '-' + s },
    inventoryQuantities: stock(p[2][si]), file: img(p[3], p[0] + ' polo') }))) };

const out = process.argv[2] || 'gift-products.jsonl';
fs.writeFileSync(out, [hat, polo].map(p => JSON.stringify({ input: p })).join('\n') + '\n');
console.log('wrote', out, '·', hat.variants.length, 'hats ·', polo.variants.length, 'polo variants');
