# Blog articles: dry run (nothing sent to Shopify)

Blog `news` (All Things Lucky): 14 live articles, 14 rewritten files.
Built by `tools/theme/publish_articles.py` from `v9/migration/live-articles.json`.

| File (= live handle) | Live article | Published | Title now -> new | Hero image now -> new | Body words now -> new |
|---|---|---|---|---|---|
| `are-your-wedges-forged` | 605107912981 | yes | Are Your Wedges Forged? -> Are your wedges forged? | Lucky_Golf_Foreged_Wedges_Factory_Pic.png -> lg-art-forged-factory.webp | 508 -> 447 |
| `future-videos` | 14450589767 | yes | Future Videos -> Future videos | 40-17008-R56-CA2-M01-Bag_Shot_1_56_GOLD.85-CR-WB.png -> lg-walk-off-green.webp | 13 -> 219 |
| `golf-com-proves-why-a-lucky-charm-is-necessary-on-the-golf-course` | 603193770055 | yes | Golf.com Proves Why a "Lucky" Charm Is Necessary on the Golf Course -> Golf.com proves why a lucky charm is necessary on the golf course | Screen_Shot_2021-06-16_at_11.11.45_AM.png -> lg-from-the-cup.webp | 58 -> 385 |
| `golf-is-a-mental-game` | 605083402517 | yes | Golf is a Mental Game -> Golf is a mental game | FDC0DC59-178B-47F1-8306-CC92CFAAAD67.jpg -> lg-art-mental-game.webp | 435 -> 514 |
| `how-to-improve-your-golf-game-according-to-the-pros` | 605160145173 | yes | How to Improve Your Golf Game According to the Pros -> How to improve your golf game according to the pros | scorecard.jpg -> lg-art-scorecard.webp | 384 -> 473 |
| `mastering-your-putt-the-power-of-a-well-crafted-putting-routine` | 605356556565 | no (draft, stays a draft) | Mastering Your Putt: The Power of a Well-Crafted Putting Routine -> Mastering your putt: the power of a well-crafted putting routine | none -> lg-putt-sunset.webp | 608 -> 505 |
| `mrshortgame-golf-reviews-lucky-wedges` | 34666872903 | yes | MrShortGame Golf Reviews Lucky Wedges! -> MrShortGame Golf reviews Lucky wedges | Screen_Shot_2019-10-07_at_10.45.07_PM.png -> lg-art-mrshortgame.webp | 34 -> 231 |
| `the-dreaded-chili-dip-golf-shot` | 28364832839 | yes | The Dreaded Chili Dip Golf Shot -> The dreaded chili dip golf shot | Chili-Dip-Golf.jpg -> lg-art-chili-dip.webp | 435 -> 526 |
| `the-top-10-golf-shots-you-can-hit-using-a-wedge` | 605122560277 | yes | The Top 10 Golf Shots You Can Hit Using a Wedge -> The top 10 golf shots you can hit using a wedge | daniel-berger.jpg -> lg-swing-black-wedge.webp | 679 -> 522 |
| `use-your-lucky-wedge-to-get-out-of-a-deep-bunker-lie` | 30067753031 | yes | Use Your Lucky Wedge to Get Out of a Deep Bunker Lie -> Use your Lucky wedge to get out of a deep bunker lie | none -> lg-gold-wedge-bag.webp | 63 -> 403 |
| `using-your-lucky-wedge-from-the-rough` | 28401107015 | yes | Using Your Lucky Wedge from the Rough -> Using your Lucky wedge from the rough | Colin_McCarthy.jpg -> lg-art-rough-tip.webp | 182 -> 439 |
| `welcome-to-lucky` | 28364734535 | yes | Welcome to Lucky -> Welcome to Lucky | Gold_With_Lucky_Ball.PNG -> lg-art-welcome.webp | 218 -> 352 |
| `why-golf-wedges-are-the-most-important-club-in-your-bag` | 604352774421 | yes | Why Golf Wedges are the Most Important Club in Your Bag. -> Why golf wedges are the most important club in your bag | IMG_3920.jpg -> lg-art-most-important.webp | 931 -> 492 |
| `why-we-have-the-best-golf-wedges-for-under-100` | 592321544263 | yes | Why We Have The Best Golf Wedges For Under $100 -> Why we have the best golf wedges for under $100 | Screen_Shot_2021-03-23_at_9.35.47_PM.png -> lg-art-under-100.webp | 21 -> 308 |

Nothing else on the store changes. The theme's article template reads the lucky.* metafields and
falls back to the article title (and skips the lede and sign-off it lacks), so the live articles render fine before and after.

## Per article

### are-your-wedges-forged

- Summary now: when it comes to selecting the best wedge for your game, you will be faced with a choice b...
- Summary new: Forged or cast: the choice most golfers never get explained, and why it changes the feel and the price.
- Meta description now: (none, Shopify falls back to the body); new: the summary above
- Heading on the page: Are your wedges forged ? (gold word from lucky.h1)
- Body now starts: As a golf enthusiast, you are likely aware of the importance of having the right set of cl...
- Body new starts: Casting is the quick way, and there's nothing sinister about it. Molten steel goes into a ...
- Quick answers added: 3; sign-off: Forged, not cast / See the Carver -> /products/lucky-golf-lgw02-gold
- Unchanged: handle, URL, publish date, published state, tags, template, author, comments.
### future-videos

- Summary now: (empty)
- Summary new: Trick shots and hole-outs you'll never repeat. Here's where to send them.
- Meta description now: (none, Shopify falls back to the body); new: the summary above
- Heading on the page: Future videos (gold word from lucky.h1)
- Body now starts: We will post user submitted trick shots in this area in the future
- Body new starts: Some of the best golf ever hit never makes it past a group chat. The flop over a bunker th...
- Quick answers added: 3; sign-off: Show us the shot / See the Community -> /pages/community
- Unchanged: handle, URL, publish date, published state, tags, template, author, comments.
### golf-com-proves-why-a-lucky-charm-is-necessary-on-the-golf-course

- Summary now: (empty)
- Summary new: People told their golf ball was lucky holed more putts. Golf.com wrote up the study, and we've been saying it since 2018.
- Meta description now: (none, Shopify falls back to the body); new: the summary above
- Heading on the page: Golf.com proves why a lucky charm is necessary on the golf course (gold word from lucky.h1)
- Body now starts: In this recent article on Golf.com they explain why it's important to have a "Lucky" charm...
- Body new starts: In June 2021, Golf.com's Luke Kerr-Dineen wrote about a study golfers are going to like. L...
- Quick answers added: 3; sign-off: Bring your own luck / See the clubs -> /collections/lucky-golf-clubs
- Unchanged: handle, URL, publish date, published state, tags, template, author, comments.
### golf-is-a-mental-game

- Summary now: Welcome to the world of golf, a sport that is much more than just hitting a ball into a ho...
- Summary new: Focus, patience and letting the bad ones go. The part of the game you can't buy your way out of.
- Meta description now: (none, Shopify falls back to the body); new: the summary above
- Heading on the page: Golf is a mental game (gold word from lucky.h1)
- Body now starts: Welcome to the world of golf, a sport that is much more than just hitting a ball into a ho...
- Body new starts: Let's get it out of the way: golf is frustrating. You'll hit a shot you'd happily frame, t...
- Quick answers added: 3; sign-off: It's better to be lucky / See the clubs -> /collections/lucky-golf-clubs
- Unchanged: handle, URL, publish date, published state, tags, template, author, comments.
### how-to-improve-your-golf-game-according-to-the-pros

- Summary now: Golf is a challenging game, but it's also one of the most rewarding. With a little practic...
- Summary new: Borrow the habits, not the swing. What the people who play for a living actually do, scaled down for a Saturday golfer.
- Meta description now: (none, Shopify falls back to the body); new: the summary above
- Heading on the page: How to improve your golf game according to the pros (gold word from lucky.h1)
- Body now starts: How to Improve Your Golf Game Golf is a challenging game, but it's also one of the most re...
- Body new starts: Pick a number "Get better" isn't a goal. Breaking 100 is. So is breaking 90 by the end of ...
- Quick answers added: 3; sign-off: Practice gets you lucky / See the Carver -> /products/lucky-golf-lgw02-gold
- Unchanged: handle, URL, publish date, published state, tags, template, author, comments.
### mastering-your-putt-the-power-of-a-well-crafted-putting-routine

- Summary now: (empty)
- Summary new: Read it, pick a spot, feel the speed, go. A putting routine that holds up when the putt matters.
- Meta description now: (none, Shopify falls back to the body); new: the summary above
- Heading on the page: Mastering your putt: the power of a well-crafted putting routine (gold word from lucky.h1)
- Body now starts: Introduction: When it comes to golf, the importance of a strong putting game cannot be ove...
- Body new starts: Putting looks like the simple part. No swing speed, no carry, just a ball and a hole. That...
- Quick answers added: 3; sign-off: Roll it pure / See the putters -> /collections/lucky-golf-clubs#putters
- Unchanged: handle, URL, publish date, published state, tags, template, author, comments.
### mrshortgame-golf-reviews-lucky-wedges

- Summary now: (empty)
- Summary new: A wedge reviewer put our gold 60° on camera next to one of the big names.
- Meta description now: (none, Shopify falls back to the body); new: the summary above
- Heading on the page: MrShortGame Golf reviews Lucky wedges (gold word from lucky.h1)
- Body now starts: MrShortGame Golf or Matt Fisher reviewed our Gold 60 degree Lucky Wedge and did a side by ...
- Body new starts: It's one thing for us to tell you our wedge is good. It's another when somebody who review...
- Quick answers added: 3; sign-off: Run your own test / See the Carver -> /products/lucky-golf-lgw02-gold
- Unchanged: handle, URL, publish date, published state, tags, template, author, comments.
### the-dreaded-chili-dip-golf-shot

- Summary now: (empty)
- Summary new: Everybody's hit one. Here's why it happens, and the drill that stops it.
- Meta description now: (none, Shopify falls back to the body); new: the summary above
- Heading on the page: The dreaded chili dip (gold word from lucky.h1)
- Body now starts: The Dreaded Chili Dip Golf Shot It's every golfers greatest fear. you're lying 10 yards of...
- Body new starts: You smoked the drive and came up a touch short with the approach. Now it's a tight lie, te...
- Quick answers added: 3; sign-off: Chip it like you mean it / See the Carver -> /products/lucky-golf-lgw02-gold
- Unchanged: handle, URL, publish date, published state, tags, template, author, comments.
### the-top-10-golf-shots-you-can-hit-using-a-wedge

- Summary now: If you want to take your golf game to the next level, it's time to start mastering the art...
- Summary new: Ten shots, from the fairway to the bottom of a bunker, and how to hit every one of them.
- Meta description now: (none, Shopify falls back to the body); new: the summary above
- Heading on the page: The top 10 golf shots you can hit using a wedge (gold word from lucky.h1)
- Body now starts: If you want to take your golf game to the next level, it's time to start mastering the art...
- Body new starts: From the fairway The full wedge. It's your stock shot from inside a full swing. Ball in th...
- Quick answers added: 3; sign-off: Ten shots, one wedge at a time / See the Carver -> /products/lucky-golf-lgw02-gold
- Unchanged: handle, URL, publish date, published state, tags, template, author, comments.
### use-your-lucky-wedge-to-get-out-of-a-deep-bunker-lie

- Summary now: (empty)
- Summary new: Plugged in the sand with half the ball showing. A PGA pro shows how to get it out anyway.
- Meta description now: (none, Shopify falls back to the body); new: the summary above
- Heading on the page: Use your Lucky wedge to get out of a deep bunker lie (gold word from lucky.h1)
- Body now starts: In this video, Colin McCarthy PGA Pro shows you how to get a buried ball out of a bunker u...
- Body new starts: A normal bunker shot has one rule: open the face and splash the sand out. A buried lie fli...
- Quick answers added: 3; sign-off: Out in one / See the Carver -> /products/lucky-golf-lgw02-gold
- Unchanged: handle, URL, publish date, published state, tags, template, author, comments.
### using-your-lucky-wedge-from-the-rough

- Summary now: Lucky Wedges are designed with extra weight and balance to help carry momentum through chi...
- Summary new: How to get through thick grass without the chili dip, with a simple trick from a PGA pro.
- Meta description now: (none, Shopify falls back to the body); new: the summary above
- Heading on the page: Using your Lucky wedge from the rough (gold word from lucky.h1)
- Body now starts: Hitting any shot from the rough is less desirable than being in the fairway, that's obviou...
- Body new starts: Nobody wants to be in the rough, and chipping out of it is where a lot of rounds get away....
- Quick answers added: 3; sign-off: Rough lies, handled / See the Carver -> /products/lucky-golf-lgw02-gold
- Unchanged: handle, URL, publish date, published state, tags, template, author, comments.
### welcome-to-lucky

- Summary now: Welcome to Lucky Wedges
- Summary new: A gold wedge, two complaints about golf, and what this blog is for.
- Meta description now: (none, Shopify falls back to the body); new: the summary above
- Heading on the page: Welcome to Lucky (gold word from lucky.h1)
- Body now starts: As a newly launched company Lucky Wedges is starting to make a name for itself in the gian...
- Body new starts: The first complaint was how golf looked. Walk down any range and every bag's full of the s...
- Quick answers added: 3; sign-off: Start with the wedge / See the Carver -> /products/lucky-golf-lgw02-gold
- Unchanged: handle, URL, publish date, published state, tags, template, author, comments.
### why-golf-wedges-are-the-most-important-club-in-your-bag

- Summary now: (empty)
- Summary new: The driver gets the attention. The wedges decide the score, and here's how to build a set that covers every yard.
- Meta description now: (none, Shopify falls back to the body); new: the summary above
- Heading on the page: Why golf wedges are the most important club in your bag (gold word from lucky.h1)
- Body now starts: Golf is a game of precision and accuracy. It’s fair to say that it’s not your average roun...
- Body new starts: Count your next round honestly. You'll swing the driver maybe fourteen times. Everything f...
- Quick answers added: 3; sign-off: Start with the wedges / See the Carver -> /products/lucky-golf-lgw02-gold
- Unchanged: handle, URL, publish date, published state, tags, template, author, comments.
### why-we-have-the-best-golf-wedges-for-under-100

- Summary now: (empty)
- Summary new: A forged wedge for $99 sounds like a catch. Here's what's behind the price, and a reviewer who went looking.
- Meta description now: (none, Shopify falls back to the body); new: the summary above
- Heading on the page: Why we have the best golf wedges for under $100 (gold word from lucky.h1)
- Body now starts: Watch the Art of Simple Golf break down exactly why Lucky Wedges will get you best value i...
- Body new starts: Big-name wedges keep creeping up in price, and it's fair to wonder what a $99 wedge is lea...
- Quick answers added: 3; sign-off: No catch, just spin / See the Carver -> /products/lucky-golf-lgw02-gold
- Unchanged: handle, URL, publish date, published state, tags, template, author, comments.
