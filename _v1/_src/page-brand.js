/* page-brand.js — the ambassador application, markup only.
   Same contract as the contact form (§25g): the prototype notice sits ABOVE
   the fields, submit is intercepted, and nobody is thanked for a message that
   never sent — the interception repeats the notice instead. Native `required`
   validation still runs; this fires only on a valid submit. */
(function(){
  var f = document.getElementById('amb-apply');
  if (!f) return;
  function brApplyIntercept(e){
    e.preventDefault();
    var n = document.getElementById('amb-sent');
    if (n){ n.hidden = false; n.focus(); }
  }
  f.addEventListener('submit', brApplyIntercept);
})();
