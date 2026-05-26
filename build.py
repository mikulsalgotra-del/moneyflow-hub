import re

with open('original.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. CSS fixes
css_fixes = """
    /* RESPONSIVE LAYOUT OVERRIDES */
    @media (max-width: 768px) {
      .calc-grid { grid-template-columns: 1fr; }
      .page-row { flex-direction: column; }
      nav { padding: 12px 20px; }
      .nav-links { display: none; }
      .hamburger { display: block; }
      section { padding: 60px 20px; }
      .hero { padding: 100px 20px 60px; }
      .calc-result { grid-template-columns: 1fr; }
      .step { grid-template-columns: 1fr; }
      .step-num { font-size: 36px; text-align: left; }
    }

    /* ===== UTILITY CLASSES (replacing broken Tailwind refs) ===== */
    .ad-top-wrapper {
      width: 100%;
      padding: 24px 16px;
      display: flex;
      justify-content: center;
      z-index: 10;
      position: relative;
    }
    .mx-auto { margin-left: auto; margin-right: auto; }
    .w-full { width: 100%; }
    .relative { position: relative; }
    .p-8 { padding: 32px; }
    .results-hidden {
      max-height: 0;
      opacity: 0;
      overflow: hidden;
      transition: max-height 0.5s ease, opacity 0.5s ease;
    }
    .sponsored-label {
      position: absolute;
      top: 8px;
      right: 12px;
      font-size: 8px;
      font-weight: 700;
      color: #475569;
      letter-spacing: 2px;
      text-transform: uppercase;
      font-family: 'Space Mono', monospace;
    }

    /* Responsive grid helpers (replace invalid sm:/md: inline syntax) */
    .grid-responsive-2col {
      display: grid;
      grid-template-columns: 1fr;
      gap: 20px;
    }
    .grid-responsive-converter {
      display: grid;
      grid-template-columns: 1fr;
      gap: 20px;
      align-items: center;
    }
    @media (min-width: 640px) {
      .grid-responsive-2col {
        grid-template-columns: 1fr 1fr;
      }
    }
    @media (min-width: 768px) {
      .grid-responsive-converter {
        grid-template-columns: 9fr 1fr 9fr;
      }
    }
  </style>
"""

content = content.replace("</style>", css_fixes)

# 2. Replace Tailwind classes and inline responsive hacks
content = content.replace('<div class="w-full py-6 px-4 flex justify-center z-10 relative">', '<div class="ad-top-wrapper">')
content = content.replace('<div style="display: grid; grid-template-columns: 1fr sm:grid-template-columns: 1fr 1fr; gap: 20px;">', '<div class="grid-responsive-2col">')
content = content.replace('<div id="crypto-results" class="results-hidden space-y-4"', '<div id="crypto-results" class="results-hidden"')
content = content.replace('<div style="display:grid; grid-template-columns:1fr; md:grid-template-columns:1fr 1fr; gap:16px; margin: 16px 0;">', '<div class="grid-responsive-2col" style="margin: 16px 0;">')
content = content.replace('<div style="display:grid; grid-template-columns: 1fr sm:grid-template-columns: 1fr 1fr; gap:16px; margin-top:16px;">', '<div class="grid-responsive-2col" style="margin-top:16px;">')
content = content.replace('<div style="display: grid; grid-template-columns: 1fr; md:grid-template-columns: 9fr 1fr 9fr; gap: 20px; align-items: center;">', '<div class="grid-responsive-converter">')

content = content.replace('<span class="absolute top-2 right-3 text-[8px] font-bold text-slate-600 tracking-widest uppercase" style="font-family:\'Space Mono\', monospace;">Sponsored Feed</span>', '<span class="sponsored-label">Sponsored Feed</span>')

# 3. Fix smooth scroll
old_scroll = """  // Smooth scroll anchors
  document.querySelectorAll('a[href^="#"]').forEach(a => {
    a.addEventListener('click', e => {
      e.preventDefault();
      document.querySelector(a.getAttribute('href'))?.scrollIntoView({ behavior:'smooth' });
    });
  });"""
new_scroll = """  // Smooth scroll anchors
  document.querySelectorAll('a[href^="#"]').forEach(a => {
    a.addEventListener('click', e => {
      e.preventDefault();
      const targetId = a.getAttribute('href');
      if (targetId === '#') {
        window.scrollTo({ top: 0, behavior: 'smooth' });
        return;
      }
      document.querySelector(targetId)?.scrollIntoView({ behavior:'smooth' });
    });
  });"""
content = content.replace(old_scroll, new_scroll)

# 4. Generate 1000 ads
AD_TYPES = [
    {
        'name': 'Leaderboard (728x90)',
        'key': '8310950c7541eab88b09554be5184029',
        'width': 728,
        'height': 90,
        'isNative': False
    },
    {
        'name': 'Medium Rectangle (300x250)',
        'key': '81038345ce39f3f91c0605f7ae85d8a0',
        'width': 300,
        'height': 250,
        'isNative': False
    },
    {
        'name': 'Skyscraper (160x600)',
        'key': '9bba29ed9c7efae90efaaac92c7c5717',
        'width': 160,
        'height': 600,
        'isNative': False
    },
    {
        'name': 'Mini Skyscraper (160x300)',
        'key': '90ac07fb1231f17fbb50a97371d72495',
        'width': 160,
        'height': 300,
        'isNative': False
    },
    {
        'name': 'Standard Banner (468x60)',
        'key': 'f5cdd8a153dc16903733dd4ee6eb94b0',
        'width': 468,
        'height': 60,
        'isNative': False
    },
    {
        'name': 'Native Banner Widget',
        'key': '2c63d1892f0f4cdfa097843b6668d8af',
        'width': '100%',
        'height': 220,
        'isNative': True
    }
]

html_slots = []
for i in range(1, 1001):
    ad_type = AD_TYPES[i % len(AD_TYPES)]
    
    if ad_type['isNative']:
        srcdoc = f"<!DOCTYPE html><html><head><style>body {{ margin: 0; background: transparent; }}</style></head><body><script async='async' data-cfasync='false' src='https://pl29559837.effectivecpmnetwork.com/2c63d1892f0f4cdfa097843b6668d8af/invoke.js'></script><div id='container-2c63d1892f0f4cdfa097843b6668d8af'></div></body></html>"
    else:
        srcdoc = f"<!DOCTYPE html><html><head><style>body {{ margin: 0; background: transparent; display: flex; justify-content: center; align-items: center; height: 100vh; }}</style></head><body><script>atOptions = {{ 'key' : '{ad_type['key']}', 'format' : 'iframe', 'height' : {ad_type['height']}, 'width' : {ad_type['width']}, 'params' : {{}} }};</script><script src='https://www.highperformanceformat.com/{ad_type['key']}/invoke.js'></script></body></html>"
    
    w = ad_type['width'] if not ad_type['isNative'] else "100%"
    w_px = f"{w}px" if isinstance(w, int) else w
    h = ad_type['height']
    
    html_slots.append(f"""    <div class="yield-card" style="background: var(--dark3); border: 1px solid var(--border); border-radius: 8px; padding: 12px; display: flex; flex-direction: column; align-items: center; gap: 8px; min-width: 160px;">
      <span style="font-family:'Space Mono', monospace; font-size:8.5px; color:var(--gold); font-weight:700; text-align:center;">Slot #{i} [{ad_type['name'].split(' (')[0]}]</span>
      <div style="width: 100%; height: {h}px; overflow: hidden; display: flex; justify-content: center; align-items: center; background: rgba(0,0,0,0.2); border-radius: 4px;">
        <iframe srcdoc="{srcdoc.replace('"', '&#39;')}" style="width: {w_px}; height: {h}px; border: none; overflow: hidden; background: transparent;" loading="lazy" scrolling="no"></iframe>
      </div>
    </div>""")

massive_yield_mine = f"""
<!-- ===================== [AD_MASSIVE_1000_GRID] MASSIVE MONETIZATION ZONE ===================== -->
<section id="massive-ad-grid" style="padding: 60px 40px; background: var(--dark2); border-top: 1px solid var(--border);">
  <div class="fade-in" style="text-align: center; margin-bottom: 40px;">
    <div class="section-tag">Massive Yield Mine</div>
    <h2 class="section-title">1,000 Live<br>Ad Slots</h2>
    <p class="section-desc">Arranged in a high-density, automated responsive grid. Duplicated systematically up to 1,000 active nodes utilizing isolated iframe sandboxes and native lazy loading to maintain 60 FPS performance and avoid browser render overhead.</p>
  </div>
  <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(180px, 1fr)); gap: 15px; padding: 20px; border-radius: 16px; border: 1px solid var(--border); background: var(--dark);">
{chr(10).join(html_slots)}
  </div>
</section>
"""

# Insert before <footer>
content = content.replace("<footer>", massive_yield_mine + "<footer>")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Build complete.")
