/* The five Judge.me pulls, merged by tools/build.py and tagged with the product
   each review is about. Verbatim submissions — HANDOFF forbids invented ones. */
var LG_ALL_REVIEWS = {{REVIEWS_JSON}};

/* Same widget the product pages run (_src/reviews.js). The only difference is
   that this data carries a `products` list, which is what makes the widget
   render its club chips. A page of 177 reviews wants a longer first page than
   a PDP's six. */
(function(){
  LG_REVIEWS.mount(document.getElementById('reviews'), LG_ALL_REVIEWS, {page: 10});
})();
