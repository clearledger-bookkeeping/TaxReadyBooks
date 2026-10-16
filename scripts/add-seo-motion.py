from pathlib import Path

path = Path("index.html")
s = path.read_text(encoding="utf-8")
marker = "/* TRB-SEO-MOTION-V1 */"

if marker in s:
    print("SEO/motion patch already applied.")
    raise SystemExit(0)

if '<meta name="author"' not in s:
    needle = '<meta name="description"'
    start = s.find(needle)
    if start == -1:
        raise SystemExit("Description meta tag not found; refusing to modify index.html.")
    end = s.find(">", start)
    if end == -1:
        raise SystemExit("Malformed description meta tag; refusing to modify index.html.")
    s = s[:end + 1] + '\n  <meta name="author" content="Dipak Kumar Khadka, TaxReady Books">' + s[end + 1:]

css = '''
    /* TRB-SEO-MOTION-V1 */
    .trb-scroll-progress{position:fixed;top:0;left:0;width:100%;height:2px;z-index:1000;pointer-events:none;background:transparent}
    .trb-scroll-progress span{display:block;width:100%;height:100%;background:var(--saffron);transform:scaleX(0);transform-origin:left center}
    .trb-reveal{opacity:0;transform:translate3d(0,28px,0);transition:opacity .72s cubic-bezier(.22,1,.36,1),transform .72s cubic-bezier(.22,1,.36,1);will-change:opacity,transform}
    .trb-reveal.trb-visible{opacity:1;transform:none}
    .trb-reveal[data-trb-delay="1"]{transition-delay:.06s}.trb-reveal[data-trb-delay="2"]{transition-delay:.12s}.trb-reveal[data-trb-delay="3"]{transition-delay:.18s}.trb-reveal[data-trb-delay="4"]{transition-delay:.24s}
    .trb-parallax{transform:translate3d(0,var(--trb-parallax,0px),0);will-change:transform}
    @media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}.trb-reveal{opacity:1!important;transform:none!important;transition:none!important}.trb-parallax{transform:none!important}.trb-scroll-progress{display:none}}
'''

style_end = s.rfind("</style>")
if style_end == -1:
    raise SystemExit("Closing style tag not found; refusing to modify index.html.")
s = s[:style_end] + css + s[style_end:]

js = '''
  <script>
    (() => {
      const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
      const progress = document.createElement('div');
      progress.className = 'trb-scroll-progress';
      progress.innerHTML = '<span></span>';
      document.body.prepend(progress);
      const bar = progress.firstElementChild;

      const groups = [
        '.hero-copy', '.hero-visual', 'section .section-head',
        'section .card', 'section .trust-item', '.services-grid > *',
        '.reviews-grid > *', '.pricing-grid > *'
      ];
      const nodes = [];
      groups.forEach(sel => document.querySelectorAll(sel).forEach(el => {
        if (!nodes.includes(el)) nodes.push(el);
      }));

      nodes.forEach((el, i) => {
        el.classList.add('trb-reveal');
        el.dataset.trbDelay = String((i % 4) + 1);
      });

      if (!reduce && 'IntersectionObserver' in window) {
        const io = new IntersectionObserver(entries => {
          entries.forEach(entry => {
            if (entry.isIntersecting) {
              entry.target.classList.add('trb-visible');
              io.unobserve(entry.target);
            }
          });
        }, {threshold: .12, rootMargin: '0px 0px -8% 0px'});
        nodes.forEach(el => io.observe(el));
      } else {
        nodes.forEach(el => el.classList.add('trb-visible'));
      }

      const hero = document.querySelector('.hero-visual');
      let ticking = false;
      const update = () => {
        const total = Math.max(1, document.documentElement.scrollHeight - window.innerHeight);
        const progressValue = Math.min(1, Math.max(0, window.scrollY / total));
        bar.style.transform = `scaleX(${progressValue})`;
        if (!reduce && hero) {
          const heroProgress = Math.min(1, Math.max(0, window.scrollY / Math.max(1, window.innerHeight)));
          hero.style.setProperty('--trb-parallax', `${heroProgress * 18}px`);
        }
        ticking = false;
      };
      const onScroll = () => {
        if (!ticking) { ticking = true; requestAnimationFrame(update); }
      };
      update();
      window.addEventListener('scroll', onScroll, {passive:true});
      window.addEventListener('resize', update, {passive:true});
    })();
  </script>
'''

body_end = s.rfind("</body>")
if body_end == -1:
    raise SystemExit("Closing body tag not found; refusing to modify index.html.")
s = s[:body_end] + js + s[body_end:]
path.write_text(s, encoding="utf-8")
print("Applied SEO author metadata and scroll-based animation safely.")
