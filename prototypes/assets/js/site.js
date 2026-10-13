// Mobile menu toggle
(function(){
  var btn=document.querySelector('.menu-btn'), nav=document.querySelector('[data-nav]');
  if(!btn||!nav) return;
  btn.addEventListener('click',function(){
    var open=nav.classList.toggle('open'); btn.setAttribute('aria-expanded',open);
  });
  nav.addEventListener('click',function(e){ if(e.target.closest('a')){nav.classList.remove('open');btn.setAttribute('aria-expanded',false);} });
})();
// Join form: static site, so compose an email. Replace with a form service (Buttondown, Formspree, etc.) later.
(function(){
  document.querySelectorAll('.join-form').forEach(function(f){
    f.addEventListener('submit',function(e){
      e.preventDefault();
      var d=new FormData(f), body='Name: '+d.get('name')+'\nEmail: '+d.get('email')+'\nPostal code: '+d.get('zip')+'\n';
      location.href='mailto:tom@tougholdmen.com?subject='+encodeURIComponent('Join Tough Old Men')+'&body='+encodeURIComponent(body);
    });
  });
})();
// Shop filter chips (only on pages that have them)
(function(){
  var chips=document.querySelectorAll('[data-filter]'), items=document.querySelectorAll('[data-cat]');
  chips.forEach(function(c){c.addEventListener('click',function(){
    chips.forEach(function(x){x.setAttribute('aria-pressed',x===c)});
    var f=c.dataset.filter; items.forEach(function(i){i.hidden=!(f==='all'||i.dataset.cat===f)});
  })});
})();
