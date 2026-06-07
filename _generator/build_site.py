#!/usr/bin/env python3
# Packed Agency — full static site generator (all 3 sitemap phases)
import os, re, json, datetime

OUT = "/sessions/vibrant-zealous-sagan/mnt/Genesislink/packed-website"
os.makedirs(OUT, exist_ok=True)

PHONE = "343-558-5062"
TEL = "tel:+13435585062"
EMAIL = "info@packedagency.ca"
BASE = "https://packedagency.ca/"

CSS = """
:root{--navy:#131A24;--navy-d:#0D1219;--orange:#F97316;--orange-d:#FB8A3C;--paper:#0A0E14;--ink:#EAEEF5;--grey:#9AA4B4;--line:rgba(255,255,255,.09);--surface:#0F141C;--card:#151C27}
*{margin:0;padding:0;box-sizing:border-box}html{scroll-behavior:smooth}
body{font-family:'Inter',system-ui,sans-serif;color:var(--ink);background:var(--paper);line-height:1.6}
h1,h2,h3{font-family:'Archivo',sans-serif;line-height:1.1;letter-spacing:-.5px}
img,video{max-width:100%;display:block}a{color:inherit;text-decoration:none}
:focus-visible{outline:2px solid var(--orange);outline-offset:2px}
.wrap{max-width:1160px;margin:0 auto;padding:0 24px}
.btn{display:inline-block;background:var(--orange);color:#190B01;font-weight:700;font-family:'Archivo',sans-serif;padding:16px 30px;border-radius:8px;font-size:16px;transition:.18s;border:none;cursor:pointer}
.btn:hover{background:var(--orange-d);transform:translateY(-2px)}
.btn.ghost{background:transparent;border:1px solid rgba(255,255,255,.28);color:#fff}
.btn.ghost:hover{border-color:#fff;background:rgba(255,255,255,.07)}
.btn.navy{background:#1E2A3D;color:#fff}.btn.navy:hover{background:#27364E}
.kicker{font-family:'Archivo',sans-serif;font-weight:700;letter-spacing:.26em;font-size:11.5px;color:var(--orange);text-transform:uppercase;margin-bottom:14px}
section{padding:84px 0}
.sec-h2{font-size:clamp(28px,4vw,42px);font-weight:900;margin-bottom:14px;color:#fff}
.sec-sub{color:var(--grey);font-size:18px;max-width:640px}
header.top{position:sticky;top:0;z-index:50;background:rgba(10,14,20,.88);backdrop-filter:blur(12px);border-bottom:1px solid var(--line)}
.nav{display:flex;align-items:center;justify-content:space-between;height:72px}
.logo{display:flex;align-items:center;gap:11px;font-family:'Archivo',sans-serif}
.logo svg{width:36px;height:36px}.logo b{font-weight:900;font-size:20px;letter-spacing:-.5px;color:#fff}
.logo span{display:block;font-size:9px;letter-spacing:.42em;color:var(--orange);font-weight:700}
.nav-links{display:flex;gap:24px;align-items:center;font-weight:500;font-size:14.5px;color:#C2CAD6}
.nav-links a:hover{color:#fff}.nav-links a.on{color:var(--orange)}
.nav-phone{font-weight:700;color:#fff}.nav .btn{padding:10px 18px;font-size:14px}
.burger{display:none;background:none;border:none;font-size:26px;cursor:pointer;color:#fff}
.phero{background:var(--navy-d);color:#fff;padding:90px 0 76px;position:relative;overflow:hidden}
.phero .bgfx{position:absolute;inset:0;background:radial-gradient(900px 500px at 85% -10%,rgba(249,115,22,.13),transparent 60%),repeating-linear-gradient(0deg,transparent 0 79px,rgba(255,255,255,.03) 79px 80px),repeating-linear-gradient(90deg,transparent 0 79px,rgba(255,255,255,.03) 79px 80px)}
.phero .wrap{position:relative;z-index:2}
.phero h1{font-size:clamp(34px,5vw,58px);font-weight:900;letter-spacing:-1.5px;max-width:840px;color:#fff}
.phero h1 em{font-style:italic;color:var(--orange)}
.phero p.lead{font-size:18.5px;color:#A6AFBE;max-width:620px;margin:18px 0 30px}
.crumb{font-size:13px;color:#7C8698;margin-bottom:18px}.crumb a:hover{color:var(--orange)}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:24px}.grid3{display:grid;grid-template-columns:repeat(3,1fr);gap:22px}.grid4{display:grid;grid-template-columns:repeat(4,1fr);gap:18px}
.card{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:28px;transition:.18s}
.card:hover{border-color:rgba(249,115,22,.55);transform:translateY(-2px);box-shadow:0 16px 34px rgba(0,0,0,.45)}
.card h3{font-size:19px;margin-bottom:8px;color:#fff}.card p{color:var(--grey);font-size:15px}
.card .tag{font-size:12px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:var(--orange)}
.card .from{font-weight:800;font-family:'Archivo',sans-serif;margin-top:14px;color:#fff}.card .from small{color:var(--grey);font-weight:500}
.card.dark{background:#1C140A;border-color:rgba(249,115,22,.4)}.card.dark p{color:#C9B299}
.badge{display:inline-block;background:var(--orange);color:#190B01;font-size:11px;font-weight:800;letter-spacing:.1em;padding:4px 10px;border-radius:6px;margin-bottom:10px}
table.cb{width:100%;border-collapse:collapse;margin:26px 0;background:var(--surface);border-radius:12px;overflow:hidden;border:1px solid var(--line)}
table.cb th{background:#1B2435;color:#fff;text-align:left;padding:14px 18px;font-family:'Archivo',sans-serif;font-size:15px}
table.cb td{padding:14px 18px;border-top:1px solid var(--line);font-size:15px;vertical-align:top}
table.cb tr td:first-child{color:var(--grey)}table.cb tr td:last-child{font-weight:600;color:#E5EAF2}
.stat-strip{background:var(--surface);border:1px solid var(--line);color:#fff;border-radius:14px;padding:36px;display:grid;grid-template-columns:repeat(3,1fr);gap:26px;margin:40px 0;text-align:center}
.stat-strip b{display:block;font-family:'Archivo',sans-serif;font-size:34px;color:var(--orange)}
.stat-strip span{font-size:14px;color:var(--grey)}
.ctaband{background:var(--navy-d);border-top:1px solid var(--line);color:#fff;text-align:center;padding:70px 0}
.ctaband h2{font-size:clamp(26px,3.6vw,38px);font-weight:900;margin-bottom:12px}
.ctaband p{color:#A6AFBE;margin-bottom:26px;font-size:17px}
details{border-bottom:1px solid var(--line);padding:20px 0}
summary{font-family:'Archivo',sans-serif;font-weight:700;font-size:17.5px;cursor:pointer;list-style:none;display:flex;justify-content:space-between;align-items:center;color:#fff}
summary::after{content:"+";color:var(--orange);font-size:26px;font-weight:400;transition:.2s}
details[open] summary::after{transform:rotate(45deg)}
details p{margin-top:12px;color:var(--grey);font-size:15.5px;max-width:700px}
.checks{list-style:none;margin:20px 0}
.checks li{padding:9px 0 9px 32px;position:relative;font-size:15.5px}
.checks li::before{content:"";position:absolute;left:0;top:14px;width:16px;height:16px;border-radius:4px;background:var(--orange)}
.checks.lt li{color:#C9D2E3}
.aform{background:var(--card);border-radius:14px;padding:36px;color:var(--ink);border:1px solid var(--line)}
.aform h3{font-size:22px;margin-bottom:6px;color:#fff}.aform .sub{font-size:14px;color:var(--grey);margin-bottom:22px}
.aform label{display:block;font-size:13px;font-weight:700;margin:14px 0 6px}
.aform input,.aform select{width:100%;padding:13px 14px;border:1px solid rgba(255,255,255,.14);border-radius:8px;font-size:15px;font-family:inherit;background:#0A0E14;color:var(--ink)}
.aform input:focus,.aform select:focus{outline:none;border-color:var(--orange)}
.aform .btn{width:100%;margin-top:22px}
.aform .fine{font-size:12.5px;color:var(--grey);margin-top:12px;line-height:1.5}
.price-card{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:34px;position:relative}
.price-card.hot{border-color:var(--orange);box-shadow:0 18px 44px rgba(249,115,22,.13)}
.price-card .pin{position:absolute;top:-13px;left:30px;background:var(--orange);color:#190B01;font-size:11px;font-weight:800;letter-spacing:.1em;padding:5px 12px;border-radius:6px}
.price-card .amt{font-family:'Archivo',sans-serif;font-weight:900;font-size:34px;margin:8px 0 2px;color:#fff}
.price-card .per{color:var(--grey);font-size:14px;margin-bottom:16px}
footer.site{background:#070A0F;color:#8B95A5;padding:60px 0 30px;border-top:1px solid var(--line)}
.f-grid{display:grid;grid-template-columns:2fr 1fr 1fr 1fr;gap:40px;margin-bottom:44px}
.f-grid h4{color:#fff;font-size:14px;letter-spacing:.12em;text-transform:uppercase;margin-bottom:16px;font-family:'Archivo',sans-serif}
.f-grid a{display:block;padding:5px 0;font-size:14.5px}.f-grid a:hover{color:var(--orange)}
.f-bottom{border-top:1px solid var(--line);padding-top:24px;font-size:13px;display:flex;justify-content:space-between;flex-wrap:wrap;gap:10px}
.callbar{display:none;position:fixed;bottom:0;left:0;right:0;z-index:60;background:var(--orange);color:#190B01;text-align:center;padding:15px;font-weight:800;font-family:'Archivo',sans-serif;font-size:17px}
.calc{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:36px;max-width:560px}
.calc label{display:block;font-size:13.5px;font-weight:700;margin:16px 0 6px}
.calc input{width:100%;padding:13px;border:1px solid rgba(255,255,255,.14);border-radius:8px;font-size:16px;background:#0A0E14;color:var(--ink)}
.calc .result{margin-top:26px;background:#1B2435;color:#fff;border-radius:12px;padding:26px;text-align:center}
.calc .result b{display:block;font-family:'Archivo',sans-serif;font-size:40px;color:var(--orange)}
.calc .result span{font-size:14px;color:#B9C4D8}
.prose{max-width:760px}
.prose h2{font-size:26px;margin:36px 0 12px;color:#fff}
.prose p{margin-bottom:16px;font-size:16.5px;color:#C3CCDA}
.prose ul{margin:0 0 16px 22px;color:#C3CCDA}
.note{background:#221A07;border:1px solid #4A3A12;border-radius:10px;padding:16px 20px;font-size:14px;color:#E6C77F;margin:24px 0}
.statbar{display:grid;grid-template-columns:repeat(3,1fr);border-bottom:1px solid var(--line);background:var(--paper)}
.statbar div{padding:20px 28px;border-right:1px solid var(--line)}
.statbar div:last-child{border-right:none}
.statbar b{display:block;font-family:'Archivo',sans-serif;font-weight:900;font-size:25px;color:#fff}
.statbar b.o{color:var(--orange)}
.statbar span{font-size:13px;color:var(--grey)}
.marq{overflow:hidden;background:var(--orange);padding:11px 0;white-space:nowrap}
.marq span{display:inline-block;font-family:'Archivo',sans-serif;font-weight:900;font-size:12.5px;color:#190B01;letter-spacing:.18em;animation:marq 36s linear infinite;padding-right:0}
@keyframes marq{from{transform:translateX(0)}to{transform:translateX(-50%)}}
@media(prefers-reduced-motion:reduce){.marq span{animation:none}html{scroll-behavior:auto}}
@media(max-width:920px){.grid2,.grid3,.f-grid{grid-template-columns:1fr 1fr}.grid4{grid-template-columns:1fr 1fr}.stat-strip{grid-template-columns:1fr}.statbar{grid-template-columns:1fr}.statbar div{border-right:none;border-bottom:1px solid var(--line)}.nav-links{display:none}.burger{display:block}.nav-links.open{display:flex;position:absolute;top:72px;left:0;right:0;background:#0A0E14;flex-direction:column;padding:24px;gap:18px;border-bottom:1px solid var(--line);z-index:49}}
@media(max-width:600px){.grid2,.grid3,.grid4,.f-grid{grid-template-columns:1fr}section{padding:60px 0}.callbar{display:block}body{padding-bottom:54px}}
"""

LOGO_SVG = """<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"><rect x="8" y="14" width="84" height="78" rx="16" fill="#F97316"/><rect x="22" y="6" width="8" height="16" rx="3" fill="#F97316"/><rect x="70" y="6" width="8" height="16" rx="3" fill="#F97316"/><g fill="#190B01"><rect x="20" y="32" width="16" height="16" rx="3"/><rect x="42" y="32" width="16" height="16" rx="3"/><rect x="64" y="32" width="16" height="16" rx="3"/><rect x="20" y="54" width="16" height="16" rx="3"/><rect x="64" y="54" width="16" height="16" rx="3"/><rect x="20" y="76" width="16" height="10" rx="3"/><rect x="42" y="76" width="16" height="10" rx="3"/><rect x="64" y="76" width="16" height="10" rx="3"/></g><rect x="42" y="54" width="16" height="16" rx="3" fill="#FFE3CC"/></svg>"""

def head(title, desc, fname=""):
    url = BASE + ("" if fname == "index.html" else fname)
    return ("<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n<meta charset=\"UTF-8\">\n"
        '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
        "<title>" + title + "</title>\n<meta name=\"description\" content=\"" + desc + "\">\n"
        '<link rel="canonical" href="' + url + '">\n'
        '<meta property="og:type" content="website">\n'
        '<meta property="og:site_name" content="Packed Agency">\n'
        '<meta property="og:locale" content="en_CA">\n'
        '<meta property="og:title" content="' + title.replace('"', "&quot;") + '">\n'
        '<meta property="og:description" content="' + desc.replace('"', "&quot;") + '">\n'
        '<meta property="og:url" content="' + url + '">\n'
        '<meta property="og:image" content="' + BASE + 'assets/og-image.png">\n'
        '<meta name="twitter:card" content="summary_large_image">\n'
        '<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">\n'
        '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
        '<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@500;700;900&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">\n'
        '<link rel="stylesheet" href="style.css">\n'
        '<script async src="https://www.googletagmanager.com/gtag/js?id=G-P93QZLT872"></script>\n'
        '<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag("js",new Date());gtag("config","G-P93QZLT872");</script>\n'
        '<meta name="theme-color" content="#0A0E14">\n'
        '<script type="application/ld+json">{"@context":"https://schema.org","@type":"LocalBusiness","name":"Packed Agency","telephone":"+1-343-558-5062","email":"info@packedagency.ca","url":"https://packedagency.ca","address":{"@type":"PostalAddress","streetAddress":"500 Preston St","addressLocality":"Ottawa","addressRegion":"ON","addressCountry":"CA"},"areaServed":["Ottawa","Gatineau","Toronto"],"description":"Marketing, exclusive leads and follow-up automation for contractors and home-service companies."}</script>\n</head>\n<body>\n')

def header(active=""):
    def on(k): return " class=\"on\"" if k == active else ""
    return ("<header class=\"top\"><div class=\"wrap nav\">"
        "<a class=\"logo\" href=\"index.html\">" + LOGO_SVG + "<div><b>PACKED</b><span>AGENCY</span></div></a>"
        "<nav class=\"nav-links\" id=\"navLinks\">"
        "<a href=\"services.html\"" + on("services") + ">Services</a>"
        "<a href=\"pricing.html\"" + on("pricing") + ">Pricing</a>" "<a href=\"resources.html\"" + on("resources") + ">Free Resources</a>"
        "<a href=\"results.html\"" + on("results") + ">Results</a>"
        "<a href=\"about.html\"" + on("about") + ">About</a>"
        "<a class=\"nav-phone\" href=\"" + TEL + "\">" + PHONE + "</a>"
        "<a class=\"btn\" href=\"free-audit.html\">Get Free Audit</a></nav>"
        "<button class=\"burger\" onclick=\"document.getElementById('navLinks').classList.toggle('open')\">&#9776;</button>"
        "</div></header>\n")

FORM_JS = """<script>
function wireForm(id,evt,msg){
  var f=document.getElementById(id);if(!f)return;
  f.addEventListener("submit",function(e){
    e.preventDefault();
    var btn=f.querySelector("button[type=submit]"),orig=btn.textContent;
    btn.disabled=true;btn.textContent="Sending...";
    fetch("https://api.web3forms.com/submit",{method:"POST",headers:{"Content-Type":"application/json",Accept:"application/json"},body:JSON.stringify(Object.fromEntries(new FormData(f)))})
    .then(function(r){return r.json()})
    .then(function(d){
      if(d.success){
        f.innerHTML="<div style='padding:26px 6px;text-align:center'><div style='font-family:Archivo,sans-serif;font-weight:900;font-size:22px;color:#fff'>Got it. &#10003;</div><p style='color:#9AA4B4;margin-top:10px;font-size:14.5px'>"+msg+"</p></div>";
        if(window.gtag)gtag("event",evt);
      }else{btn.disabled=false;btn.textContent=orig;alert("Something went wrong - please call or text 343-558-5062.");}
    })
    .catch(function(){btn.disabled=false;btn.textContent=orig;alert("Something went wrong - please call or text 343-558-5062.");});
  });
}
wireForm("auditForm","lead_audit","Your audit is on the way - we will text or call within one business day, and the video lands within two.");
wireForm("contactForm","lead_contact","Message received - we reply within one business day.");
</script>
"""

FOOTER = ("<footer class=\"site\"><div class=\"wrap\"><div class=\"f-grid\">"
    "<div><div class=\"logo\" style=\"margin-bottom:14px\">" + LOGO_SVG + "<div style=\"color:#fff\"><b style=\"color:#fff\">PACKED</b><span>AGENCY</span></div></div>"
    "<p style=\"font-size:14px;max-width:300px\">We keep your schedule packed. Marketing, exclusive leads and follow-up automation for Canada's trades. Ottawa-built.</p></div>"
    "<div><h4>Services</h4><a href=\"local-seo.html\">Local SEO &amp; Maps</a><a href=\"google-ads.html\">Google Ads &amp; LSA</a><a href=\"websites.html\">Conversion Websites</a><a href=\"automation.html\">Follow-up Automation</a><a href=\"calculator.html\">Missed-Call Calculator</a></div>"
    "<div><h4>Trades</h4><a href=\"hvac-marketing.html\">HVAC Marketing</a><a href=\"plumber-marketing.html\">Plumber Marketing</a><a href=\"electrician-marketing.html\">Electrician Marketing</a><a href=\"renovation-marketing.html\">Renovation Marketing</a><a href=\"toronto.html\">Toronto</a></div>"
    "<div><h4>Company</h4><a href=\"process.html\">Our Process</a><a href=\"resources.html\">Free Resources</a><a href=\"guarantees.html\">Guarantees</a><a href=\"results.html\">Results</a><a href=\"reviews.html\">Reviews</a><a href=\"blog.html\">Blog</a><a href=\"contact.html\">Contact</a></div>"
    "</div><div class=\"f-bottom\"><span>&copy; 2026 Packed Agency. All rights reserved.</span>"
    "<span><a href=\"privacy.html\">Privacy Policy</a> &nbsp;&middot;&nbsp; <a href=\"terms.html\">Terms</a> &nbsp;&middot;&nbsp; Client Portal (coming soon)</span></div></div></footer>\n"
    "<a class=\"callbar\" href=\"" + TEL + "\">&#128222; Call Packed &mdash; " + PHONE + "</a>\n" + FORM_JS + "</body>\n</html>")

def phero(kicker, h1, lead, crumb=""):
    c = ("<div class=\"crumb\"><a href=\"index.html\">Home</a> / " + crumb + "</div>") if crumb else ""
    return ("<section class=\"phero\"><div class=\"bgfx\"></div><div class=\"wrap\">" + c +
        "<div class=\"kicker\">" + kicker + "</div><h1>" + h1 + "</h1>"
        "<p class=\"lead\">" + lead + "</p>"
        "<a class=\"btn\" href=\"free-audit.html\">Get My Free Audit</a></div></section>\n")

CTA = ("<section class=\"ctaband\"><div class=\"wrap\"><h2>Ready for a packed schedule?</h2>"
    "<p>Start with the free audit &mdash; we check your Google listing, website and phones, then send you a 10-minute video of what we found. No meeting. No pressure. No cost.</p>"
    "<a class=\"btn\" href=\"free-audit.html\">Get My Free Audit</a>&nbsp;&nbsp;"
    "<a class=\"btn ghost\" href=\"" + TEL + "\">Call or Text " + PHONE + "</a></div></section>\n")

def cb_table(rows):
    out = "<table class=\"cb\"><tr><th>Your concern</th><th>How Packed handles it</th></tr>"
    for a, b in rows:
        out += "<tr><td>" + a + "</td><td>" + b + "</td></tr>"
    return out + "</table>"

PAGES = []
SERVICE_SCHEMA = {
    "local-seo.html": ("Local SEO and Google Maps for Contractors", "Google Maps ranking, reviews and local search for Ottawa contractors.", "1195"),
    "google-ads.html": ("Google Ads and Local Services Ads Management", "Managed Google Ads and LSA campaigns for Ottawa contractors.", "549"),
    "websites.html": ("Contractor Website Design", "Fast websites built to turn visitors into phone calls. Client owns everything.", "2950"),
    "automation.html": ("Follow-up Automation for Contractors", "Missed-call text-back, instant lead follow-up and customer win-back campaigns.", "349"),
}

def _plain(s):
    s = re.sub(r"<[^>]+>", "", s)
    for a, b in (("&amp;", "&"), ("&mdash;", "-"), ("&ndash;", "-"), ("&rsquo;", "'"), ("&ldquo;", '"'), ("&rdquo;", '"'), ("&nbsp;", " ")):
        s = s.replace(a, b)
    return " ".join(s.split())

def page(fname, title, desc, active, body):
    html = head(title, desc, fname) + header(active) + body + FOOTER
    html = html.replace("background:#fff", "background:var(--surface)")
    html = html.replace("background:var(--orange);color:#fff", "background:var(--orange);color:#1A0D02")
    html = html.replace("background:linear-gradient(160deg,#22345A,#1B2A4A)", "background:#1B2435")
    html = html.replace("<iframe src=\"https://maps.google.com", "<iframe loading=\"lazy\" src=\"https://maps.google.com")
    extras = ""
    faqs = re.findall(r"<summary>(.*?)</summary><p>(.*?)</p>", body, re.S)
    if faqs:
        items = [{"@type": "Question", "name": _plain(q), "acceptedAnswer": {"@type": "Answer", "text": _plain(a)}} for q, a in faqs]
        extras += '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": items}) + "</script>\n"
    if fname in SERVICE_SCHEMA:
        nm, ds, pr = SERVICE_SCHEMA[fname]
        extras += '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@type": "Service", "name": nm, "description": ds, "provider": {"@type": "LocalBusiness", "name": "Packed Agency", "telephone": "+1-343-558-5062"}, "areaServed": "Ottawa, ON", "offers": {"@type": "Offer", "price": pr, "priceCurrency": "CAD"}}) + "</script>\n"
    if fname == "blog-hvac-lead-cost.html":
        extras += '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@type": "BlogPosting", "headline": "What an HVAC Lead Costs in Ottawa (2026)", "author": {"@type": "Person", "name": "Sajad"}, "publisher": {"@type": "Organization", "name": "Packed Agency"}, "datePublished": "2026-06-07", "mainEntityOfPage": BASE + fname}) + "</script>\n"
    if extras:
        html = html.replace("</head>", extras + "</head>")
    with open(os.path.join(OUT, fname), "w") as f:
        f.write(html)
    PAGES.append(fname)
    print("wrote", fname)

def svc_page(fname, tag, name, h1, lead, problem, dolist, concerns, numbers, price, crumb):
    body = phero(tag, h1, lead, crumb)
    body += "<section><div class=\"wrap\"><div class=\"grid2\" style=\"align-items:start;gap:50px\">"
    body += "<div><div class=\"kicker\">The problem</div><h2 class=\"sec-h2\" style=\"font-size:30px\">" + problem[0] + "</h2><p class=\"sec-sub\">" + problem[1] + "</p></div>"
    body += "<div><div class=\"kicker\">What we do</div><ul class=\"checks\">"
    for d in dolist: body += "<li>" + d + "</li>"
    body += "</ul></div></div>"
    body += "<div class=\"stat-strip\">"
    for b, s in numbers: body += "<div><b>" + b + "</b><span>" + s + "</span></div>"
    body += "</div>"
    body += "<h2 class=\"sec-h2\" style=\"font-size:28px\">Straight answers to fair concerns</h2>" + cb_table(concerns)
    body += ("<div style=\"display:flex;align-items:center;gap:26px;flex-wrap:wrap;margin-top:30px\">"
        "<div style=\"font-family:'Archivo',sans-serif;font-weight:900;font-size:30px\">" + price[0] +
        " <small style=\"font-size:15px;color:var(--grey);font-weight:500\">" + price[1] + "</small></div>"
        "<a class=\"btn\" href=\"free-audit.html\">Start with the free audit</a></div>")
    body += "</div></section>" + CTA
    page(fname, name + " for Contractors in Ottawa | Packed Agency", lead, "services", body)

def trade_page(fname, trade, h1, lead, pains, math_rows, faq):
    body = phero(trade + " Marketing — Ottawa", h1, lead, trade + " Marketing")
    body += "<section><div class=\"wrap\"><div class=\"kicker\">Sound familiar?</div><h2 class=\"sec-h2\" style=\"font-size:30px\">What keeps " + trade + " owners up at night</h2><div class=\"grid3\" style=\"margin-top:30px\">"
    for t, d in pains:
        body += "<div class=\"card\"><h3>" + t + "</h3><p>" + d + "</p></div>"
    body += "</div>"
    body += "<h2 class=\"sec-h2\" style=\"font-size:28px;margin-top:60px\">The " + trade.lower() + " math, in plain numbers</h2>"
    body += "<table class=\"cb\"><tr><th>Metric</th><th>What it means for you</th></tr>"
    for a, b in math_rows:
        body += "<tr><td>" + a + "</td><td>" + b + "</td></tr>"
    body += "</table>"
    body += ("<div class=\"grid4\" style=\"margin-top:50px\">"
        "<a class=\"card\" href=\"local-seo.html\"><span class=\"tag\">Get Found</span><h3>Local SEO &amp; Maps</h3><p>Own the map pack for your trade.</p></a>"
        "<a class=\"card\" href=\"google-ads.html\"><span class=\"tag\">Get Leads</span><h3>Google Ads &amp; LSA</h3><p>Emergency-intent calls this week.</p></a>"
        "<a class=\"card\" href=\"websites.html\"><span class=\"tag\">Get Hired</span><h3>Conversion Website</h3><p>A site that makes phones ring.</p></a>"
        "<a class=\"card dark\" href=\"automation.html\"><span class=\"badge\">ONLY AT PACKED</span><h3>Follow-up Automation</h3><p>Never lose a missed call again.</p></a></div>")
    body += "<h2 class=\"sec-h2\" style=\"font-size:28px;margin-top:60px\">FAQ for " + trade + " companies</h2><div style=\"max-width:820px\">"
    for q, a in faq:
        body += "<details><summary>" + q + "</summary><p>" + a + "</p></details>"
    body += "</div></div></section>" + CTA
    page(fname, trade + " Marketing Ottawa | Packed Agency", lead, "services", body)

# ============================================================ INDEX
index_body = """
<section class="phero" style="padding:110px 0 90px">
  <div class="bgfx"></div>
  <!-- Hero footage: clip 1 self-hosted (Pexels free license, compressed 720p). Clips 2-5 are
       Mixkit free-license CDN streams; download and self-host them before production launch. -->
  <video id="heroVid" muted playsinline preload="none" aria-hidden="true" poster="assets/hero-poster.jpg"
    style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:.3"></video>
  <script>
  window.addEventListener("load",function(){
    if(window.matchMedia&&window.matchMedia("(prefers-reduced-motion: reduce)").matches)return;
    var clips=["assets/hero-1.mp4",
               "https://assets.mixkit.co/videos/4010/4010-360.mp4",
               "https://assets.mixkit.co/videos/45349/45349-360.mp4",
               "https://assets.mixkit.co/videos/49192/49192-360.mp4",
               "https://assets.mixkit.co/videos/49024/49024-360.mp4"];
    var hv=document.getElementById("heroVid"),i=0;
    if(!hv)return;
    hv.src=clips[0];var pp=hv.play();if(pp&&pp.catch)pp.catch(function(){});
    hv.addEventListener("ended",function(){i=(i+1)%clips.length;hv.src=clips[i];hv.play();});
    hv.addEventListener("error",function(){i=(i+1)%clips.length;if(i!==0){hv.src=clips[i];hv.play();}});
    document.addEventListener("visibilitychange",function(){if(document.hidden){hv.pause();}else{var p=hv.play();if(p&&p.catch)p.catch(function(){});}});
  });
  </script>
  <div class="wrap" style="position:relative;z-index:2">
    <div class="kicker">Marketing for Contractors &amp; Home Services — Ottawa</div>
    <h1 style="font-size:clamp(38px,6vw,66px)">We keep contractors' schedules <em>packed.</em></h1>
    <p class="lead" style="font-size:20px">We get you found on Google, make the phone ring, and follow up on every lead automatically — for HVAC, plumbing, electrical and renovation companies. Everything we build belongs to you.</p>
    <div style="display:flex;gap:14px;flex-wrap:wrap;align-items:center">
      <a class="btn" href="free-audit.html">Get My Free Audit</a>
      <a class="btn ghost" href="tel:+13435585062">Call or Text """ + PHONE + """</a>
    </div>
    <div style="display:flex;gap:10px;flex-wrap:wrap;margin-top:44px">
      <span style="background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.14);padding:9px 18px;border-radius:99px;font-size:14px;font-weight:600;color:#DDE4F0"><b style="color:var(--orange)">HVAC</b></span>
      <span style="background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.14);padding:9px 18px;border-radius:99px;font-size:14px;font-weight:600;color:#DDE4F0"><b style="color:var(--orange)">Plumbing</b></span>
      <span style="background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.14);padding:9px 18px;border-radius:99px;font-size:14px;font-weight:600;color:#DDE4F0"><b style="color:var(--orange)">Electrical</b></span>
      <span style="background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.14);padding:9px 18px;border-radius:99px;font-size:14px;font-weight:600;color:#DDE4F0"><b style="color:var(--orange)">Renovation</b></span>
      <span style="background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.14);padding:9px 18px;border-radius:99px;font-size:14px;font-weight:600;color:#DDE4F0">One client per trade, per city — <b style="color:var(--orange)">yours exclusively</b></span>
    </div>
  </div>
</section>

<div class="statbar">
  <div><b>90%</b><span>of contractor websites never make the phone ring &mdash; yours will</span></div>
  <div><b class="o">5+</b><span>contacts to close a job &mdash; we automate every one</span></div>
  <div><b>100%</b><span>asset ownership &mdash; it&rsquo;s in the contract</span></div>
</div>
<div class="marq" aria-hidden="true"><span>YOU OWN EVERYTHING &#10038;&nbsp; NO LOCK-IN AFTER 90 DAYS &#10038;&nbsp; ONE CLIENT PER TRADE, PER CITY &#10038;&nbsp; YOU OWN EVERYTHING &#10038;&nbsp; NO LOCK-IN AFTER 90 DAYS &#10038;&nbsp; ONE CLIENT PER TRADE, PER CITY &#10038;&nbsp; YOU OWN EVERYTHING &#10038;&nbsp; NO LOCK-IN AFTER 90 DAYS &#10038;&nbsp; ONE CLIENT PER TRADE, PER CITY &#10038;&nbsp; YOU OWN EVERYTHING &#10038;&nbsp; NO LOCK-IN AFTER 90 DAYS &#10038;&nbsp; ONE CLIENT PER TRADE, PER CITY &#10038;&nbsp; YOU OWN EVERYTHING &#10038;&nbsp; NO LOCK-IN AFTER 90 DAYS &#10038;&nbsp; ONE CLIENT PER TRADE, PER CITY &#10038;&nbsp; YOU OWN EVERYTHING &#10038;&nbsp; NO LOCK-IN AFTER 90 DAYS &#10038;&nbsp; ONE CLIENT PER TRADE, PER CITY &#10038;&nbsp; </span></div>

<section style="background:#fff;border-top:1px solid var(--line)">
  <div class="wrap">
    <div class="kicker">Start where it hurts</div>
    <h2 class="sec-h2">Which one sounds like you?</h2>
    <div class="grid4" style="margin-top:36px">
      <a class="card" href="websites.html"><h3 style="font-size:17px">"I need a website that actually brings in work."</h3><p>90% of contractor sites never turn a visit into a call. Yours won't be one of them.</p><span style="color:var(--orange);font-weight:700;font-size:14px">Conversion websites →</span></a>
      <a class="card" href="local-seo.html"><h3 style="font-size:17px">"I have a website. Nobody finds it."</h3><p>97% of homeowners search online. The top 3 map results win the call.</p><span style="color:var(--orange);font-weight:700;font-size:14px">Local SEO &amp; Maps →</span></a>
      <a class="card" href="automation.html"><h3 style="font-size:17px">"My phone rings, but jobs slip away."</h3><p>80% of sales take 5+ contacts. Missed calls quietly cost you thousands.</p><span style="color:var(--orange);font-weight:700;font-size:14px">Follow-up automation →</span></a>
      <a class="card" href="free-audit.html"><h3 style="font-size:17px">"Honestly? I don't know where to start."</h3><p>Ten checks, real numbers, a recorded walkthrough. Free, no obligation.</p><span style="color:var(--orange);font-weight:700;font-size:14px">Free Schedule Audit →</span></a>
    </div>
  </div>
</section>

<section style="background:var(--navy);color:#fff">
  <div class="wrap">
    <div class="kicker">Why "Packed"</div>
    <h2 class="sec-h2">Three things we keep packed.</h2>
    <div class="grid3" style="margin-top:40px">
      <div style="background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.1);border-radius:16px;padding:32px 28px"><h3 style="font-size:21px;margin-bottom:10px">Packed Team</h3><p style="color:#B9C4D8;font-size:15px">Websites, SEO, ads, media and automation — delivered under one roof by the person you actually talk to. No hand-offs, no outsourcing.</p></div>
      <div style="background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.1);border-radius:16px;padding:32px 28px"><h3 style="font-size:21px;margin-bottom:10px">Packed Focus</h3><p style="color:#B9C4D8;font-size:15px">Contractors and home services. Only. We know what an Ottawa HVAC lead costs and what homeowners type at 2 a.m. when the furnace dies.</p></div>
      <div style="background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.1);border-radius:16px;padding:32px 28px"><h3 style="font-size:21px;margin-bottom:10px">Packed Schedule</h3><p style="color:#B9C4D8;font-size:15px">The only metric that matters: booked jobs on your calendar. Every report we send is written in jobs and dollars.</p></div>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="kicker">How it works</div>
    <h2 class="sec-h2">From audit to a packed calendar.</h2>
    <div class="grid3" style="margin-top:40px">
      <div class="card"><h3>1 · Free Schedule Audit</h3><p>Ten checks on your map ranking, reviews, website and follow-up — including a mystery call to your own business.</p><div class="from">Free <small>· no obligation</small></div></div>
      <div class="card"><h3>2 · The Door-Opener</h3><p>A fast, provable win: a &ldquo;win-back&rdquo; campaign to your past customers, or your Google listing fixed top to bottom. Booked jobs inside 30 days.</p><div class="from">$749 <small>· one-time</small></div></div>
      <div class="card"><h3>3 · The Lead Engine</h3><p>Google Maps ranking, fresh reviews, and automatic follow-up on every call and quote — the system that keeps the schedule packed.</p><div class="from">$1,495/mo <small>· no lock-in after 90 days</small></div></div>
    </div>
    <p style="margin-top:24px"><a href="process.html" style="color:var(--orange);font-weight:700">See the full process →</a></p>
  </div>
</section>

<section style="background:#fff;border-top:1px solid var(--line)" id="services">
  <div class="wrap">
    <div class="kicker">What we do</div>
    <h2 class="sec-h2">Everything a trade needs to stay booked.</h2>
    <div class="grid2" style="margin-top:40px">
      <a class="card" href="local-seo.html"><span class="tag">Get Found</span><h3>Get Found on Google Maps</h3><p>When a homeowner searches &ldquo;plumber near me&rdquo;, the top 3 map results get the calls. We put you there — and keep you there.</p><div class="from">From $1,195/mo <small>· or inside the Lead Engine</small></div></a>
      <a class="card" href="google-ads.html"><span class="tag">Get Leads</span><h3>Ads That Pay for Themselves</h3><p>Ads only on searches that mean money — emergencies and big jobs. About $50–60 per call, and you see every dollar spent.</p><div class="from">From $549/mo <small>· or 12% of ad spend</small></div></a>
      <a class="card" href="websites.html"><span class="tag">Get Hired</span><h3>A Website That Makes the Phone Ring</h3><p>Fast, simple, built for one job: turning visitors into calls. And it&rsquo;s yours — in writing.</p><div class="from">$2,950 <small>· one-time</small></div></a>
      <a class="card dark" href="automation.html"><span class="badge">ONLY AT PACKED</span><h3>Never Miss Another Lead</h3><p>Miss a call on the roof? The customer gets a text back in seconds. Every quote gets followed up. Automatically.</p><div class="from" style="color:#fff">From $349/mo <small style="color:#B9C4D8">· setup $995</small></div></a>
    </div>
  </div>
</section>

<section class="guar" style="background:var(--orange);color:#fff;padding:60px 0">
  <div class="wrap grid3" style="text-align:center">
    <div><h3 style="font-size:20px;margin-bottom:6px">You own everything</h3><p style="font-size:14.5px;opacity:.93">Website, ad accounts, data, content. In writing.</p></div>
    <div><h3 style="font-size:20px;margin-bottom:6px">No lock-in</h3><p style="font-size:14.5px;opacity:.93">90-day initial term, then month-to-month.</p></div>
    <div><h3 style="font-size:20px;margin-bottom:6px">One client per trade</h3><p style="font-size:14.5px;opacity:.93">We never work for your competitor in your city.</p></div>
  </div>
</section>

<section style="background:var(--navy);border-top:1px solid var(--line)">
  <div class="wrap"><div class="grid2" style="gap:50px;align-items:center">
    <div>
      <div class="kicker">A note from the founder</div>
      <h2 class="sec-h2" style="font-size:30px">Packed is new. I&rsquo;m not.</h2>
      <p style="color:#B9C4D8;font-size:16px;margin-bottom:14px">I&rsquo;m Sajad. I&rsquo;ve spent 8+ years building campaigns and websites — and watching trades pay agencies for reports full of words that don&rsquo;t mean anything. So I built the agency I&rsquo;d want if I ran a contracting company: plain English, published prices, and promises that go in the contract.</p>
      <p style="color:#B9C4D8;font-size:16px;margin-bottom:18px">Because we&rsquo;re new, you get our best-ever pricing. Because I&rsquo;m confident, you risk 90 days — not a year. When you call, I answer. When something isn&rsquo;t working, I tell you first.</p>
      <a class="btn" href="about.html">More about me</a>&nbsp;&nbsp;<a class="btn ghost" href="guarantees.html">Read the guarantees</a>
    </div>
    <div style="aspect-ratio:4/3;background:#1B2435;border:1px solid var(--line);border-radius:14px;display:flex;align-items:center;justify-content:center;color:#7C8698;font-size:14px;text-align:center;padding:20px">[ Founder photo &mdash; job-site setting. Replace with &lt;img&gt; ]</div>
  </div></div>
</section>

<section>
  <div class="wrap" style="max-width:860px">
    <div class="kicker">Straight answers</div>
    <h2 class="sec-h2" style="font-size:30px">Questions contractors actually ask us</h2>
    <details><summary>How fast will my phone start ringing?</summary><p>Honestly: win-back campaigns and missed-call text-back work within days. Ads work in the first week. Google Maps rankings take 60&ndash;90 days, then keep paying off for years. We always start with the fast stuff so you see proof early.</p></details>
    <details><summary>Do I really own the website and the accounts?</summary><p>Yes — website, Google listing, ad accounts, customer list, photos. Registered in your name from day one, stated in the contract. If we ever part ways, you keep everything, including every password.</p></details>
    <details><summary>What&rsquo;s the minimum commitment?</summary><p>90 days — the shortest honest window to show results. After that it&rsquo;s month-to-month. If we&rsquo;re not earning the money, fire us with 30 days&rsquo; notice. No exit fees.</p></details>
    <details><summary>You&rsquo;re a new agency. Why should I trust you?</summary><p>Don&rsquo;t trust us — check us. Prices are published, the guarantees are in the contract, every report shows real calls and real jobs, and your risk is 90 days, not a 12-month lock-in. Being new is also why you get founder-level attention and our lowest pricing ever. The experience behind it is 8+ years.</p></details>
    <details><summary>I&rsquo;m not good with computers. Is that a problem?</summary><p>Not at all — most of our clients would rather be on the tools, and that&rsquo;s the point. You change nothing about how you work. Calls and texts reach you like they always did, and your monthly report is one page in plain English: calls, jobs, dollars.</p></details>
    <details><summary>Who are you NOT for?</summary><p>Companies that want overnight magic, the cheapest possible option, or won&rsquo;t answer the phone when it rings. If that&rsquo;s the case, we&rsquo;ll say so in the audit and part as friends.</p></details>
  </div>
</section>

<section style="background:var(--surface);border-top:1px solid var(--line)">
  <div class="wrap" style="text-align:center">
    <h2 class="sec-h2">What is a missed call costing you?</h2>
    <p class="sec-sub" style="margin:0 auto 26px">Most contractors lose more to unanswered phones than to any competitor. Find your number in 20 seconds.</p>
    <a class="btn navy" href="calculator.html">Try the Missed-Call Calculator</a>
  </div>
</section>
""" + CTA
page("index.html", "Contractor Marketing Ottawa | Packed Agency",
     "Packed Agency keeps Ottawa contractors' schedules packed — local SEO, exclusive leads, and follow-up automation. You own everything. No lock-in.", "", index_body)

# ============================================================ FREE AUDIT
audit_body = phero("Free — no obligation", "The Free <em>Schedule Audit.</em>",
    "Ten checks on how your business gets found, chosen and booked — delivered as a recorded video walkthrough within 2 business days.", "Free Audit")
audit_body += """
<section><div class="wrap"><div class="grid2" style="gap:60px;align-items:start">
<div>
  <h2 class="sec-h2" style="font-size:28px">What the 10-point audit covers</h2>
  <ul class="checks">
    <li><b>Map ranking</b> — where you sit in the Google map pack for your top 3 money keywords, and who's beating you</li>
    <li><b>Review gap</b> — your review count and velocity vs. your strongest local competitor</li>
    <li><b>Website conversion score</b> — the 7 elements that make phones ring (click-to-call, forms, speed, proof)</li>
    <li><b>The mystery call</b> — we call your business once and time what happens, exactly like a homeowner would</li>
    <li><b>Missed-call exposure</b> — your estimated dollars lost per year to unanswered calls and dead follow-up</li>
    <li><b>Listings &amp; citations</b> — whether Google can trust your business data</li>
    <li><b>Ad presence check</b> — what your competitors spend to outrank you, and whether it's working</li>
  </ul>
  <h2 class="sec-h2" style="font-size:24px;margin-top:34px">What you get</h2>
  <p class="sec-sub">A 10-minute recorded video of your results — watch it on a job site, share it with your partner, no meeting required. If we see things you can fix yourself for free, we say so. If we think we can help, we'll tell you exactly what we'd do and what it costs. That's the whole pitch.</p>
</div>
<div class="aform">
  <h3>Get your free audit</h3>
  <p class="sub">Takes under a minute.</p>
  <ol style="margin:0 0 10px 18px;font-size:13.5px;color:var(--grey);line-height:1.8"><li>You fill in the basics below</li><li>We check your Google listing, website, reviews and phones</li><li>You get a 10-minute video in 2 business days &mdash; no meeting, no pressure</li></ol>
  <form id="auditForm">
    <input type="hidden" name="access_key" value="9aac958d-5965-4b75-8736-b6ab7274db68">
    <input type="hidden" name="subject" value="NEW LEAD: Free Audit request (packedagency.ca)">
    <input type="hidden" name="from_name" value="Packed Agency Website">
    <input type="checkbox" name="botcheck" style="display:none" tabindex="-1" autocomplete="off">
    <label>Name</label><input type="text" name="name" placeholder="Mike Tremblay" required>
    <label>Email</label><input type="email" name="email" placeholder="mike@tremblayheating.ca" required>
    <label>Trade</label>
    <select name="trade" required><option value="">Choose your trade…</option><option>HVAC / Heating &amp; Cooling</option><option>Plumbing</option><option>Electrical</option><option>Renovation / General Contracting</option><option>Roofing</option><option>Kitchen &amp; Bath</option><option>Flooring</option><option>Painting</option><option>Windows &amp; Doors</option><option>Landscaping / Lawn Care</option><option>Concrete / Paving</option><option>Fencing &amp; Decks</option><option>Garage Doors</option><option>Eavestrough / Siding</option><option>Cleaning Services</option><option>Pest Control</option><option>Appliance Repair</option><option>Moving</option><option>Other home service</option></select>
    <label>Phone</label><input type="tel" name="phone" placeholder="613-555-0123" required>
    <label>City / area <span style="font-weight:500;color:var(--grey)">(optional)</span></label><input type="text" name="city" placeholder="Ottawa, Kanata, Orl&eacute;ans&hellip;">
    <label>Biggest headache right now? <span style="font-weight:500;color:var(--grey)">(optional)</span></label>
    <select name="pain_point"><option value="">Pick one&hellip;</option><option>My website brings in no work</option><option>Nobody finds us on Google</option><option>We miss calls / leads slip away</option><option>Not enough reviews</option><option>Slow season &mdash; need jobs now</option><option>Paying for leads that go nowhere</option><option>I don&rsquo;t know where to start</option><option>Something else</option></select>
    <button class="btn" type="submit">Send Me My Free Audit</button>
    <p class="fine">By submitting, you agree to receive a reply by phone, text or email about your audit. No spam, no list-selling, unsubscribe anytime. (CASL compliant)</p>
    <p class="fine" style="margin-top:8px"><b>Hate forms?</b> Text the word <b>AUDIT</b> to <a href="sms:+13435585062" style="color:var(--orange);font-weight:700">343-558-5062</a> and we&rsquo;ll take it from there.</p>
  </form>
</div>
</div>
<div style="max-width:820px;margin-top:60px">
  <h2 class="sec-h2" style="font-size:26px">Fair questions</h2>
  <details><summary>What's the catch?</summary><p>The audit is our Door-Opener — some businesses who get it become clients, most at least learn something. We'd rather earn trust with free value than cold-pitch you.</p></details>
  <details><summary>Will you spam me afterwards?</summary><p>You'll get the audit, one follow-up to ask if you have questions, and that's it unless you reply. We sell follow-up automation — we know exactly where the line between persistent and annoying is.</p></details>
  <details><summary>I'm not in HVAC/plumbing/electrical/reno. Can I still get one?</summary><p>If you're an owner-run home-service business in the Ottawa area, yes — request it and we'll tell you straight if we're not the right fit.</p></details>
</div>
</div></section>"""
page("free-audit.html", "Free Marketing Audit for Contractors | Packed Agency",
     "Free 10-point schedule audit for Ottawa contractors: map ranking, reviews, website conversion, mystery call. Video walkthrough in 2 days.", "", audit_body)

# ============================================================ PRICING
pricing_body = phero("Published. Like it should be.", "Real prices. <em>No sales-call required.</em>",
    "Almost no agency publishes prices. We do — because $1,495 a month should be an easy decision when one extra furnace install covers it.", "Pricing")
pricing_body += """
<section><div class="wrap">
<div class="grid4" style="align-items:stretch">
  <div class="price-card"><span class="tag">Step 1</span><h3>Door-Opener</h3><div class="amt">$749</div><div class="per">one-time</div>
    <ul class="checks"><li>A &ldquo;win-back&rdquo; text/email campaign to your past customers <i>or</i> your Google listing fixed top to bottom</li><li>Tracked results in ~30 days</li><li>No strings attached</li></ul></div>
  <div class="price-card"><span class="tag">Foundation</span><h3>Conversion Website</h3><div class="amt">$3,950</div><div class="per">one-time · website + Google listing + brand refresh</div>
    <ul class="checks"><li>WordPress — you own it, in writing</li><li>Click-to-call, quote forms, reviews</li><li>SEO-ready structure</li></ul></div>
  <div class="price-card hot"><span class="pin">MOST POPULAR</span><span class="tag">Monthly</span><h3>Lead Engine</h3><div class="amt">$1,495</div><div class="per">per month · 90 days, then month-to-month</div>
    <ul class="checks"><li>Google Maps ranking work (local SEO)</li><li>Automatic review requests after every job</li><li>Missed calls get an instant text back</li><li>New leads answered in under a minute</li><li>Monthly report in jobs and dollars</li></ul></div>
  <div class="price-card"><span class="tag">Monthly</span><h3>Growth</h3><div class="amt">$2,950</div><div class="per">per month + ad spend</div>
    <ul class="checks"><li>Everything in Lead Engine</li><li>Google Ads + LSA management</li><li>Social media management</li><li>Quarterly content day (photo/video)</li></ul></div>
</div>
<div class="note"><b>The anchor:</b> $1,495/month is roughly the price of 16 shared HomeStars/Angi leads — except marketplace leads get sold to five competitors and disappear, while everything we build is exclusive and compounds. One average HVAC install pays for the month.</div>
<h2 class="sec-h2" style="font-size:28px;margin-top:50px">À la carte</h2>
<table class="cb"><tr><th>Service</th><th>Price</th></tr>
<tr><td>Local SEO (standalone)</td><td>$1,195/mo</td></tr>
<tr><td>Google Ads management</td><td>$549/mo or 12% of ad spend above $5k</td></tr>
<tr><td>Local Services Ads management</td><td>$449/mo flat</td></tr>
<tr><td>Meta/Facebook lead campaigns</td><td>$449/mo add-on</td></tr>
<tr><td>Landing page</td><td>$649 per page</td></tr>
<tr><td>Missed-call text-back (alone)</td><td>$199/mo</td></tr>
<tr><td>Automation suite (speed-to-lead + booking + reviews)</td><td>$995 setup + $349/mo</td></tr>
<tr><td>Database reactivation campaign</td><td>$749 per campaign</td></tr>
<tr><td>Reputation management</td><td>$249/mo</td></tr>
<tr><td>Social media management</td><td>$649/mo</td></tr>
<tr><td>Logo / brand kit</td><td>$495 / $1,250</td></tr>
<tr><td>Promo video / job-site content day</td><td>$1,450 / $495</td></tr></table>
<div style="max-width:820px;margin-top:40px">
<details><summary>Why are you cheaper than the big agencies?</summary><p>Lower overhead, no account-manager layers, and entry pricing while we build our Ottawa case-study wall. Prices rise as proof accumulates — locking in now is genuinely the best deal we'll ever offer.</p></details>
<details><summary>What's NOT included?</summary><p>Ad spend (paid directly to Google/Meta — your account, your money, full visibility) and third-party costs like premium stock or print runs. No markups, no surprises.</p></details>
</div>
</div></section>""" + CTA
page("pricing.html", "Pricing | Packed Agency — Contractor Marketing Ottawa",
     "Published pricing: Door-Opener $749, conversion website $3,950, Lead Engine $1,495/mo, Growth $2,950/mo. No lock-in after 90 days.", "pricing", pricing_body)

# ============================================================ SERVICES HUB
svc_body = phero("Services", "Built to fill <em>calendars,</em> not dashboards.",
    "Four services, one job: more booked work. Each comes with call tracking and a monthly report written in jobs and dollars.", "Services")
svc_body += """
<section><div class="wrap"><div class="grid2">
  <a class="card" href="local-seo.html"><span class="tag">Get Found</span><h3>Local SEO &amp; Google Maps</h3><p>Show up in the top 3 on Google Maps — where homeowners actually pick who to call.</p><div class="from">From $1,195/mo</div></a>
  <a class="card" href="google-ads.html"><span class="tag">Get Leads</span><h3>Google Ads &amp; Local Services Ads</h3><p>Paid ads only on the searches that mean money. Calls this week, not next season.</p><div class="from">From $549/mo</div></a>
  <a class="card" href="websites.html"><span class="tag">Get Hired</span><h3>Conversion Websites</h3><p>Fast, simple sites built to turn visitors into phone calls. You own every file.</p><div class="from">$2,950 one-time</div></a>
  <a class="card dark" href="automation.html"><span class="badge">ONLY AT PACKED</span><h3>Follow-up Automation</h3><p>Missed calls texted back in seconds, every quote followed up, past customers brought back. Nobody else here sells this.</p><div class="from" style="color:#fff">From $349/mo</div></a>
</div>
<p style="margin-top:34px;text-align:center"><a class="btn navy" href="calculator.html">First: see what missed calls cost you →</a></p>
</div></section>""" + CTA
page("services.html", "Services | Packed Agency", "Local SEO, Google Ads, conversion websites and follow-up automation for Ottawa contractors.", "services", svc_body)

# ============================================================ SERVICE PAGES
svc_page("local-seo.html", "Get Found", "Local SEO",
    "Own the <em>map pack.</em>", "When a furnace dies at 2 a.m., the top three Google Maps results get the call. We put you there — and keep you there.",
    ("Invisible where it matters most",
     "97% of consumers search online for local services and 88% contact a business straight from the results. If you're not in the top 3 map results for your trade, you effectively don't exist for most of your market — no matter how good your work is."),
    ["Google Business Profile rebuilt: categories, services, photos, weekly posts, Q&amp;A",
     "Review engine: automated requests after every job, response handling",
     "Service-area and city pages that rank for '[trade] + [neighbourhood]'",
     "Citations and listings cleanup so Google trusts your data",
     "Monthly map-rank tracking on your real money keywords"],
    [("\"SEO is a black box — how do I know it's working?\"", "Call tracking from day one and a monthly report showing rankings, calls and booked jobs. You see everything we see."),
     ("\"I tried SEO before. Nothing happened.\"", "Most 'SEO' is generic blog posts. Local trades SEO is GBP + reviews + service-area pages — different work, measured in map positions, visible in 60–90 days."),
     ("\"What if I stop paying?\"", "You keep everything: profile, reviews, pages, rankings. We build assets you own, not rentals.")],
    [("Top 3", "map results take most calls"), ("~40%", "lower cost-per-sale vs. paid ads"), ("20–50", "leads/mo from a strong GBP")],
    ("From $1,195/mo", "or included in the Lead Engine at $1,495/mo"), "Local SEO")

svc_page("google-ads.html", "Get Leads", "Google Ads & LSA",
    "Calls <em>this week.</em>", "Search ads and Local Services Ads on emergency-intent keywords — tightly managed, fully tracked, in an account you own.",
    ("Paying Google without a pilot",
     "Most contractor ad accounts are set up once and left to burn money: broad keywords, no negative lists, clicks sent to a homepage that doesn't convert. Google happily takes the budget either way."),
    ["Search campaigns on high-intent and emergency keywords only",
     "Local Services Ads setup, badge verification and lead disputing",
     "Dedicated landing pages — never your homepage",
     "Call tracking and recording on every ad dollar",
     "Weekly optimization: bids, negatives, A/B tests"],
    [("\"Ads are expensive.\"", "Unmanaged ads are expensive. Benchmarks we manage to: ~$50–60 per call with ~55% close rates — that's roughly $110 per booked job."),
     ("\"Agencies hide what they spend.\"", "The ad account is yours. You see every dollar, every keyword, every call. Our fee is separate and flat."),
     ("\"I tried LSA and got junk leads.\"", "LSA leads can be disputed — most contractors don't know that. We dispute aggressively; you only pay for real ones.")],
    [("$50–60", "typical cost per call, managed"), ("55%", "typical close rate on ad calls"), ("70%", "of contractors now use LSA — most unmanaged")],
    ("From $549/mo", "or 12% of ad spend above $5,000"), "Google Ads")

svc_page("websites.html", "Get Hired", "Conversion Websites",
    "A website that makes <em>phones ring.</em>", "Fast, mobile-first, built around one job: turning a visit into a call or quote request. On WordPress. Yours, in writing.",
    ("Beautiful sites that never ring",
     "About 90% of contractor websites fail to convert visitors into calls — slow loading, no click-to-call, buried phone numbers, zero proof. A site like that doesn't just underperform; it silently wastes every ad dollar and SEO gain you ever buy."),
    ["5–10 page WordPress build: services, service areas, reviews, financing",
     "Click-to-call everywhere, quote forms above the fold",
     "Job photos and reviews wired in as proof, not decoration",
     "Page-speed and mobile-first by default — homeowners search from phones",
     "SEO-ready structure so rankings have somewhere to land"],
    [("\"Agencies keep your website hostage.\"", "The #1 complaint about big platforms. Ours: WordPress, your hosting, your login, ownership stated in the agreement. Leave anytime, take everything."),
     ("\"I already have a website.\"", "If it's fast and converting, keep it — we'll say so in the audit. If it leaks leads, we'll show you exactly where, with numbers."),
     ("\"$3,950 seems cheap. What's missing?\"", "Nothing — it's entry pricing while we build our Ottawa portfolio. Same conversion structure the $10k agencies sell.")],
    [("90%", "of contractor sites fail to convert"), ("75%", "judge credibility by the website"), ("<3s", "load time we build to")],
    ("$3,950", "one-time, incl. GBP + brand refresh · site alone $2,950"), "Websites")

svc_page("automation.html", "ONLY AT PACKED", "Follow-up Automation",
    "Stop losing jobs you <em>already won.</em>", "Missed-call text-back, speed-to-lead sequences, and database reactivation — the conversion layer no other agency in this market sells.",
    ("The leak nobody talks about",
     "80% of sales happen after the fifth contact — but most contractors stop after one attempt, and 30–60% of calls to trades go unanswered during work hours. You don't have a leads problem. You have a follow-up problem, and it's costing more than any ad budget."),
    ["Missed-call text-back: every unanswered call gets an instant SMS — recovers 30–60% of missed calls into conversations",
     "Speed-to-lead: form and LSA leads get a response in under 60 seconds, then a 5-touch sequence until booked",
     "Database reactivation: seasonal campaigns to your past customers — documented results at under $9 cost-per-sale",
     "Review requests fired automatically when a job closes",
     "All of it visible in one pipeline you can check from your truck"],
    [("\"Automated texts will annoy my customers.\"", "A homeowner who just called you wants a reply. 'Sorry we missed you — this is Mike's Plumbing, how can we help?' within 10 seconds is service, not spam."),
     ("\"I'm not technical.\"", "You change nothing about how you work. Calls and texts reach you exactly as before — the system just catches everything you can't."),
     ("\"Why doesn't every agency sell this?\"", "Because it's operations, not media — agencies sell what they know. We checked every competitor's site: none of them offer it. That's exactly why we lead with it.")],
    [("30–60%", "of missed calls recovered by text-back"), ("80%", "of sales need 5+ contacts"), ("<$9", "cost-per-sale in documented reactivation campaigns")],
    ("From $349/mo", "+ $995 setup · text-back alone $199/mo"), "Automation")

# ============================================================ ABOUT
about_body = phero("About Packed", "Built by a marketer who got tired of <em>agencies.</em>",
    "8+ years running campaigns. One conclusion: the trades deserve better than lock-ins, jargon and rented websites.", "About")
about_body += """
<section><div class="wrap"><div class="grid2" style="gap:60px;align-items:start">
<div>
  <div style="aspect-ratio:3/4;max-width:340px;background:linear-gradient(160deg,#22345A,#1B2A4A);border-radius:18px;display:flex;align-items:center;justify-content:center;color:#7E8DAA;font-size:14px;text-align:center;padding:20px">[ Founder photo — job-site setting. Replace with &lt;img&gt; ]</div>
</div>
<div class="prose">
  <h2 style="font-size:30px;margin-top:0">The short version</h2>
  <p>I'm Sajad. I've spent more than eight years building marketing campaigns — websites, search, paid ads, video, automation — and watching the same story repeat: a hardworking business pays an agency, gets a pretty report full of impressions, and can't point to a single booked job it produced.</p>
  <p>Packed exists to be the opposite of that. One vertical — contractors and home services. One metric — booked jobs. One person accountable — me. I build your site, run your campaigns, and wire the automation personally. When you call, the person who answers is the person who did the work.</p>
  <h2 style="font-size:24px">The three things we keep packed</h2>
  <p><b>A packed team</b> — full-stack delivery under one roof. <b>A packed focus</b> — trades only, so every lesson from one client makes the next one stronger. <b>A packed schedule</b> — yours, which is the only outcome we report on.</p>
  <h2 style="font-size:24px">Where we work</h2>
  <p>Ottawa first — in person, on job sites, at supplier counters. Toronto and the rest of Canada as we grow. One client per trade, per city, always.</p>
  <p><a class="btn" href="guarantees.html">Read our three guarantees</a></p>
</div>
</div></div></section>""" + CTA
page("about.html", "About | Packed Agency", "Founder-led contractor marketing in Ottawa. 8+ years experience, full-stack delivery, trades only.", "about", about_body)

# ============================================================ GUARANTEES
guar_body = phero("In writing, not in vibes", "Three guarantees. <em>Contract language.</em>",
    "Every promise below appears in your agreement — because the biggest agencies in this industry built their reputations on the opposite.", "Guarantees")
guar_body += """
<section><div class="wrap prose">
  <h2>1. You own everything.</h2>
  <p>Your website (WordPress, on hosting registered to you), your Google Business Profile, your ad accounts, your customer data, your content. All of it registered in your name from day one. If we ever part ways, you keep every asset and every login — stated explicitly in the agreement. The industry's worst habit is holding websites hostage on proprietary platforms; we built our contract specifically against it.</p>
  <h2>2. No lock-in.</h2>
  <p>Retainers run a 90-day initial term — the minimum honest window to show results — and then month-to-month, cancel with 30 days' notice. No 12-month commitments, no exit fees, no "talk to retention." We keep clients by keeping schedules packed.</p>
  <h2>3. One client per trade, per city.</h2>
  <p>While you're a client, we will not take on a competing business in your trade in your market. Your competitor can't hire us at any price. Agencies that serve five roofers in one city make their clients bid against each other with their own marketing budgets — we think that's absurd, and we put the exclusivity in writing.</p>
  <div class="note"><b>What we don't guarantee:</b> specific rankings or a specific number of leads — anyone who promises those is lying to you. What we guarantee is transparent reporting in jobs and dollars, and the honesty to tell you when something isn't working.</div>
</div></section>""" + CTA
page("guarantees.html", "Our Guarantees | Packed Agency", "You own everything. No lock-in after 90 days. One client per trade per city. In contract language.", "", guar_body)

# ============================================================ CONTACT
contact_body = phero("Contact", "Talk to the person who <em>does the work.</em>",
    "No call centre, no account managers. Phone, text or email — you reach the founder.", "Contact")
contact_body += """
<section><div class="wrap"><div class="grid2" style="gap:60px;align-items:start">
<div class="prose">
  <h2 style="margin-top:0">Reach us</h2>
  <p><b>Phone / text:</b> <a href=\"""" + TEL + """\" style="color:var(--orange);font-weight:700">""" + PHONE + """</a><br>
  <b>Email:</b> <a href="mailto:""" + EMAIL + """" style="color:var(--orange);font-weight:700">""" + EMAIL + """</a><br>
  <b>Address:</b> 500 Preston St, Ottawa, ON<br>
  <b>Service area:</b> Ottawa–Gatineau and surrounding region · Toronto/GTA (remote)</p>
  <div style="border-radius:14px;overflow:hidden;border:1.5px solid var(--line);margin-top:20px">
    <iframe src="https://maps.google.com/maps?q=500%20Preston%20St%2C%20Ottawa%2C%20ON&z=15&output=embed"
      width="100%" height="280" style="border:0;display:block" loading="lazy" title="Packed Agency — 500 Preston St, Ottawa"></iframe>
  </div>
  <p>Prefer to skip the back-and-forth? The fastest path is the <a href="free-audit.html" style="color:var(--orange);font-weight:700">free audit</a> — you'll have real numbers about your business before we ever talk.</p>
</div>
<div class="aform">
  <h3>Send a message</h3>
  <p class="sub">We reply within one business day.</p>
  <form id="contactForm">
    <input type="hidden" name="access_key" value="9aac958d-5965-4b75-8736-b6ab7274db68">
    <input type="hidden" name="subject" value="NEW MESSAGE: Contact form (packedagency.ca)">
    <input type="hidden" name="from_name" value="Packed Agency Website">
    <input type="checkbox" name="botcheck" style="display:none" tabindex="-1" autocomplete="off">
    <label>Name</label><input type="text" name="name" required>
    <label>Phone or email</label><input type="text" name="contact_info" required>
    <label>What do you need?</label><input type="text" name="message" placeholder="e.g., my website brings zero leads">
    <button class="btn" type="submit">Send</button>
    <p class="fine">CASL consent: by submitting you agree to be contacted about your inquiry. Unsubscribe anytime.</p>
    <p class="fine" style="margin-top:8px"><b>Faster:</b> call or text <a href="tel:+13435585062" style="color:var(--orange);font-weight:700">343-558-5062</a> &mdash; you reach Sajad directly, not a call centre.</p>
  </form>
</div>
</div></div></section>"""
page("contact.html", "Contact | Packed Agency", "Contact Packed Agency — contractor marketing in Ottawa. Phone, text, email or the free audit.", "", contact_body)

# ============================================================ PROCESS
process_body = phero("Our process", "Five steps. <em>Zero mystery.</em>",
    "Copying the best client experience in the industry, minus the 12-month contract.", "Process")
steps = [
    ("Free Schedule Audit", "Ten checks, a mystery call, and a recorded video of your results. You learn where the leaks are whether or not you hire us."),
    ("Door-Opener (~30 days)", "A $749 quick win — database reactivation or GBP overhaul — with tracked results. We earn the retainer conversation with proof, not promises."),
    ("Strategy + Onboarding", "One working session: your trades, service areas, capacity, season. Call tracking goes live the same week — measurement before marketing."),
    ("The Lead Engine (ongoing)", "Local SEO, reviews, missed-call text-back, speed-to-lead. Ads layered on when the foundation converts. Everything visible in your pipeline."),
    ("Monthly Jobs Report", "One page: calls received, jobs booked, dollars attributed, what we're changing next. If something underperforms, the report says so first."),
]
process_body += "<section><div class=\"wrap\" style=\"max-width:860px\">"
for i, (t, d) in enumerate(steps, 1):
    process_body += ("<div style=\"display:flex;gap:26px;margin-bottom:34px\"><div style=\"font-family:'Archivo',sans-serif;font-weight:900;font-size:42px;color:var(--orange);min-width:64px\">0" + str(i) + "</div>"
        "<div><h3 style=\"font-size:21px;margin-bottom:6px\">" + t + "</h3><p style=\"color:var(--grey)\">" + d + "</p></div></div>")
process_body += "</div></section>" + CTA
page("process.html", "Our Process | Packed Agency", "From free audit to packed calendar in five transparent steps.", "", process_body)

# ============================================================ CALCULATOR
calc_body = phero("Free tool", "The Missed-Call <em>Cost Calculator.</em>",
    "Three numbers, twenty seconds, and you'll know what unanswered phones cost your business every year.", "Calculator")
calc_body += """
<section><div class="wrap"><div class="grid2" style="gap:60px;align-items:start">
<div class="calc">
  <h3 style="font-size:22px;margin-bottom:4px">Your numbers</h3>
  <label>Missed calls per week (be honest — during jobs, after hours)</label>
  <input type="number" id="mc" value="8" min="0">
  <label>Your close rate on real enquiries (%)</label>
  <input type="number" id="cr" value="40" min="1" max="100">
  <label>Average job value ($)</label>
  <input type="number" id="jv" value="450" min="1">
  <div class="result"><span>Estimated revenue lost per year</span><b id="out">$0</b><span id="outsub"></span></div>
</div>
<div class="prose">
  <h2 style="margin-top:0">Why this number is real</h2>
  <p>Industry data shows 30–60% of calls to trades go unanswered during working hours — owners are on roofs, under sinks, on ladders. And about 85% of callers who hit voicemail don't leave a message; they call the next name on Google.</p>
  <p>Missed-call text-back fires an SMS within seconds of any unanswered call ("Sorry we missed you — this is Mike's Plumbing, how can we help?"). Documented recovery rates run 30–60% of those calls back into conversations.</p>
  <p><b>The fix costs $199/month.</b> Compare that to the number on the left.</p>
  <a class="btn" href="automation.html">See Follow-up Automation</a>
</div>
</div></div></section>
<script>
function calc(){
  var mc=+document.getElementById('mc').value||0, cr=(+document.getElementById('cr').value||0)/100, jv=+document.getElementById('jv').value||0;
  var lost=Math.round(mc*52*0.85*cr*jv);
  var rec=Math.round(lost*0.45);
  document.getElementById('out').textContent='$'+lost.toLocaleString();
  document.getElementById('outsub').textContent='Text-back could recover roughly $'+rec.toLocaleString()+' of it.';
}
['mc','cr','jv'].forEach(function(id){document.getElementById(id).addEventListener('input',calc)});calc();
</script>""" + CTA
page("calculator.html", "Missed-Call Cost Calculator | Packed Agency", "What do missed calls cost your contracting business? Find out in 20 seconds.", "", calc_body)

# ============================================================ RESULTS / REVIEWS (honest placeholders)
results_body = phero("Results", "Judge us by <em>evidence,</em> not adjectives.",
    "We are a new agency and we refuse to fake it. Here is what you CAN verify today — and exactly what every future case study will show.", "Results")
results_body += """
<section><div class="wrap">
  <div class="kicker">Proof you can check right now</div>
  <h2 class="sec-h2" style="font-size:30px">This website is our first case study.</h2>
  <div class="grid3" style="margin-top:30px">
    <div class="card"><h3>Built like we build for clients</h3><p>Conversion-first layout, click-to-call everywhere, sub-3-second loads, published pricing. Every principle we sell is running on the page you are reading.</p></div>
    <div class="card"><h3>The tools work — try one</h3><p>The <a href="calculator.html" style="color:var(--orange);font-weight:700">Missed-Call Calculator</a> is the same kind of automation thinking we install for clients. Twenty seconds, real math.</p></div>
    <div class="card"><h3>We teach in public</h3><p>The <a href="blog.html" style="color:var(--orange);font-weight:700">blog</a> and <a href="resources.html" style="color:var(--orange);font-weight:700">free resources</a> publish our actual playbooks with real benchmark numbers. No gatekeeping.</p></div>
  </div>

  <div class="kicker" style="margin-top:60px">The founder's track record</div>
  <h2 class="sec-h2" style="font-size:28px">8+ years of campaigns behind this.</h2>
  <p class="sec-sub">Packed is new. The experience isn't: eight-plus years of hands-on work across paid ads, search, web builds and automation — with documented campaign results we walk through in every audit call. Ask, and we will show you the numbers screen-by-screen.</p>

  <div class="kicker" style="margin-top:60px">What every Packed case study will look like</div>
  <h2 class="sec-h2" style="font-size:28px">The report format, shown with sample data</h2>
  <p class="sec-sub" style="margin-bottom:20px">Below is the exact format clients receive monthly — populated here with illustrative numbers so you can see the standard. Real client studies replace this as results are verified.</p>
  <table class="cb"><tr><th>Metric (sample format — illustrative data)</th><th>Month 1</th><th>Month 3</th></tr>
    <tr><td>Tracked calls received</td><td>22</td><td>47</td></tr>
    <tr><td>Missed calls recovered by text-back</td><td>6</td><td>11</td></tr>
    <tr><td>Jobs booked (attributed)</td><td>8</td><td>19</td></tr>
    <tr><td>Revenue attributed</td><td>$9,400</td><td>$23,800</td></tr>
    <tr><td>Google map-pack position (main keyword)</td><td>#9</td><td>#3</td></tr>
    <tr><td>Reviews added</td><td>+4</td><td>+17</td></tr></table>
  <div class="note"><b>Why the honesty:</b> every agency claims results; almost none show their reporting standard before you sign. This page will fill with verified Ottawa case studies — first clients get entry pricing locked for life in exchange for letting us publish their (anonymized if preferred) numbers.</div>
  <a class="btn" href="free-audit.html" style="margin-top:10px">Be the first case study — start with the audit</a>
</div></section>""" + CTA
page("results.html", "Results & Reporting Standard | Packed Agency", "What Packed has done, what you can verify today, and the exact report format every client receives.", "results", results_body)

reviews_body = phero("Reviews", "What clients say — <em>verified.</em>",
    "Live Google reviews will be embedded here. We don't paste quotes we can't prove.", "Reviews")
reviews_body += """
<section><div class="wrap">
<div class="note" style="max-width:760px">Google reviews widget goes here once the Google Business Profile is live (GHL or Elfsight embed — both free options documented in the launch checklist). Until then, this page stays honest and empty.</div>
<p style="margin-top:24px"><a class="btn navy" href="results.html">See results instead →</a></p>
</div></section>""" + CTA
page("reviews.html", "Reviews | Packed Agency", "Verified Google reviews from Ottawa contractors.", "", reviews_body)

# ============================================================ BLOG + first post
blog_body = phero("The Packed Blog", "We give the playbook <em>away.</em>",
    "Weekly, Ottawa-specific answers to the questions contractors actually type into Google. Teaching is our marketing.", "Blog")
blog_body += """
<section><div class="wrap"><div class="grid3">
  <a class="card" href="blog-hvac-lead-cost.html"><span class="tag">Published</span><h3>What an HVAC Lead Costs in Ottawa (2026)</h3><p>Real benchmark numbers: LSA, Google Ads, marketplaces and SEO compared — and which one quietly wins.</p><span style="color:var(--orange);font-weight:700;font-size:14px">Read →</span></a>
  <div class="card" style="opacity:.7"><span class="tag">Next week</span><h3>The Mystery Call: We Phoned 10 Ottawa Plumbers</h3><p>How many answered? How many called back? The results explain a lot about who's busy.</p></div>
  <div class="card" style="opacity:.7"><span class="tag">Coming</span><h3>HomeStars vs. Owning Your Leads: the Real Math</h3><p>What shared leads actually cost over a year, vs. building sources you own.</p></div>
</div></div></section>""" + CTA
page("blog.html", "Contractor Marketing Blog | Packed Agency", "Ottawa-specific contractor marketing answers, published weekly.", "", blog_body)

post_body = phero("Blog · 6 min read", "What an HVAC Lead Costs in Ottawa <em>(2026)</em>",
    "Real benchmark numbers across every channel — so you can stop guessing what 'good' looks like.", "Blog")
post_body += """
<section><div class="wrap prose">
  <p>If you run an HVAC company in Ottawa, you're probably paying for leads somewhere — Google, HomeStars, Local Services Ads, maybe a marketing agency. The question almost nobody can answer: <b>what should a lead actually cost?</b> Here are the benchmark numbers, straight from published 2025–2026 industry data.</p>
  <h2>The benchmarks</h2>
  <ul>
    <li><b>Google Local Services Ads (LSA):</b> $60–$120 per lead for HVAC — pay-per-lead, and you can dispute junk. About 70% of contractors now use LSA; most run it unmanaged.</li>
    <li><b>Google Search Ads:</b> roughly $50–$60 per call when tightly managed, with close rates around 55% — about $110 per booked job.</li>
    <li><b>Home-services average across channels:</b> ~$91 per lead. HVAC sits near $105.</li>
    <li><b>Marketplaces (HomeStars/Angi):</b> comparable sticker price per lead — but the same homeowner is sold to up to five competitors, so your real cost per <i>won</i> job is far higher.</li>
    <li><b>Local SEO / map pack:</b> the slow channel that wins: top-3 map placement averages about 40% lower cost-per-sale than paid ads, and a well-built Google Business Profile alone can drive 20–50 calls a month.</li>
  </ul>
  <h2>The number nobody benchmarks: leads you already paid for and lost</h2>
  <p>Industry studies show 80% of sales take five or more contacts — while most contractors stop following up after one. Add unanswered calls during work hours and the math gets ugly: the cheapest lead you'll ever buy is the one already in your missed-call log. (Try our <a href="calculator.html" style="color:var(--orange);font-weight:700">missed-call calculator</a> — it takes 20 seconds and usually hurts.)</p>
  <h2>What we'd do with a $2,000/month budget in Ottawa</h2>
  <p>First $200: fix follow-up — missed-call text-back and a five-touch sequence, so nothing leaks. Next $1,000+: own the map pack — GBP, reviews, service-area pages. The rest: LSA, managed and disputed weekly. Paid search ads only after the first two are converting, because ads pointed at a leaky bucket just speed up the leak.</p>
  <p><i>Sources: LocaliQ 2025 home-services benchmarks, Contractor Marketing Pros HVAC lead-cost data, WebFX home-services benchmarks. Full citations available on request — we don't make numbers up.</i></p>
</div></section>""" + CTA
page("blog-hvac-lead-cost.html", "What an HVAC Lead Costs in Ottawa (2026) | Packed Agency",
     "HVAC lead cost benchmarks for Ottawa: LSA $60-120, search ads ~$50-60/call, marketplaces vs map pack compared.", "", post_body)

# ============================================================ TRADE PAGES (Phase 2)
trade_page("hvac-marketing.html", "HVAC",
    "HVAC marketing that survives the <em>shoulder seasons.</em>",
    "Emergency calls in January are easy. We build the system that keeps trucks rolling in April and October too.",
    [("Feast and famine", "Slammed in heat waves and cold snaps, quiet in between — and marketplace leads dry up exactly when you need them."),
     ("Shared leads", "The same furnace-repair homeowner sold to five HVAC companies. You win on price or not at all."),
     ("Missed calls in season", "When you're busiest is when the most calls go unanswered — peak season is your biggest leak.")],
    [("$60–120", "typical HVAC lead cost on LSA — manageable, disputable"),
     ("$105", "average HVAC lead cost across channels"),
     ("30–60%", "of in-season calls go unanswered — text-back recovers a third or more")],
    [("Do you understand HVAC seasonality?", "It's the core of the plan: reactivation campaigns before shoulder seasons (tune-up offers to your own customer list), ads weighted to weather, and SEO that compounds year-round."),
     ("We already run LSA. Why do we need you?", "Unmanaged LSA bleeds: undisputed junk leads, wrong categories, no review velocity feeding the ranking. Management pays for itself in disputes alone, usually."),
     ("How fast until the phone rings?", "Reactivation: ~30 days. LSA/ads: first week. Map pack: 60–90 days and then it compounds. We sequence them in that order.")])

trade_page("plumber-marketing.html", "Plumbing",
    "Plumbing marketing for the <em>2 a.m. emergency.</em>",
    "Burst pipes don't browse. They call the first plumber Google shows — we make sure that's you.",
    [("Emergency = top 3 or nothing", "A flooding basement doesn't scroll to page two. If you're not in the map pack, the job goes to whoever is."),
     ("Voicemail loses jobs", "85% of emergency callers won't leave a message — they dial the next plumber on the list."),
     ("Reviews decide ties", "Two plumbers, same distance: the one with 150 reviews beats the one with 30, every time.")],
    [("Top 3", "map results take the emergency call"), ("85%", "of callers won't leave a voicemail"), ("$50–60", "per call from managed search ads")],
    [("We get most work from word of mouth. Why change?", "Don't change it — back it up. Referrals are gold but unpredictable; the map pack and text-back catch everything referrals miss, especially emergencies from people who don't know you yet."),
     ("Can you guarantee #1 on Google?", "No, and nobody honest can. We guarantee transparent rank tracking, the proven inputs (GBP, reviews, pages), and reporting that shows exactly where you stand."),
     ("What does the first 90 days look like?", "Audit → text-back live in week one (stops the bleeding) → GBP rebuilt → review engine on → service-area pages shipping monthly. You see calls tracked from day one.")])

trade_page("electrician-marketing.html", "Electrical",
    "Electrician marketing beyond the <em>panel upgrade.</em>",
    "From service calls to EV chargers — own the searches that match the work you actually want.",
    [("Low-value service calls", "The phone rings, but for $150 jobs — while panel upgrades and EV charger installs go to competitors who rank for them."),
     ("Invisible for the good keywords", "'EV charger installation Ottawa' is a high-ticket search you can own — almost nobody has."),
     ("Quotes that vanish", "You quote the rewire, they 'think about it', and nobody ever follows up. That's not lost — that's unfinished.")],
    [("EV + heat pumps", "fast-growing high-ticket searches in Ottawa"), ("5+", "contacts needed to close bigger jobs"), ("<60s", "our speed-to-lead response on quote requests")],
    [("Can you target only the work I want?", "Yes — that's the point of keyword-level control. We weight EV chargers, panels and renovations over $99 service calls, or whatever your ideal mix is."),
     ("I'm a small shop. Is this overkill?", "The Lead Engine at $1,495 is sized exactly for owner-run shops. One panel upgrade a month covers it."),
     ("What about Gatineau/French?", "We serve English-side Ottawa today and say so honestly — bilingual coverage is on our roadmap, and we'll tell you if a competitor fits the Quebec side better right now.")])

trade_page("renovation-marketing.html", "Renovation",
    "Renovation marketing for <em>project pipelines.</em>",
    "Big tickets, long sales cycles, feast-and-famine pipelines. We build the system that keeps the next project always lined up.",
    [("The gap between projects", "A $80k kitchen ends and the pipeline is empty — because nobody marketed while everyone was building."),
     ("Portfolio stuck on your phone", "Your best sales tool is 400 job photos nobody ever sees. Homeowners hire what they can see."),
     ("6-week decision cycles", "Reno clients research for weeks. Without nurture, they forget you long before they sign with someone.")],
    [("$15k–150k", "typical project values — one job pays for years of marketing"), ("6+ weeks", "typical decision cycle — nurture wins it"), ("3×", "more quote requests from portfolio-led sites")],
    [("Our work comes from referrals and Houzz.", "Keep both. We add the searchers who don't know you yet — and the nurture sequences that keep 6-week deciders warm until they sign."),
     ("Can you photograph our projects?", "Yes — media production is in-house: job-site photo/video days at $495, woven into your site, GBP and social."),
     ("How do you handle long sales cycles?", "Email/SMS nurture built for renovation timelines: project galleries, financing info, checklists — staying helpful, not annoying, for the full 6 weeks.")])

# ============================================================ TORONTO (Phase 3)
tor_body = phero("Toronto / GTA", "Now booking GTA trades — <em>remotely, transparently.</em>",
    "The same Ottawa-proven system — local SEO, ads, and follow-up automation — delivered to Toronto contractors with the same three guarantees.", "Toronto")
tor_body += """
<section><div class="wrap"><div class="grid2" style="gap:60px;align-items:start">
<div class="prose">
  <h2 style="margin-top:0">Why GTA contractors work with an Ottawa agency</h2>
  <p>Because everything we deliver — rankings, ads, automation, reporting — is digital, tracked, and yours to verify daily. Distance changes nothing except the trade-show schedule. And our one-client-per-trade rule means your slot in Toronto is exclusively yours: something the big national agencies structurally cannot promise.</p>
  <ul class="checks">
    <li>Audit and strategy by video call — same 10 checks, same recorded walkthrough</li>
    <li>GTA-specific keyword and competitor research (we publish our Toronto lead-cost data on the blog)</li>
    <li>Quarterly in-person: GTA trade shows and client visits</li>
    <li>Same published pricing, +GTA market adjustment where ad costs demand it — always quoted upfront</li>
  </ul>
</div>
<div>
  <div class="card dark" style="margin-bottom:18px"><span class="badge">EXCLUSIVITY</span><h3>One HVAC company. One plumber. One electrician. One renovator.</h3><p>Per city. First come, first served — when your trade's Toronto slot is taken, it's taken.</p></div>
  <div class="card"><h3>Check your trade's availability</h3><p>Request the free audit and mention Toronto — we'll confirm whether your slot is open before anything else.</p><a class="btn" style="margin-top:10px" href="free-audit.html">Check availability</a></div>
</div>
</div></div></section>""" + CTA
page("toronto.html", "Contractor Marketing Toronto | Packed Agency", "Ottawa-proven contractor marketing for GTA trades: local SEO, ads, follow-up automation. One client per trade.", "", tor_body)

# ============================================================ RESOURCES (free learning hub)
res_body = phero("Free learning — no email wall", "The Contractor's <em>Marketing School.</em>",
    "Everything below is free, specific, and usable today — the same playbooks we charge for, taught in public. Steal it all.", "Free Resources")
res_body += """
<section><div class="wrap">

  <div class="kicker">Lesson 1</div>
  <h2 class="sec-h2" style="font-size:28px">The 10-minute Google Business Profile fix</h2>
  <p class="sec-sub" style="margin-bottom:18px">Your GBP drives more calls than your website. Most trades have it 30% filled. Do these today:</p>
  <ul class="checks" style="max-width:760px">
    <li>Pick your <b>primary category</b> precisely ("Plumber", not "Contractor") — it is the single biggest ranking lever</li>
    <li>Add every service you offer as a separate service item, with a sentence each</li>
    <li>Upload 10+ real job photos (trucks, crews, finished work) — phone photos beat stock, always</li>
    <li>Set service areas to the neighbourhoods you actually want jobs in</li>
    <li>Answer the Q&amp;A section yourself before strangers do</li>
    <li>Post once a week — a finished job with one photo counts</li>
  </ul>

  <div class="kicker" style="margin-top:56px">Lesson 2</div>
  <h2 class="sec-h2" style="font-size:28px">The review playbook that actually works</h2>
  <p class="sec-sub" style="margin-bottom:18px">Reviews decide ties in the map pack. The trick isn't asking — it's <i>when</i> and <i>how</i>:</p>
  <ul class="checks" style="max-width:760px">
    <li>Ask at the <b>moment of thanks</b> — when the customer says "this is great", that's the window</li>
    <li>Send the direct review link by text within 10 minutes (search "Google review link generator" — it's free)</li>
    <li>Aim for velocity, not volume: 2–3 fresh reviews a month beats 50 old ones</li>
    <li>Reply to every review, including the bad ones — replies are ranking signals and trust signals</li>
    <li>Never buy reviews. Google's filters catch them and the penalty outlasts the boost</li>
  </ul>

  <div class="kicker" style="margin-top:56px">Lesson 3</div>
  <h2 class="sec-h2" style="font-size:28px">7 reasons contractor websites never ring</h2>
  <ul class="checks" style="max-width:760px">
    <li>Phone number not clickable on mobile (60%+ of your visitors are on phones)</li>
    <li>No quote form above the fold — visitors won't scroll to find it</li>
    <li>Slow loading: every extra second loses visitors before they see anything</li>
    <li>Stock photos instead of your real trucks and crews — homeowners can smell it</li>
    <li>No reviews or proof on the page itself</li>
    <li>One generic page instead of a page per service and area</li>
    <li>No follow-up when someone does fill the form (see Lesson 4)</li>
  </ul>

  <div class="kicker" style="margin-top:56px">Lesson 4</div>
  <h2 class="sec-h2" style="font-size:28px">Follow-up: where the money actually leaks</h2>
  <p class="sec-sub" style="margin-bottom:18px">The stats that should change how you run your phone:</p>
  <ul class="checks" style="max-width:760px">
    <li><b>80% of sales take 5+ contacts</b> — most contractors stop at one</li>
    <li><b>85% of callers who hit voicemail don't leave a message</b> — they call the next name on Google</li>
    <li>Free fix #1: a text auto-reply on your business line ("Sorry we missed you — text us the job details")</li>
    <li>Free fix #2: a 5-minute end-of-day rule — every missed call and quote gets one text before you go home</li>
    <li>Free fix #3: a "quote sent" reminder 3 days later. One text. Most competitors never send it</li>
    <li>Want your number? The <a href="calculator.html" style="color:var(--orange);font-weight:700">Missed-Call Calculator</a> takes 20 seconds</li>
  </ul>

  <div class="kicker" style="margin-top:56px">Lesson 5</div>
  <h2 class="sec-h2" style="font-size:28px">What leads should cost (so nobody rips you off)</h2>
  <table class="cb" style="max-width:820px"><tr><th>Channel</th><th>Honest benchmark</th></tr>
    <tr><td>Google Local Services Ads (HVAC)</td><td>$60–120 per lead — disputable if junk</td></tr>
    <tr><td>Google Search ads (managed)</td><td>~$50–60 per call, ~55% close</td></tr>
    <tr><td>Home-services average</td><td>~$91 per lead; roofing up to ~$228</td></tr>
    <tr><td>Shared marketplaces (HomeStars/Angi)</td><td>Similar sticker — but sold to up to 5 competitors</td></tr>
    <tr><td>Map pack (local SEO)</td><td>~40% lower cost-per-sale than ads once ranked</td></tr></table>
  <p class="sec-sub" style="margin-top:14px">If someone quotes you far outside these ranges, ask why — and make them answer in numbers.</p>

  <div class="note" style="max-width:820px;margin-top:50px"><b>Why we give this away:</b> teaching is our marketing. If you do all of this yourself, genuinely — good, your schedule gets fuller and you'll tell other trades who taught you. If you'd rather be on the tools than on Google, that's what <a href="services.html" style="color:var(--orange);font-weight:700">we're for</a>.</p></div>
  <p style="margin-top:26px"><a class="btn" href="blog.html">More lessons on the blog</a>&nbsp;&nbsp;<a class="btn navy" href="free-audit.html">Or get the free audit</a></p>
</div></section>"""
page("resources.html", "Free Marketing Resources for Contractors | Packed Agency",
     "Free contractor marketing lessons: Google Business Profile fixes, review playbook, website checklist, follow-up tactics and honest lead-cost benchmarks.", "resources", res_body)

# ============================================================ PRIVACY & TERMS
priv_body = phero("Legal", "Privacy <em>Policy.</em>", "Plain-language, CASL-aware. Have a lawyer review before launch.", "Privacy")
priv_body += """
<section><div class="wrap prose">
<div class="note"><b>Template notice:</b> this is a working draft for launch. Have it reviewed by a lawyer, and replace the bracketed items.</div>
<h2>Who we are</h2><p>Packed Agency ("we") is a marketing services business operated by [legal name], Ottawa, Ontario. Contact: """ + EMAIL + """.</p>
<h2>What we collect</h2><p>Information you submit through our forms (name, company, trade, phone, email), call recordings on tracked numbers (announced where required), and standard analytics (GA4) about site usage.</p>
<h2>How we use it</h2><p>To deliver the audit or services you requested, to respond to enquiries, and — only with your express consent (CASL) — to send commercial electronic messages. Every message includes an unsubscribe that works.</p>
<h2>What we never do</h2><p>Sell, rent or trade your information. Ever.</p>
<h2>Storage &amp; access</h2><p>Data is stored in our CRM (GoHighLevel) and analytics tools. You may request a copy or deletion of your data at any time via """ + EMAIL + """.</p>
<h2>Cookies</h2><p>We use analytics and advertising cookies (GA4, Meta Pixel). You can block cookies in your browser without losing access to this site.</p>
<p><i>Last updated: [date]. Questions: """ + EMAIL + """.</i></p>
</div></section>"""
page("privacy.html", "Privacy Policy | Packed Agency", "Packed Agency privacy policy — CASL-aware, plain language.", "", priv_body)

terms_body = phero("Legal", "Terms of <em>Service.</em>", "The short, fair version. Full service terms live in your signed agreement.", "Terms")
terms_body += """
<section><div class="wrap prose">
<div class="note"><b>Template notice:</b> working draft — lawyer review before launch.</div>
<h2>Site use</h2><p>Content on this site is provided for information. Benchmarks cited are from published industry sources and your results will vary with market, budget and execution.</p>
<h2>Service terms (summary)</h2><p>Services are governed by a signed agreement which includes our three guarantees: client ownership of all assets, 90-day initial term then month-to-month, and one-client-per-trade-per-city exclusivity. The agreement prevails over this summary.</p>
<h2>No guarantees of outcomes</h2><p>We do not guarantee specific rankings, lead volumes or revenue — and we put that in writing because honest expectations are part of the product.</p>
<h2>Liability</h2><p>To the maximum extent permitted by law, our liability is limited to fees paid in the three months preceding a claim.</p>
<p><i>Last updated: [date].</i></p>
</div></section>"""
page("terms.html", "Terms | Packed Agency", "Packed Agency terms of service.", "", terms_body)

# ============================================================ 404
nf_body = phero("404", "This page is <em>not packed.</em>",
    "The page you were looking for does not exist — but your schedule can still be. Try one of these instead.")
nf_body += """
<section><div class="wrap"><div class="grid3">
  <a class="card" href="index.html"><h3>Home</h3><p>Start from the top.</p></a>
  <a class="card" href="pricing.html"><h3>Pricing</h3><p>Real published prices.</p></a>
  <a class="card" href="free-audit.html"><h3>Free Audit</h3><p>The 30-second form.</p></a>
</div></div></section>"""
page("404.html", "Page Not Found | Packed Agency", "That page does not exist.", "", nf_body)

# ============================================================ SEO files
today = datetime.date.today().isoformat()
prio = lambda f: "1.0" if f == "index.html" else ("0.3" if f in ("privacy.html", "terms.html") else "0.8")
sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for f in PAGES:
    if f == "404.html":
        continue
    loc = BASE + ("" if f == "index.html" else f)
    sm += "  <url><loc>" + loc + "</loc><lastmod>" + today + "</lastmod><priority>" + prio(f) + "</priority></url>\n"
sm += "</urlset>\n"
open(os.path.join(OUT, "sitemap.xml"), "w").write(sm)
robots = "User-agent: *\nAllow: /\n\n"
for bot in ("GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "Claude-Web", "anthropic-ai", "PerplexityBot", "Google-Extended", "Applebot-Extended", "Bytespider", "CCBot", "meta-externalagent"):
    robots += "User-agent: " + bot + "\nAllow: /\n\n"
robots += "Sitemap: " + BASE + "sitemap.xml\n"
open(os.path.join(OUT, "robots.txt"), "w").write(robots)
LLMS = """# Packed Agency

> Founder-led digital marketing agency for contractors and home-service companies (HVAC, plumbing, electrical, renovation/general contracting) in Ottawa, Canada, expanding to Toronto/GTA. We keep contractors' schedules packed: Google Maps/local SEO, Google Ads & Local Services Ads, conversion websites, and follow-up automation (missed-call text-back, instant lead response, customer win-back campaigns).

Key facts:
- Location: 500 Preston St, Ottawa, ON, Canada. Phone: 343-558-5062. Email: info@packedagency.ca
- Published pricing (rare in this industry): Door-Opener $749 one-time; Conversion Website $3,950 one-time; Lead Engine $1,495/month; Growth $2,950/month + ad spend
- Three contract guarantees: the client owns every asset (website, ad accounts, data); no lock-in after a 90-day initial term; one client per trade per city (market exclusivity)
- Unique service in this market: follow-up automation (missed-call text-back, sub-60-second lead response, database reactivation) - confirmed unavailable from local competitors
- Founder: Sajad, 8+ years of marketing experience; clients talk directly to the person doing the work

## Main pages
- [Pricing](https://packedagency.ca/pricing.html): full transparent price list
- [Free Schedule Audit](https://packedagency.ca/free-audit.html): free 10-point marketing checkup with recorded video, no obligation
- [Services overview](https://packedagency.ca/services.html)
- [Follow-up automation](https://packedagency.ca/automation.html): the flagship differentiator
- [Guarantees](https://packedagency.ca/guarantees.html): contract-language promises
- [Free contractor marketing lessons](https://packedagency.ca/resources.html): Google Business Profile fixes, review playbook, lead-cost benchmarks - free, no email wall
- [HVAC marketing](https://packedagency.ca/hvac-marketing.html), [Plumber marketing](https://packedagency.ca/plumber-marketing.html), [Electrician marketing](https://packedagency.ca/electrician-marketing.html), [Renovation marketing](https://packedagency.ca/renovation-marketing.html)
- [Toronto/GTA](https://packedagency.ca/toronto.html)
- [Blog](https://packedagency.ca/blog.html): Ottawa-specific lead-cost benchmarks and contractor marketing data

## Benchmarks we publish (sources cited on site)
- HVAC lead cost on Google LSA: $60-120; average across channels ~$105
- Managed Google Search ads: ~$50-60 per call, ~55% close rate
- Top-3 Google Maps placement: ~40% lower cost-per-sale than paid ads
- 80% of sales take 5+ contacts; 85% of callers who reach voicemail do not leave a message
"""
open(os.path.join(OUT, "llms.txt"), "w").write(LLMS)
print("wrote robots.txt + llms.txt")
os.makedirs(os.path.join(OUT, "assets"), exist_ok=True)
open(os.path.join(OUT, "assets", "favicon.svg"), "w").write(LOGO_SVG.replace(' aria-hidden="true"', ""))
print("wrote sitemap.xml, robots.txt, favicon.svg")

# ============================================================ style.css
with open(os.path.join(OUT, "style.css"), "w") as f:
    f.write(CSS)
print("wrote style.css")
print("DONE —", len(os.listdir(OUT)), "files in", OUT)
