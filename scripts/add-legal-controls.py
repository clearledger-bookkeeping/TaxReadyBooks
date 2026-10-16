from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

LEGAL_LINKS = '''<div class="trb-legal-links" aria-label="Legal and privacy links">
  <a href="/privacy-policy.html">Privacy Policy</a>
  <a href="/terms.html">Terms &amp; Conditions</a>
  <a href="/cookie-policy.html">Cookie Policy</a>
  <a href="/refund-policy.html">Refund Policy</a>
</div>'''

LEGAL_CSS = '''
<style id="trb-legal-controls-css">
.trb-legal-links{display:flex;flex-wrap:wrap;gap:12px 18px;margin-top:18px;font-size:.76rem;color:inherit;opacity:.78}
.trb-legal-links a{text-decoration:none}.trb-legal-links a:hover{text-decoration:underline;text-underline-offset:4px}
.trb-email-consent{display:flex;align-items:flex-start;gap:9px;margin:4px 0 2px;font-size:.78rem;line-height:1.5;color:inherit}
.trb-email-consent input{width:16px!important;height:16px!important;flex:0 0 16px;margin:2px 0 0!important;accent-color:#F2A33A}
.trb-email-consent a{text-decoration:underline;text-underline-offset:3px}
#trb-cookie-banner{position:fixed;left:16px;right:16px;bottom:16px;z-index:9999;display:none;max-width:760px;margin:auto;padding:18px 20px;border:1px solid rgba(255,255,255,.18);border-radius:14px;background:#1B1F3B;color:#FAFAF7;box-shadow:0 18px 55px rgba(0,0,0,.25);font:14px/1.55 Inter,system-ui,sans-serif}
#trb-cookie-banner.show{display:block}.trb-cookie-inner{display:flex;align-items:center;gap:18px;justify-content:space-between}.trb-cookie-copy{max-width:500px}.trb-cookie-copy strong{display:block;margin-bottom:3px}.trb-cookie-copy a{color:#F2A33A}.trb-cookie-actions{display:flex;gap:8px;flex:0 0 auto}.trb-cookie-actions button{border:1px solid rgba(255,255,255,.35);padding:9px 12px;border-radius:7px;background:transparent;color:#FAFAF7;font-weight:700;cursor:pointer}.trb-cookie-actions button:last-child{background:#F2A33A;color:#1B1F3B;border-color:#F2A33A}
@media(max-width:620px){.trb-cookie-inner{display:grid;gap:12px}.trb-cookie-actions{display:grid;grid-template-columns:1fr 1fr}.trb-cookie-actions button{width:100%}}
</style>'''

LEGAL_JS = '''
<script id="trb-legal-controls">
(function(){
  function addConsentToForms(){
    document.querySelectorAll('form').forEach(function(form){
      if(form.dataset.trbEmailConsent==='1') return;
      if(!form.querySelector('input[type="email"]')) return;
      if(/review/i.test(form.id+' '+form.className)) return;
      var wrap=document.createElement('label');
      wrap.className='trb-email-consent';
      wrap.innerHTML='<input type="checkbox" name="emailConsent" value="yes"><span>I agree to receive emails from TaxReady Books about my enquiry, services, referrals, and related updates. I can withdraw marketing consent at any time. See the <a href="/privacy-policy.html">Privacy Policy</a>.</span>';
      var submit=form.querySelector('button[type="submit"],input[type="submit"]');
      if(submit) submit.parentNode.insertBefore(wrap,submit); else form.appendChild(wrap);
      form.dataset.trbEmailConsent='1';
    });
  }
  function cookieBanner(){
    if(document.getElementById('trb-cookie-banner')) return;
    var choice=localStorage.getItem('trbThirdPartyTrackingConsent');
    var b=document.createElement('div');
    b.id='trb-cookie-banner';
    b.innerHTML='<div class="trb-cookie-inner"><div class="trb-cookie-copy"><strong>Privacy choices</strong><span>We keep optional third-party analytics, advertising, and tracking disabled unless you allow them. Essential site storage may still be used. <a href="/cookie-policy.html">Cookie Policy</a></span></div><div class="trb-cookie-actions"><button type="button" data-cookie="decline">Decline</button><button type="button" data-cookie="allow">Allow third-party</button></div></div>';
    document.body.appendChild(b);
    if(!choice) b.classList.add('show');
    b.addEventListener('click',function(e){
      var action=e.target.closest('[data-cookie]'); if(!action) return;
      localStorage.setItem('trbThirdPartyTrackingConsent',action.dataset.cookie==='allow'?'granted':'denied');
      b.classList.remove('show');
      window.dispatchEvent(new CustomEvent('trb:tracking-consent',{detail:{granted:action.dataset.cookie==='allow'}}));
    });
  }
  function init(){addConsentToForms();cookieBanner();}
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',init); else init();
})();
</script>'''

for name in ('index.html','referral.html'):
    p=ROOT/name
    if not p.exists():
        continue
    s=p.read_text(encoding='utf-8')
    if 'trb-legal-controls-css' not in s:
        s=s.replace('</head>',LEGAL_CSS+'\n</head>',1)
    if 'trb-legal-controls' not in s:
        s=s.replace('</body>',LEGAL_JS+'\n</body>',1)
    if 'class="trb-legal-links"' not in s:
        s=s.replace('</footer>',LEGAL_LINKS+'\n</footer>',1)
    p.write_text(s,encoding='utf-8')

print('Legal controls applied.')