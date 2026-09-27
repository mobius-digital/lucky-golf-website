# Open orders check (pulled from Shopify 2026-09-27)

About 100 orders show as Unfulfilled or Partially fulfilled. Shopify holds stock for every
open line, so these also make "available" stock look lower than it is.
Don't archive them: archiving hides the order but leaves it open and the stock held.

**Done:** #36199 (TEST / DO-NOT-SHIP, $0 Whatnot demo) archived.

## A. Dec 2025 to Jan 2026: 26 orders (ShipBob era). Almost certainly shipped, never marked

#32194 #32195 #32197 #32199 #32201 #32207 #32209 #32210 #32218 #32222 #32231 #32232 #32234
#32235 #32241 #32833 #33008 #33009 #33054 #33060 #33067 #33075 #33095 #33119 #33120 #33268

Open items: old putter SKUs (CPB1 / CPM1), the hybrid (63019), wedges (93011 / 93014).
**Fix:** once the 3PL (or the Gorgias inbox) confirms nobody is waiting, mark fulfilled
WITHOUT notifying the customer. Claude can do all 26 in one go on Cole's yes.

## B. June 20 to Sept 20: about 60 orders with 1 or 2 lines still open. Check each

**B1. Clubs, possibly real backorders (customers may be waiting):**
- LGW02 56 / 60 right-hand (the sold-out S grind, back next month): #34898 #34953 #35513 #35797
  #35934 (52) #35975 #35979 #35986 #35988 #35989
- LGW01 left-hand 54 / 58 / 60: #35207 #35609 #35653 #35856 #36096 #36148 #36193 #36279
- LGW01 / black wedges right-hand: #35411 #35505 #35534 #35600 #35628
- Putter / hybrid: #35568 (Mallet LH + cover + polo) #36076 (Stryker)
**Fix:** ship when stock lands, or email the customer with a date. Don't mark these fulfilled.

**B2. Polos in big sizes (XL, XXL, 3XL), maybe out of stock:**
#34956 #35945 #35970 #36010 #36058 #36184 #36239
**Fix:** ship, or refund that line and tell the customer.

**B3. Small add-ons (probably gifts or extras that were never sent, or sent and not marked):**
- Blade covers: #34905 #34907 #34933 #34936
- Hats: #35284 #35285 #35298 #35304
- Gloves: #35307 #35423 #35503 #35534 #35565 #35691 #36112 #36139 #36179
- Grips: #35430 #35474 #35488 #36197; stock putter grips: #35745 #35836 #35878 #35919
- Tees: #35446 #35488 #35562 #35599 #35700
**Fix:** if they went out, mark fulfilled (no email). If not, ship them or refund the line.

## C. Sept 21 onward: normal orders in progress. Leave them.
