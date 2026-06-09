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
.todo-box{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:8px 22px 16px;margin:26px 0}
.todo-head{display:flex;justify-content:space-between;align-items:center;padding:14px 0;border-bottom:1px solid var(--line);font-family:'Archivo',sans-serif;font-weight:700}
.todo-score{color:var(--orange);font-weight:800;font-size:15px}
.todo{display:flex;gap:14px;align-items:flex-start;padding:13px 0;border-bottom:1px solid var(--line);cursor:pointer;font-size:15.5px}
.todo:last-of-type{border-bottom:none}
.todo input{width:21px;height:21px;min-width:21px;margin-top:2px;accent-color:var(--orange);cursor:pointer}
.todo input:checked+span{color:var(--grey);text-decoration:line-through;text-decoration-color:rgba(249,115,22,.6)}
.todo-msg{padding-top:12px;color:var(--grey);font-size:13.5px}
.ic{width:44px;height:44px;border-radius:10px;background:rgba(249,115,22,.13);display:flex;align-items:center;justify-content:center;margin-bottom:14px;color:var(--orange)}
.ic svg{width:22px;height:22px}
.chip{display:inline-block;background:var(--card);border:1px solid var(--line);color:#DDE4F0;padding:8px 15px;border-radius:99px;font-size:12.5px;font-weight:600;margin:0 8px 10px 0}
.chip b{color:var(--orange)}
.chip:hover{border-color:rgba(249,115,22,.6)}
.chooser{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-top:8px}
.choose{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:26px 20px;text-align:center;transition:.16s;display:block}
.choose:hover{border-color:var(--orange);transform:translateY(-3px)}
.choose .ci{width:54px;height:54px;border-radius:14px;background:rgba(249,115,22,.13);display:flex;align-items:center;justify-content:center;margin:0 auto 14px;color:var(--orange)}
.choose .ci svg{width:27px;height:27px}
.choose h3{font-size:16px;color:#fff;margin-bottom:6px}
.choose p{font-size:13px;color:var(--grey);margin-bottom:10px;line-height:1.5}
.choose .go{color:var(--orange);font-weight:700;font-size:13px}
.cardico{width:46px;height:46px;border-radius:11px;background:rgba(249,115,22,.13);display:flex;align-items:center;justify-content:center;margin-bottom:16px;color:var(--orange)}
.cardico svg{width:23px;height:23px}
.card.dark .cardico{background:rgba(249,115,22,.2)}
.pill-ico{width:46px;height:46px;border-radius:11px;background:rgba(249,115,22,.16);display:flex;align-items:center;justify-content:center;margin-bottom:16px;color:var(--orange)}
.pill-ico svg{width:23px;height:23px}
@media(max-width:760px){.chooser{grid-template-columns:1fr 1fr}}
@media(max-width:430px){.chooser{grid-template-columns:1fr}}
.svcgrid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-top:8px}
.svc{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:22px;display:flex;flex-direction:column}
.svc .si{width:44px;height:44px;border-radius:11px;background:rgba(249,115,22,.13);display:flex;align-items:center;justify-content:center;color:var(--orange);margin-bottom:14px}
.svc .si svg{width:22px;height:22px}
.svc h4{font-size:16px;color:#fff;margin-bottom:6px;font-family:'Archivo',sans-serif}
.svc p{font-size:13px;color:var(--grey);line-height:1.5;flex:1;margin-bottom:14px}
.svc .pr{font-family:'Archivo',sans-serif;font-weight:900;font-size:22px;color:#fff}
.svc .pr small{font-size:12px;color:var(--grey);font-weight:500;display:block;margin-top:2px}
.svc.feat{border-color:rgba(249,115,22,.5)}
@media(max-width:760px){.svcgrid{grid-template-columns:1fr 1fr}}
@media(max-width:480px){.svcgrid{grid-template-columns:1fr}}
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
        "<a class=\"nav-phone\" href=\"https://calendar.app.google/s2etv2aRyPFDhRZm7\" target=\"_blank\" rel=\"noopener\">Book a call</a>"
        "<a class=\"btn\" href=\"free-audit.html\">Get Free Audit</a></nav>"
        "<button class=\"burger\" onclick=\"document.getElementById('navLinks').classList.toggle('open')\">&#9776;</button>"
        "</div></header>\n")

FORM_JS = """<script>
function pkLower(f){var e=f.querySelector("input[name=email]");return e?e.value.trim().toLowerCase():"";}
function pkSeen(type,email){try{var k="pk_"+type;var list=JSON.parse(localStorage.getItem(k)||"[]");return email&&list.indexOf(email)>-1;}catch(e){return false;}}
function pkMark(type,email){try{var k="pk_"+type;var list=JSON.parse(localStorage.getItem(k)||"[]");if(email&&list.indexOf(email)<0){list.push(email);localStorage.setItem(k,JSON.stringify(list));}}catch(e){}}
function pkDoneBox(f,title,msg){f.innerHTML="<div style='padding:24px 6px;text-align:center'><div style='font-family:Archivo,sans-serif;font-weight:900;font-size:21px;color:#fff'>"+title+"</div><p style='color:#9AA4B4;margin-top:10px;font-size:14.5px'>"+msg+"</p></div>";}
function wireForm(id,evt,msg){
  var f=document.getElementById(id);if(!f)return;
  f.addEventListener("submit",function(e){
    e.preventDefault();
    var email=pkLower(f);
    if(pkSeen(evt,email)){pkDoneBox(f,"You're already on our list. \u2713","Looks like you already reached out with this email &mdash; no need to send it twice. We'll get back to you soon. Need it faster? Call or text 343-558-5062.");return;}
    var btn=f.querySelector("button[type=submit]"),orig=btn.textContent;
    btn.disabled=true;btn.textContent="Sending...";
    fetch("https://api.web3forms.com/submit",{method:"POST",headers:{"Content-Type":"application/json",Accept:"application/json"},body:JSON.stringify(Object.fromEntries(new FormData(f)))})
    .then(function(r){return r.json()})
    .then(function(d){
      if(d.success){
        f.innerHTML="<div style='padding:26px 6px;text-align:center'><div style='font-family:Archivo,sans-serif;font-weight:900;font-size:22px;color:#fff'>Got it. &#10003;</div><p style='color:#9AA4B4;margin-top:10px;font-size:14.5px'>"+msg+"</p></div>";
        pkMark(evt,email);if(window.gtag)gtag("event",evt);
      }else{btn.disabled=false;btn.textContent=orig;alert("Something went wrong - please call or text 343-558-5062.");}
    })
    .catch(function(){btn.disabled=false;btn.textContent=orig;alert("Something went wrong - please call or text 343-558-5062.");});
  });
}
wireForm("auditForm","lead_audit","Your audit is on the way - we will text or call within one business day, and the video lands within two.");
wireForm("contactForm","lead_contact","Message received - we reply within one business day.");
document.querySelectorAll(".mg-form").forEach(function(f){
  f.addEventListener("submit",function(e){
    e.preventDefault();
    var email=pkLower(f);
    if(pkSeen("magnet_download",email)){f.innerHTML="<a class='btn' style='width:100%;text-align:center' href='assets/packed-contractor-marketing-checklist.pdf' download>Download the checklist (PDF) &#8595;</a><p class='fine' style='margin-top:8px;color:#9AA4B4'>You already grabbed this &mdash; here it is again. Check your inbox for the bulletin.</p>";return;}
    var btn=f.querySelector("button"),orig=btn.textContent;btn.disabled=true;btn.textContent="...";
    fetch("https://api.web3forms.com/submit",{method:"POST",headers:{"Content-Type":"application/json",Accept:"application/json"},body:JSON.stringify(Object.fromEntries(new FormData(f)))})
    .then(function(r){return r.json()}).then(function(d){
      if(d.success){f.innerHTML="<a class='btn' style='width:100%;text-align:center' href='assets/packed-contractor-marketing-checklist.pdf' download>Download the checklist (PDF) &#8595;</a><p class='fine' style='margin-top:8px;color:#9AA4B4'>It's yours. The monthly bulletin lands in your inbox too.</p>";pkMark("magnet_download",email);if(window.gtag)gtag("event","magnet_download");}
      else{btn.disabled=false;btn.textContent=orig;}
    }).catch(function(){btn.disabled=false;btn.textContent=orig;});
  });
});
document.querySelectorAll(".nl-form").forEach(function(f){
  f.addEventListener("submit",function(e){
    e.preventDefault();
    var email=pkLower(f);
    if(pkSeen("newsletter_signup",email)){f.innerHTML="<p style='font-family:Archivo,sans-serif;font-weight:900;color:#fff;font-size:16px;padding:10px 0'>You're already subscribed. \u2713<br><span style='font-weight:400;font-size:13.5px;color:#9AA4B4'>No need to sign up twice &mdash; the next bulletin is on its way.</span></p>";return;}
    var btn=f.querySelector("button"),orig=btn.textContent;btn.disabled=true;btn.textContent="...";
    fetch("https://api.web3forms.com/submit",{method:"POST",headers:{"Content-Type":"application/json",Accept:"application/json"},body:JSON.stringify(Object.fromEntries(new FormData(f)))})
    .then(function(r){return r.json()}).then(function(d){
      if(d.success){f.innerHTML="<p style='font-family:Archivo,sans-serif;font-weight:900;color:#fff;font-size:17px;padding:10px 0'>You're in. &#10003; First bulletin lands next month.</p>";pkMark("newsletter_signup",email);if(window.gtag)gtag("event","newsletter_signup");}
      else{btn.disabled=false;btn.textContent=orig;}
    }).catch(function(){btn.disabled=false;btn.textContent=orig;});
  });
});
document.querySelectorAll(".todo-box").forEach(function(box){
  var cbs=box.querySelectorAll("input[type=checkbox]"),sc=box.querySelector("[data-score]"),msg=box.querySelector("[data-msg]");
  function upd(){var n=0;cbs.forEach(function(c){if(c.checked)n++});sc.textContent=n+" / "+cbs.length+" done";
    if(n===cbs.length){msg.innerHTML="All boxes ticked? You're ahead of 90% of contractors. The <a href='free-audit.html' style='color:#F97316;font-weight:700'>free audit</a> finds what checklists can't.";}
    else{msg.textContent="Tick what you've already done - every empty box is costing you calls. "+(cbs.length-n)+" to go.";}}
  cbs.forEach(function(c){c.addEventListener("change",upd)});upd();
});
</script>
"""

FOOTER = ("<footer class=\"site\"><div class=\"wrap\"><div class=\"f-grid\">"
    "<div><div class=\"logo\" style=\"margin-bottom:14px\">" + LOGO_SVG + "<div style=\"color:#fff\"><b style=\"color:#fff\">PACKED</b><span>AGENCY</span></div></div>"
    "<p style=\"font-size:14px;max-width:300px\">We keep your schedule packed. Marketing, exclusive leads and follow-up automation for Canada's trades. Ottawa-built.</p></div>"
    "<div><h4>Services</h4><a href=\"local-seo.html\">Local SEO &amp; Maps</a><a href=\"google-ads.html\">Google Ads &amp; LSA</a><a href=\"websites.html\">Conversion Websites</a><a href=\"automation.html\">Follow-up Automation</a><a href=\"calculator.html\">Missed-Call Calculator</a></div>"
    "<div><h4>Trades</h4><a href=\"hvac-marketing.html\">HVAC Marketing</a><a href=\"plumber-marketing.html\">Plumber Marketing</a><a href=\"electrician-marketing.html\">Electrician Marketing</a><a href=\"renovation-marketing.html\">Renovation Marketing</a><a href=\"toronto.html\">Toronto</a></div>"
    "<div><h4>Company</h4><a href=\"process.html\">Our Process</a><a href=\"resources.html\">Free Resources</a><a href=\"events.html\">Events</a><a href=\"news.html\">Trade News</a><a href=\"guarantees.html\">Guarantees</a><a href=\"results.html\">Results</a><a href=\"reviews.html\">Reviews</a><a href=\"blog.html\">Blog</a><a href=\"contact.html\">Contact</a></div>"
    "</div><div class=\"f-bottom\"><span>&copy; 2026 Packed Agency. All rights reserved.</span>"
    "<span><a href=\"privacy.html\">Privacy Policy</a> &nbsp;&middot;&nbsp; <a href=\"terms.html\">Terms</a> &nbsp;&middot;&nbsp; Client Portal (coming soon)</span></div></div></footer>\n"
    "<a class=\"callbar\" href=\"https://calendar.app.google/s2etv2aRyPFDhRZm7\" target=\"_blank\" rel=\"noopener\">&#128197; Book a free 30-min call</a>\n" + FORM_JS + "</body>\n</html>")

def phero(kicker, h1, lead, crumb=""):
    c = ("<div class=\"crumb\"><a href=\"index.html\">Home</a> / " + crumb + "</div>") if crumb else ""
    return ("<section class=\"phero\"><div class=\"bgfx\"></div><div class=\"wrap\">" + c +
        "<div class=\"kicker\">" + kicker + "</div><h1>" + h1 + "</h1>"
        "<p class=\"lead\">" + lead + "</p>"
        "<a class=\"btn\" href=\"free-audit.html\">Get My Free Audit</a></div></section>\n")

CTA = ("<section class=\"ctaband\"><div class=\"wrap\"><h2>Ready for a packed schedule?</h2>"
    "<p>Start with the free audit &mdash; we check your Google listing, website and phones, then send you a 10-minute video of what we found. No pressure, no cost.</p>"
    "<a class=\"btn\" href=\"free-audit.html\">Get My Free Audit</a>&nbsp;&nbsp;"
    "<a class=\"btn ghost\" href=\"https://calendar.app.google/s2etv2aRyPFDhRZm7\" target=\"_blank\" rel=\"noopener\">Book a 30-min call</a>"
    "<p style=\"margin:18px 0 0;font-size:14px;color:#8B95A5\">Or text us anytime at <a href=\"" + TEL + "\" style=\"color:#fff;font-weight:600\">" + PHONE + "</a></p></div></section>\n")

NEWSLETTER = """
<div style="background:var(--card);border:1px solid rgba(249,115,22,.35);border-radius:14px;padding:30px;max-width:860px;margin:50px auto 0">
  <div style="display:flex;gap:18px;align-items:flex-start;flex-wrap:wrap">
    <div style="flex:1;min-width:240px">
      <div class="kicker" style="margin-bottom:8px">The Packed Bulletin</div>
      <h3 style="font-size:20px;color:#fff;margin-bottom:6px">One email a month. Worth opening.</h3>
      <p style="color:var(--grey);font-size:14px">Rebates, Google rule changes, lead-cost data and one tactic to try — in plain English, for Ottawa trades. No spam, unsubscribe anytime.</p>
    </div>
    <form class="nl-form" style="flex:1;min-width:260px;display:flex;gap:10px;flex-wrap:wrap;align-items:flex-start;margin-top:6px">
      <input type="hidden" name="access_key" value="9aac958d-5965-4b75-8736-b6ab7274db68">
      <input type="hidden" name="subject" value="NEWSLETTER SIGNUP (packedagency.ca)">
      <input type="hidden" name="from_name" value="Packed Agency Website">
      <input type="checkbox" name="botcheck" style="display:none" tabindex="-1" autocomplete="off">
      <input type="email" name="email" placeholder="you@yourcompany.ca" required style="flex:1;min-width:180px;padding:13px 14px;border:1px solid rgba(255,255,255,.14);border-radius:8px;font-size:15px;background:#0A0E14;color:var(--ink)">
      <button class="btn" type="submit" style="padding:13px 22px;font-size:14.5px">Sign me up</button>
      <p class="fine" style="width:100%;margin:2px 0 0;font-size:11.5px;color:var(--grey)">CASL consent: you agree to receive our monthly email. Unsubscribe in one click, anytime.</p>
    </form>
  </div>
</div>"""

MAGNET = """
<div style="background:linear-gradient(135deg,#1C140A,#151C27);border:1px solid rgba(249,115,22,.45);border-radius:16px;padding:34px;max-width:1000px;margin:0 auto 56px">
  <div style="display:flex;gap:26px;align-items:center;flex-wrap:wrap">
    <div style="flex:1.4;min-width:260px">
      <span class="badge">FREE DOWNLOAD</span>
      <h3 style="font-size:24px;color:#fff;margin:8px 0 8px">The Ottawa Contractor&rsquo;s Marketing Checklist</h3>
      <p style="color:var(--grey);font-size:15px">All 5 playbooks as one printable PDF — 34 tick-boxes covering your Google listing, reviews, website, follow-up and lead costs. Pin it to the shop wall.</p>
    </div>
    <form class="mg-form" style="flex:1;min-width:260px">
      <input type="hidden" name="access_key" value="9aac958d-5965-4b75-8736-b6ab7274db68">
      <input type="hidden" name="subject" value="CHECKLIST DOWNLOAD (packedagency.ca)">
      <input type="hidden" name="from_name" value="Packed Agency Website">
      <input type="checkbox" name="botcheck" style="display:none" tabindex="-1" autocomplete="off">
      <input type="email" name="email" placeholder="you@yourcompany.ca" required style="width:100%;padding:13px 14px;border:1px solid rgba(255,255,255,.14);border-radius:8px;font-size:15px;background:#0A0E14;color:var(--ink);margin-bottom:10px">
      <button class="btn" type="submit" style="width:100%">Send me the checklist (PDF)</button>
      <p class="fine" style="margin-top:8px;font-size:11.5px;color:var(--grey)">Instant download. CASL consent: you&rsquo;ll also get our monthly bulletin — unsubscribe anytime.</p>
    </form>
  </div>
</div>"""


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
      <a class="btn ghost" href="https://calendar.app.google/s2etv2aRyPFDhRZm7" target="_blank" rel="noopener">Book a 30-min call</a>
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

<section style="background:var(--surface);border-top:1px solid var(--line)">
  <div class="wrap" style="text-align:center">
    <div class="kicker" style="justify-content:center">What do you need?</div>
    <h2 class="sec-h2">Tap the one that sounds like you.</h2>
    <p class="sec-sub" style="margin:0 auto 30px">We'll take you straight to the fix &mdash; no scrolling, no jargon.</p>
    <div class="chooser">
      <a class="choose" href="websites.html"><div class="ci"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="16" rx="2"/><line x1="3" y1="9" x2="21" y2="9"/><circle cx="6" cy="6.5" r=".6" fill="currentColor"/><circle cx="8.5" cy="6.5" r=".6" fill="currentColor"/></svg></div><h3>I need more work coming in</h3><p>Your website doesn't bring you jobs.</p><span class="go">Fix my website &rarr;</span></a>
      <a class="choose" href="local-seo.html"><div class="ci"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"><path d="M12 21s-7-5.6-7-11a7 7 0 0 1 14 0c0 5.4-7 11-7 11z"/><circle cx="12" cy="10" r="2.5"/></svg></div><h3>Nobody finds me on Google</h3><p>You're not in the map when people search.</p><span class="go">Get me found &rarr;</span></a>
      <a class="choose" href="automation.html"><div class="ci"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 2 .7 2.9a2 2 0 0 1-.5 2.1L8 10a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.5c.9.3 1.9.6 2.9.7a2 2 0 0 1 1.7 2z"/></svg></div><h3>Leads slip through the cracks</h3><p>Missed calls and quotes that go cold.</p><span class="go">Stop the leaks &rarr;</span></a>
      <a class="choose" href="free-audit.html"><div class="ci"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"><circle cx="12" cy="12" r="9.5"/><polygon points="16,8 13,13 8,16 11,11"/></svg></div><h3>I'm not sure what I need</h3><p>Get a free check-up first.</p><span class="go">Start free &rarr;</span></a>
    </div>
  </div>
</section>

<section style="background:var(--navy);color:#fff">
  <div class="wrap">
    <div class="kicker">Why "Packed"</div>
    <h2 class="sec-h2">Three things we keep packed.</h2>
    <div class="grid3" style="margin-top:40px">
      <div style="background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.1);border-radius:16px;padding:32px 28px"><div class="pill-ico"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="9" cy="8" r="3"/><path d="M3 20a6 6 0 0 1 12 0"/><path d="M16 5.5a3 3 0 0 1 0 5"/><path d="M18 14a6 6 0 0 1 3 6"/></svg></div><h3 style="font-size:21px;margin-bottom:10px">Packed Team</h3><p style="color:#B9C4D8;font-size:15px">Websites, SEO, ads, media and automation — delivered under one roof by the person you actually talk to. No hand-offs, no outsourcing.</p></div>
      <div style="background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.1);border-radius:16px;padding:32px 28px"><div class="pill-ico"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1.4" fill="currentColor"/></svg></div><h3 style="font-size:21px;margin-bottom:10px">Packed Focus</h3><p style="color:#B9C4D8;font-size:15px">Contractors and home services. Only. We know what an Ottawa HVAC lead costs and what homeowners type at 2 a.m. when the furnace dies.</p></div>
      <div style="background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.1);border-radius:16px;padding:32px 28px"><div class="pill-ico"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"><rect x="3" y="5" width="18" height="16" rx="2"/><line x1="3" y1="10" x2="21" y2="10"/><line x1="8" y1="3" x2="8" y2="7"/><line x1="16" y1="3" x2="16" y2="7"/><rect x="7" y="13" width="3" height="3" fill="currentColor" stroke="none"/></svg></div><h3 style="font-size:21px;margin-bottom:10px">Packed Schedule</h3><p style="color:#B9C4D8;font-size:15px">The only metric that matters: booked jobs on your calendar. Every report we send is written in jobs and dollars.</p></div>
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
      <a class="card" href="local-seo.html"><div class="cardico"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"><path d="M12 21s-7-5.6-7-11a7 7 0 0 1 14 0c0 5.4-7 11-7 11z"/><circle cx="12" cy="10" r="2.5"/></svg></div><span class="tag">Get Found</span><h3>Get Found on Google Maps</h3><p>When a homeowner searches &ldquo;plumber near me&rdquo;, the top 3 map results get the calls. We put you there — and keep you there.</p><div class="from">From $1,195/mo <small>· or inside the Lead Engine</small></div></a>
      <a class="card" href="google-ads.html"><div class="cardico"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 11v2a1 1 0 0 0 1 1h2l4 4V6L6 10H4a1 1 0 0 0-1 1z"/><path d="M15 9a3 3 0 0 1 0 6"/><path d="M18 6a7 7 0 0 1 0 12"/></svg></div><span class="tag">Get Leads</span><h3>Ads That Pay for Themselves</h3><p>Ads only on searches that mean money — emergencies and big jobs. About $50–60 per call, and you see every dollar spent.</p><div class="from">From $549/mo <small>· or 12% of ad spend</small></div></a>
      <a class="card" href="websites.html"><div class="cardico"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="16" rx="2"/><line x1="3" y1="9" x2="21" y2="9"/><circle cx="6" cy="6.5" r=".6" fill="currentColor"/><circle cx="8.5" cy="6.5" r=".6" fill="currentColor"/></svg></div><span class="tag">Get Hired</span><h3>A Website That Makes the Phone Ring</h3><p>Fast, simple, built for one job: turning visitors into calls. And it&rsquo;s yours — in writing.</p><div class="from">$2,950 <small>· one-time</small></div></a>
      <a class="card dark" href="automation.html"><div class="cardico"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M13 2 3.5 14H10l-1 8L19 10h-6.5L13 2z"/></svg></div><span class="badge">ONLY AT PACKED</span><h3>Never Miss Another Lead</h3><p>Miss a call on the roof? The customer gets a text back in seconds. Every quote gets followed up. Automatically.</p><div class="from" style="color:#fff">From $349/mo <small style="color:#B9C4D8">· setup $995</small></div></a>
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
    <img src="assets/founder-sajad.jpg" alt="Sajad — founder of Packed Agency" loading="lazy" width="1000" height="1000" style="width:100%;height:auto;border-radius:14px;border:1px solid var(--line)">
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

  <div class="kicker" style="text-align:center;justify-content:center">Two ways to buy</div>
  <h2 class="sec-h2" style="text-align:center">Pick one service, or the whole system.</h2>
  <p class="sec-sub" style="margin:0 auto 36px;text-align:center">Need just a website? Just Google rankings? Buy it on its own below. Want it all handled for one monthly price? Jump to the <a href="#plans" style="color:var(--orange);font-weight:700">managed plans</a>. Every price is published &mdash; no sales call to find out what it costs.</p>

  <div class="kicker">One-time projects</div>
  <h3 style="font-family:'Archivo',sans-serif;font-weight:900;font-size:24px;color:#fff;margin-bottom:6px">Pay once. You own it forever.</h3>
  <p class="sec-sub" style="margin-bottom:18px">For when you need a specific thing built &mdash; a website, a logo, a one-time campaign.</p>
  <div class="svcgrid"><div class="svc feat"><div class="si"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="16" rx="2"/><line x1="3" y1="9" x2="21" y2="9"/><circle cx="6" cy="6.5" r=".6" fill="currentColor"/><circle cx="8.5" cy="6.5" r=".6" fill="currentColor"/></svg></div><h4>Website</h4><p>5&ndash;10 page WordPress site, click-to-call, quote forms, mobile-fast. You own every file.</p><div class="pr">$2,950</div></div><div class="svc feat"><div class="si"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 13c-1.5 1.2-2 5-2 5s3.8-.5 5-2"/><path d="M14.5 4.5C18 6 19 9 19 12c0 2-1 4-3 6l-4-1-1-4c2-2 4-3 6-3 0-3-1.5-4.5-2.5-5.5z"/><circle cx="14.5" cy="9.5" r="1.5"/></svg></div><h4>Website + Launch Bundle</h4><p>Website <i>plus</i> Google Business Profile setup and a brand refresh. Best value of the three.</p><div class="pr">$3,950</div></div><div class="svc"><div class="si"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="8" cy="15" r="4"/><path d="M10.8 12.2 19 4"/><path d="M16 7l3 3"/><path d="M14 9l2 2"/></svg></div><h4>Door-Opener</h4><p>A fast first win &mdash; win-back campaign or Google listing overhaul. Booked jobs in ~30 days.</p><div class="pr">$749</div></div><div class="svc"><div class="si"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="16" rx="2"/><line x1="3" y1="9" x2="21" y2="9"/><line x1="9" y1="9" x2="9" y2="20"/></svg></div><h4>Extra landing page</h4><p>One focused page for a specific service or ad campaign.</p><div class="pr">$649</div></div><div class="svc"><div class="si"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M9 9h3.5a2.5 2.5 0 0 1 0 5H9zM9 9v8"/></svg></div><h4>Logo</h4><p>A clean, professional logo for your trucks, site and quotes.</p><div class="pr">$495</div></div><div class="svc"><div class="si"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"><path d="M12 3a9 9 0 0 0 0 18c1 0 1.5-.8 1.5-1.5 0-.4-.2-.8-.5-1-.3-.3-.5-.6-.5-1 0-.8.7-1.5 1.5-1.5H16a5 5 0 0 0 5-5c0-4.4-4-8-9-8z"/><circle cx="7.5" cy="11.5" r="1"/><circle cx="11" cy="7.5" r="1"/><circle cx="15.5" cy="9" r="1"/></svg></div><h4>Full brand kit</h4><p>Logo + colours + fonts + truck/uniform-ready files.</p><div class="pr">$1,250</div></div><div class="svc"><div class="si"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"><rect x="3" y="6" width="13" height="12" rx="2"/><path d="M16 10l5-3v10l-5-3z"/></svg></div><h4>Promo video</h4><p>A short, professional video for your site and social.</p><div class="pr">$1,450</div></div><div class="svc"><div class="si"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"><path d="M3 8a2 2 0 0 1 2-2h2l1.5-2h7L19 6h0a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><circle cx="12" cy="12.5" r="3.2"/></svg></div><h4>Job-site content day</h4><p>Half a day on site capturing real photos &amp; clips of your crew.</p><div class="pr">$495</div></div><div class="svc"><div class="si"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12a9 9 0 1 1-2.6-6.4"/><path d="M21 4v5h-5"/></svg></div><h4>Reactivation campaign</h4><p>One-time text/email push to past customers to fill a slow stretch.</p><div class="pr">$749</div></div></div>

  <div class="kicker" style="margin-top:54px">Monthly services</div>
  <h3 style="font-family:'Archivo',sans-serif;font-weight:900;font-size:24px;color:#fff;margin-bottom:6px">Ongoing work, billed monthly.</h3>
  <p class="sec-sub" style="margin-bottom:18px">Buy any one on its own &mdash; or bundle several into a managed plan below and pay less.</p>
  <div class="svcgrid"><div class="svc feat"><div class="si"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"><path d="M12 21s-7-5.6-7-11a7 7 0 0 1 14 0c0 5.4-7 11-7 11z"/><circle cx="12" cy="10" r="2.5"/></svg></div><h4>Local SEO &amp; Maps</h4><p>Gets you into the top-3 map results where homeowners pick who to call.</p><div class="pr">$1,195<small>/month</small></div></div><div class="svc"><div class="si"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 11v2a1 1 0 0 0 1 1h2l4 4V6L6 10H4a1 1 0 0 0-1 1z"/><path d="M15 9a3 3 0 0 1 0 6"/><path d="M18 6a7 7 0 0 1 0 12"/></svg></div><h4>Google Ads</h4><p>Paid ads on money searches, managed and tracked. Ad budget paid to Google separately.</p><div class="pr">$549<small>/mo or 12% of spend</small></div></div><div class="svc"><div class="si"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"><path d="M12 3l7 3v5c0 4.5-3 8-7 10-4-2-7-5.5-7-10V6z"/><path d="M9 12l2 2 4-4"/></svg></div><h4>Local Services Ads</h4><p>The &ldquo;Google Guaranteed&rdquo; pay-per-lead ads, set up and managed.</p><div class="pr">$449<small>/month</small></div></div><div class="svc"><div class="si"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="18" cy="5" r="2.5"/><circle cx="6" cy="12" r="2.5"/><circle cx="18" cy="19" r="2.5"/><path d="M8.2 10.8l7.6-4.4M8.2 13.2l7.6 4.4"/></svg></div><h4>Facebook / Instagram</h4><p>Lead campaigns on Meta, as an add-on.</p><div class="pr">$449<small>/month</small></div></div><div class="svc feat"><div class="si"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"><path d="M4 5h16a1 1 0 0 1 1 1v10a1 1 0 0 1-1 1H8l-4 3z"/><line x1="8" y1="9" x2="16" y2="9"/><line x1="8" y1="13" x2="13" y2="13"/></svg></div><h4>Missed-call text-back</h4><p>Every missed call gets an instant text so the lead doesn&rsquo;t call a competitor.</p><div class="pr">$199<small>/month</small></div></div><div class="svc"><div class="si"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M13 2 3.5 14H10l-1 8L19 10h-6.5L13 2z"/></svg></div><h4>Automation suite</h4><p>Text-back + instant reply + booking + review requests, wired together. $995 setup.</p><div class="pr">$349<small>/month</small></div></div><div class="svc"><div class="si"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"><path d="M12 2.5l2.9 6 6.6.9-4.8 4.6 1.2 6.5L12 17.4 6.1 20.5l1.2-6.5L2.5 9.4l6.6-.9z"/></svg></div><h4>Reputation management</h4><p>Automatic review requests and response handling to grow your star rating.</p><div class="pr">$249<small>/month</small></div></div><div class="svc"><div class="si"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="18" cy="5" r="2.5"/><circle cx="6" cy="12" r="2.5"/><circle cx="18" cy="19" r="2.5"/><path d="M8.2 10.8l7.6-4.4M8.2 13.2l7.6 4.4"/></svg></div><h4>Social media management</h4><p>Regular posts so your pages look alive and trustworthy.</p><div class="pr">$649<small>/month</small></div></div></div>

  <div id="plans" class="kicker" style="margin-top:58px">Managed plans &mdash; bundle &amp; save</div>
  <h3 style="font-family:'Archivo',sans-serif;font-weight:900;font-size:24px;color:#fff;margin-bottom:6px">Want it all handled? Pick a plan.</h3>
  <p class="sec-sub" style="margin-bottom:24px">These bundle the monthly services above into one price &mdash; cheaper than buying each on its own, and managed as one system. 90-day initial term, then month-to-month.</p>
  <div class="grid3" style="align-items:stretch">
    <div class="price-card"><span class="tag">Starter</span><h3>Door-Opener</h3><div class="amt">$749</div><div class="per">one-time &middot; not monthly</div>
      <ul class="checks"><li>One fast, provable win in ~30 days</li><li>Win-back campaign or Google listing overhaul</li><li>No commitment &mdash; a no-risk first step</li></ul>
      <a class="btn navy" href="free-audit.html" style="width:100%;text-align:center;margin-top:6px">Start here</a></div>
    <div class="price-card hot"><span class="pin">MOST POPULAR</span><span class="tag">Monthly</span><h3>Lead Engine</h3><div class="amt">$1,495<small style="font-size:15px;color:var(--grey);font-weight:500">/mo</small></div><div class="per">the core system that keeps you booked</div>
      <ul class="checks"><li>Local SEO + Google Maps ranking</li><li>Automatic review requests</li><li>Missed-call text-back</li><li>Leads answered in under a minute</li><li>Monthly report in jobs &amp; dollars</li></ul>
      <a class="btn" href="free-audit.html" style="width:100%;text-align:center;margin-top:6px">Get started</a></div>
    <div class="price-card"><span class="tag">Monthly</span><h3>Growth</h3><div class="amt">$2,950<small style="font-size:15px;color:var(--grey);font-weight:500">/mo</small></div><div class="per">+ ad budget &middot; for scaling up</div>
      <ul class="checks"><li>Everything in Lead Engine</li><li>Google Ads + LSA management</li><li>Social media management</li><li>Quarterly job-site content day</li></ul>
      <a class="btn navy" href="free-audit.html" style="width:100%;text-align:center;margin-top:6px">Get started</a></div>
  </div>

  <div class="note" style="margin-top:36px"><b>Quick gut-check:</b> the $1,495/mo Lead Engine is about the cost of 16 shared HomeStars/Angi leads &mdash; except those get sold to five competitors and vanish, while everything we build is yours and compounds. One average furnace install covers the month.</div>

  <div style="max-width:820px;margin-top:46px">
  <h2 class="sec-h2" style="font-size:26px">Common questions</h2>
  <details><summary>I just want a website. What do I pay?</summary><p>$2,950 for the website on its own &mdash; built, yours to keep, no monthly fee. Or $3,950 for the Launch Bundle, which adds your Google Business Profile setup and a brand refresh (a better deal if you need all three). No monthly commitment required for either.</p></details>
  <details><summary>Do I have to sign up for a monthly plan?</summary><p>No. Buy any single service &mdash; a website, a logo, just local SEO &mdash; on its own. The monthly plans simply bundle several services for less and manage them as one system. Many contractors start with the $749 Door-Opener to see results first.</p></details>
  <details><summary>Can I mix and match?</summary><p>Yes. Start with a website, add missed-call text-back next month, layer in SEO when you're ready. We'll always tell you the single most valuable next step &mdash; the free audit usually makes it obvious.</p></details>
  <details><summary>What's NOT included in the prices?</summary><p>Ad spend (paid directly to Google/Meta &mdash; your account, your money, full visibility) and third-party costs like premium stock or print runs. No markups, no surprises.</p></details>
  <details><summary>Why are you cheaper than the big agencies?</summary><p>Lower overhead, no account-manager layers, and entry pricing while we build our Ottawa case-study wall. Prices rise as proof accumulates &mdash; locking in now is the best deal we'll ever offer.</p></details>
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
  <img src="assets/founder-sajad.jpg" alt="Sajad — founder of Packed Agency" width="1000" height="1000" style="width:100%;max-width:380px;height:auto;border-radius:18px;border:1px solid var(--line)">
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
    "No call centre, no account managers — you reach the founder directly. Book a call, send a message, or text.", "Contact")
contact_body += """
<section><div class="wrap"><div class="grid2" style="gap:60px;align-items:start">
<div class="prose">
  <div style="background:var(--card);border:1px solid rgba(249,115,22,.4);border-radius:14px;padding:24px;margin-bottom:24px">
    <div class="kicker" style="margin-bottom:8px">Best way to talk</div>
    <h2 style="margin-top:0;font-size:22px">Book a free 30-minute call</h2>
    <p style="color:var(--grey);font-size:14.5px;margin-bottom:16px">Grab a time that suits you and we&rsquo;ll meet on Google Meet &mdash; no pressure, just a straight conversation about your schedule and how to fill it.</p>
    <a class="btn" href="https://calendar.app.google/s2etv2aRyPFDhRZm7" target="_blank" rel="noopener">Pick a time that works &rarr;</a>
  </div>
  <h2 style="margin-top:0">Other ways to reach us</h2>
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
</div>""" + NEWSLETTER + """</div></section>
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
</div>""" + NEWSLETTER + """</div></section>""" + CTA
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
""" + NEWSLETTER + """</div></section>""" + CTA
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

# ============================================================ GUIDE PAGES (Marketing School)
def guide_page(fname, title, kicker, h1, lead, intro, checks, faq, note):
    b = phero(kicker, h1, lead, "Free Resources / Guide")
    b += "<section><div class=\"wrap\" style=\"max-width:860px\">"
    b += "<p class=\"sec-sub\" style=\"max-width:860px\">" + intro + "</p>"
    b += ("<div class=\"todo-box\"><div class=\"todo-head\"><span>Your checklist</span>"
          "<span class=\"todo-score\" data-score></span></div>")
    for c in checks: b += "<label class=\"todo\"><input type=\"checkbox\"><span>" + c + "</span></label>"
    b += "<div class=\"todo-msg\" data-msg></div></div>"
    if note: b += "<div class=\"note\">" + note + "</div>"
    b += "<h2 class=\"sec-h2\" style=\"font-size:26px;margin-top:40px\">Fair questions</h2>"
    for q, a in faq: b += "<details><summary>" + q + "</summary><p>" + a + "</p></details>"
    b += ("<p style=\"margin-top:34px\"><a class=\"btn\" href=\"free-audit.html\">Get My Free Audit</a>&nbsp;&nbsp;"
          "<a class=\"btn navy\" href=\"resources.html\">More free guides</a></p>")
    b += NEWSLETTER
    b += "</div></section>"
    page(fname, title, lead, "resources", b)

guide_page("guide-google-business-profile.html",
    "Google Business Profile for Contractors: The 10-Minute Fix | Packed Agency",
    "Free guide", "The 10-minute Google Business Profile <em>fix.</em>",
    "Your Google listing drives more calls than your website — and most trades have it 30% filled. Six fixes you can do today, free.",
    "When a homeowner searches your trade, Google shows the map first. Your Google Business Profile (the listing with your name, reviews and photos) decides whether you appear there. Here is exactly what to fix, in order of impact:",
    ["Pick your <b>primary category</b> precisely (&ldquo;Plumber&rdquo;, not &ldquo;Contractor&rdquo;) — it is the single biggest ranking lever",
     "Add every service you offer as a separate service item, with a sentence each",
     "Upload 10+ real job photos (trucks, crews, finished work) — phone photos beat stock, always",
     "Set service areas to the neighbourhoods you actually want jobs in",
     "Answer the Q&amp;A section yourself before strangers do",
     "Post once a week — a finished job with one photo counts"],
    [("How long until I see results?", "Category and service fixes can move your map position within 2&ndash;4 weeks. Photos and weekly posts compound over 2&ndash;3 months. It is the highest-return free work in contractor marketing."),
     ("Do I really need to post every week?", "It is a tie-breaker, not a magic bullet. Two competitors with equal reviews: the active profile wins. One photo of a finished job with one sentence is enough — do it from your truck."),
     ("My listing is suspended or duplicated. Now what?", "Common and fixable: claim the duplicate, request reinstatement with your business documents, and never list a PO box. If you are stuck, this is exactly the kind of thing our free audit catches.")],
    "<b>Since November 2024</b>, a verified Google Business Profile is also mandatory to run Google&rsquo;s pay-per-lead ads (Local Services Ads) — and since mid-2025 your profile reviews directly power those ads&rsquo; ranking. The listing is no longer optional infrastructure; it IS your marketing foundation.")

guide_page("guide-reviews.html",
    "How Contractors Get More Google Reviews: The Playbook | Packed Agency",
    "Free guide", "The review playbook that <em>actually works.</em>",
    "Reviews decide ties in the Google map pack. The trick isn't asking — it's when and how you ask.",
    "Two contractors, same distance from the homeowner: the one with 150 fresh reviews beats the one with 30 old ones, almost every time. Here is the playbook:",
    ["Ask at the <b>moment of thanks</b> — when the customer says &ldquo;this is great&rdquo;, that's the window",
     "Send the direct review link by text within 10 minutes (search &ldquo;Google review link generator&rdquo; — it's free)",
     "Aim for velocity, not volume: 2&ndash;3 fresh reviews a month beats 50 old ones",
     "Reply to every review, including the bad ones — replies are ranking signals and trust signals",
     "Never buy reviews. Google's filters catch them and the penalty outlasts the boost"],
    [("Can I just ask every customer at the end of the job?", "Yes — but timing beats coverage. The customer who just thanked you converts at several times the rate of one getting a generic &ldquo;please review us&rdquo; email three days later."),
     ("Should I respond to a bad review?", "Always, within 24 hours, calmly and factually. Future customers read your reply more carefully than the complaint. Never argue; offer to fix it offline."),
     ("Are review incentives allowed?", "No — and Google tightened this again in 2026: review quotas for techs, asking customers to name a specific employee, and &ldquo;scan this tablet before I leave&rdquo; pressure are now formal policy violations that can get reviews wiped. Ask honestly, at the right moment, and you will not need tricks.")],
    "")

guide_page("guide-website-checklist.html",
    "Why Contractor Websites Don't Generate Leads: 7 Fixes | Packed Agency",
    "Free guide", "7 reasons contractor websites <em>never ring.</em>",
    "About 90% of contractor websites fail to turn visitors into calls. These are the seven leaks — check yours against each one.",
    "A website that doesn't make the phone ring isn't a website — it's a brochure nobody asked for. Walk through your own site on your phone and check:",
    ["Phone number not clickable on mobile (60%+ of your visitors are on phones)",
     "No quote form above the fold — visitors won't scroll to find it",
     "Slow loading: every extra second loses visitors before they see anything",
     "Stock photos instead of your real trucks and crews — homeowners can smell it",
     "No reviews or proof on the page itself",
     "One generic page instead of a page per service and area",
     "No follow-up when someone does fill the form (see our follow-up guide)"],
    [("Do I need a new website, or can mine be fixed?", "If it loads fast and you can edit it, most of these leaks are patchable. If it is on an old builder, locked by a previous agency, or takes 8 seconds to load on a phone — rebuilding is usually cheaper than fighting it. Our free audit tells you which, honestly."),
     ("What matters more — looks or speed?", "Speed, and it is not close. Homeowners forgive a plain site that loads instantly and shows a phone number; they do not wait for a beautiful one. Test yours on your own phone, on data, not Wi-Fi.")],
    "")

guide_page("guide-follow-up.html",
    "Lead Follow-Up for Contractors: Where the Money Leaks | Packed Agency",
    "Free guide", "Follow-up: where the money <em>actually leaks.</em>",
    "80% of sales take five or more contacts — most contractors stop at one. Three free fixes you can start today.",
    "The cheapest lead you will ever get is the one already in your missed-call log. The stats that should change how you run your phone:",
    ["<b>80% of sales take 5+ contacts</b> — most contractors stop at one",
     "<b>85% of callers who hit voicemail don't leave a message</b> — they call the next name on Google",
     "Free fix #1: a text auto-reply on your business line (&ldquo;Sorry we missed you — text us the job details&rdquo;)",
     "Free fix #2: a 5-minute end-of-day rule — every missed call and quote gets one text before you go home",
     "Free fix #3: a &ldquo;quote sent&rdquo; reminder 3 days later. One text. Most competitors never send it",
     "Want your number? The <a href=\"calculator.html\" style=\"color:var(--orange);font-weight:700\">Missed-Call Calculator</a> takes 20 seconds"],
    [("Won't automatic texts annoy my customers?", "A homeowner who just called you wants a reply. &ldquo;Sorry we missed you — how can we help?&rdquo; within seconds is service, not spam. Annoying is silence followed by a competitor's truck in their driveway."),
     ("I'm a one-person shop. Is automation overkill?", "The opposite — you are the person who physically cannot answer while on the tools. Missed-call text-back exists precisely for the solo operator; it costs less per month than one lost service call."),
     ("Why does answer speed suddenly matter even more in 2026?", "Google now tracks whether and how fast you answer calls from its pay-per-lead ads, and ranks slow answerers lower. Follow-up speed stopped being just good practice — it is now literally a ranking factor.")],
    "")

guide_page("guide-lead-costs.html",
    "What a Contractor Lead Should Cost in 2026: Honest Benchmarks | Packed Agency",
    "Free guide", "What leads should cost <em>(so nobody rips you off.)</em>",
    "Honest 2026 benchmarks for every lead channel — so when someone quotes you a price, you can make them answer in numbers.",
    "Almost nobody publishes real lead costs, which is exactly why contractors get overcharged. Here are the honest ranges from published industry data:",
    ["<b>Google Local Services Ads (HVAC):</b> $60&ndash;120 per lead — and junk leads are disputable (most contractors never dispute)",
     "<b>Google Search ads (managed):</b> ~$50&ndash;60 per call with ~55% close rates — roughly $110 per booked job",
     "<b>Home-services average across channels:</b> ~$91 per lead; roofing runs up to ~$228",
     "<b>Shared marketplaces (HomeStars/Angi):</b> similar sticker price — but the same homeowner is sold to up to 5 competitors, so your cost per WON job is far higher",
     "<b>Google Maps / local SEO:</b> ~40% lower cost-per-sale than ads once ranked — the slow channel that wins"],
    [("Are shared marketplace leads ever worth it?", "As a temporary bridge while you build owned channels, maybe. As a strategy, no — you are bidding against four competitors for the same homeowner, with no asset left when you stop paying."),
     ("What should I ask an agency that quotes me a price?", "Three questions: What does a lead cost through you, in dollars? Do I own the accounts and the website if I leave? Can I see call tracking, not just a report? An honest agency answers all three in numbers — these benchmarks tell you if the numbers are fair.")],
    "If someone quotes you far outside these ranges — in either direction — ask why, and make them answer in numbers. (Sources: published LocaliQ, WebFX and industry benchmark data; full citations on the blog.)")

# ============================================================ EVENTS
ev_body = phero("Events &amp; networking", "Where Ottawa contractors <em>actually meet.</em>",
    "Trade shows, association breakfasts and networking that's worth a contractor's morning — updated as the calendar moves.", "Events")
ev_body += """
<section><div class="wrap">
  <div class="kicker">Join one of these first</div>
  <h2 class="sec-h2" style="font-size:28px">Local associations worth your membership</h2>
  <div class="grid3" style="margin-top:26px">
    <div class="card"><h3>Greater Ottawa Home Builders&rsquo; Association (GOHBA)</h3><p>The home-building and renovation crowd: monthly breakfast events, spring &amp; summer golf tournaments, the Housing Design Awards, and the HOWL women-in-homebuilding series. The breakfasts are the best networking-per-hour in the city. Find them at gohba.ca.</p></div>
    <div class="card"><h3>Ottawa Construction Association (OCA)</h3><p>Commercial and trade contractors: education courses year-round and the annual OCA Construction Symposium &amp; Trade Show each spring at the EY Centre — builders, suppliers and buyers in one room. Details at oca.ca.</p></div>
    <div class="card"><h3>BNI &amp; local referral groups</h3><p>Structured weekly referral networking. One plumber, one electrician, one renovator per chapter — which means your trade's seat might be open. Best ROI for service trades that live on referrals.</p></div>
  </div>

  <div class="kicker" style="margin-top:56px">Mark the calendar</div>
  <h2 class="sec-h2" style="font-size:28px">Shows where homeowners come to you</h2>
  <div class="grid3" style="margin-top:26px">
    <div class="card"><h3>Ottawa Home shows (spring &amp; fall)</h3><p>The Ottawa Home + Garden Show (spring) and Ottawa Fall Home Show put you in front of thousands of homeowners actively planning projects. A modest booth plus a good follow-up system beats a big booth with no follow-up, every time.</p></div>
    <div class="card"><h3>OCA Symposium &amp; Trade Show</h3><p>Annual, spring, EY Centre. Even as a visitor: suppliers, builders and subcontractor relationships in one afternoon.</p></div>
    <div class="card"><h3>Worth the drive: Toronto</h3><p>The Buildings Show (December) is Canada&rsquo;s biggest construction event; CMPX is the national HVACR &amp; plumbing expo. Go once a year to see where the industry is heading before your competitors do.</p></div>
  </div>

  <div class="kicker" style="margin-top:56px">Free playbook</div>
  <h2 class="sec-h2" style="font-size:28px">How to work a trade show (without wasting it)</h2>
  <ul class="checks" style="max-width:820px">
    <li>Set one number before you go: conversations that end with a phone number in your pocket. Ten beats a hundred business cards handed out</li>
    <li>Text every contact the same evening — &ldquo;Good meeting you at the show&rdquo; — while everyone else waits a week and gets forgotten</li>
    <li>Bring your calendar, not your brochure: book the estimate on the spot</li>
    <li>Photograph your booth conversations (with permission) — a month of social content in one day</li>
    <li>Walk the competitors&rsquo; booths: their pitch, their pricing sheet, their weaknesses — it&rsquo;s all public that day</li>
  </ul>
  <div class="note" style="max-width:820px;margin-top:36px"><b>Know an event we should list?</b> Tell us at info@packedagency.ca — this page is updated as the Ottawa calendar moves.</div>
""" + NEWSLETTER + """</div></section>""" + CTA
page("events.html", "Contractor Events & Networking in Ottawa (2026) | Packed Agency",
     "Ottawa contractor events, trade shows and associations: GOHBA, OCA Symposium, home shows, BNI — plus how to actually work a trade show.", "resources", ev_body)

# ============================================================ NEWS BULLETIN
news_body = phero("The Packed Bulletin &mdash; June 2026", "Trade news that <em>actually matters.</em>",
    "Five changes affecting Ottawa contractors right now — what happened, and what to do about it. Updated monthly.", "News")
news_body += """
<section><div class="wrap" style="max-width:860px">
  <div style="margin-bottom:36px">
    <a class="chip" href="#n1"><b>1</b> &nbsp;Heat-pump rebates up to $12k</a>
    <a class="chip" href="#n2"><b>2</b> &nbsp;Reviews now power your ads</a>
    <a class="chip" href="#n3"><b>3</b> &nbsp;New Google badge</a>
    <a class="chip" href="#n4"><b>4</b> &nbsp;Review-ask rules tightened</a>
    <a class="chip" href="#n5"><b>5</b> &nbsp;Slow answers = lower rank</a>
  </div>

  <div class="kicker" id="n1">No. 1 &mdash; Money on the table</div>
  <h2 class="sec-h2" style="font-size:26px">Ontario&rsquo;s heat-pump rebates run up to $7,500&ndash;$12,000 &mdash; and only registered contractors can submit</h2>
  <p class="sec-sub" style="max-width:860px;margin-bottom:10px">Ontario&rsquo;s Home Renovation Savings program pays homeowners up to $7,500 for cold-climate air-source heat pumps and up to $12,000 for geothermal — and applications go through <b>HRS-registered contractors only</b>. If you're in HVAC and not registered, every competitor who is becomes the easier choice. Deadlines and program windows shift — check the program site before quoting it to customers.</p>
  <p class="sec-sub" style="max-width:860px"><b>Do this:</b> get registered, then put &ldquo;rebate-registered&rdquo; on your Google listing, website and quotes. It's a closing tool, not paperwork.</p>

  <div class="kicker" style="margin-top:50px" id="n2">No. 2 &mdash; Google merged your reviews</div>
  <h2 class="sec-h2" style="font-size:26px">Your Google Business Profile now powers your pay-per-lead ads</h2>
  <p class="sec-sub" style="max-width:860px">Since mid-2025, Local Services Ads reviews live entirely in your Google Business Profile — and your profile's rating and review volume now directly affect your ad ranking. A verified profile is already mandatory to run LSAs at all. Translation: the free listing and the paid ads are now one system, and reviews are its fuel. (Our <a href="guide-reviews.html" style="color:var(--orange);font-weight:700">review playbook</a> is free.)</p>

  <div class="kicker" style="margin-top:50px" id="n3">No. 3 &mdash; New badge</div>
  <h2 class="sec-h2" style="font-size:26px">&ldquo;Google Guaranteed&rdquo; is gone &mdash; meet the blue checkmark</h2>
  <p class="sec-sub" style="max-width:860px">In late 2025 Google retired the Google Guaranteed and Google Screened badges and replaced both with a single <b>Google Verified</b> blue checkmark. If your truck wrap, website or estimates still say &ldquo;Google Guaranteed&rdquo;, update the wording — homeowners are already seeing the new badge in search.</p>

  <div class="kicker" style="margin-top:50px" id="n4">No. 4 &mdash; Review rules tightened</div>
  <h2 class="sec-h2" style="font-size:26px">Tablet-in-the-driveway review asks are now a violation</h2>
  <p class="sec-sub" style="max-width:860px">Google's 2026 review-policy refresh formally bans review quotas for techs, asking customers to mention an employee by name, and on-premises pressure — including the classic &ldquo;scan this before I leave&rdquo; tablet move. Penalty: wiped reviews, possibly a suspended profile. Asking honestly at the moment of thanks is still allowed — and still works best.</p>

  <div class="kicker" style="margin-top:50px" id="n5">No. 5 &mdash; Speed is now a ranking factor</div>
  <h2 class="sec-h2" style="font-size:26px">Google now ranks you lower if you answer the phone slowly</h2>
  <p class="sec-sub" style="max-width:860px">Local Services Ads now track whether you answer, how fast, and whether the call lasts long enough to be a real conversation — and slow answerers get worse placement and pay more per lead. Unanswered phones now cost you twice: the lost job AND the ranking. (This is exactly the leak our <a href="automation.html" style="color:var(--orange);font-weight:700">follow-up automation</a> plugs.)</p>

  """ + NEWSLETTER + """<div class="note" style="margin-top:50px"><b>Sources &amp; further reading:</b> Google Business Profile community notices, Google Local Services policy pages, Ontario Home Renovation Savings program documentation, and industry coverage from SmartSites, Surefire Local and Digital Shift. We read it so you can stay on the tools — new bulletin monthly.</div>
</div></section>""" + CTA
page("news.html", "Contractor Marketing News - June 2026 Bulletin | Packed Agency",
     "Heat-pump rebates, Google review policy changes, the new Verified badge, and why answer speed now affects your ranking - monthly news for Ottawa trades.", "resources", news_body)

# ============================================================ RESOURCES HUB
res_body = phero("Free learning &mdash; no email wall", "The Contractor's <em>Marketing School.</em>",
    "Free guides, local events, trade news and (soon) video lessons — the same playbooks we charge for, taught in public. Steal it all.", "Free Resources")
res_body += """
<section><div class="wrap">
""" + MAGNET + """
  <div class="kicker">Guides</div>
  <h2 class="sec-h2" style="font-size:28px">Start here — five free playbooks</h2>
  <div class="grid3" style="margin-top:26px">
    <a class="card" href="guide-google-business-profile.html"><div class="ic"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 21s-7-5.6-7-11a7 7 0 0 1 14 0c0 5.4-7 11-7 11z"/><circle cx="12" cy="10" r="2.5"/></svg></div><span class="tag">10 minutes</span><h3>The Google Business Profile fix</h3><p>The listing that drives more calls than your website — six fixes, free, today.</p><span style="color:var(--orange);font-weight:700;font-size:14px">Read the guide →</span></a>
    <a class="card" href="guide-reviews.html"><div class="ic"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"><path d="M12 2.5l2.9 6 6.6.9-4.8 4.6 1.2 6.5L12 17.4 6.1 20.5l1.2-6.5L2.5 9.4l6.6-.9z"/></svg></div><span class="tag">Playbook</span><h3>Get more Google reviews</h3><p>Reviews decide map-pack ties. When and how to ask — and the 2026 rules that changed.</p><span style="color:var(--orange);font-weight:700;font-size:14px">Read the guide →</span></a>
    <a class="card" href="guide-website-checklist.html"><div class="ic"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="16" rx="2"/><line x1="3" y1="9" x2="21" y2="9"/><circle cx="6" cy="6.5" r=".5"/><circle cx="8.5" cy="6.5" r=".5"/></svg></div><span class="tag">Checklist</span><h3>7 reasons websites never ring</h3><p>Walk your own site through the seven leaks that kill contractor websites.</p><span style="color:var(--orange);font-weight:700;font-size:14px">Read the guide →</span></a>
    <a class="card" href="guide-follow-up.html"><div class="ic"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 2 .7 2.9a2 2 0 0 1-.5 2.1L8 10a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.5c.9.3 1.9.6 2.9.7a2 2 0 0 1 1.7 2z"/></svg></div><span class="tag">3 free fixes</span><h3>Follow-up: the money leak</h3><p>80% of sales take 5+ contacts. Most contractors stop at one. Fix it free.</p><span style="color:var(--orange);font-weight:700;font-size:14px">Read the guide →</span></a>
    <a class="card" href="guide-lead-costs.html"><div class="ic"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><line x1="12" y1="2" x2="12" y2="22"/><path d="M17 6.5c0-1.9-2.2-3-5-3s-5 1.1-5 3 2 2.8 5 3.7 5 1.8 5 3.8-2.2 3-5 3-5-1.1-5-3"/></svg></div><span class="tag">Benchmarks</span><h3>What leads should cost</h3><p>Honest 2026 numbers for every channel — so nobody rips you off.</p><span style="color:var(--orange);font-weight:700;font-size:14px">Read the guide →</span></a>
    <a class="card dark" href="free-audit.html"><div class="ic"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M13 2 3.5 14H10l-1 8L19 10h-6.5L13 2z"/></svg></div><span class="badge">FASTEST PATH</span><h3>Skip ahead: the free audit</h3><p>We run all five playbooks against YOUR business and send you a 10-minute video.</p><span style="color:#FDBA74;font-weight:700;font-size:14px">Get it free →</span></a>
  </div>

  <div class="kicker" style="margin-top:60px">From the blog</div>
  <h2 class="sec-h2" style="font-size:28px">Data we publish, weekly</h2>
  <div class="grid3" style="margin-top:26px">
    <a class="card" href="blog-hvac-lead-cost.html"><span class="tag">Published</span><h3>What an HVAC lead costs in Ottawa (2026)</h3><p>Real benchmarks: LSA, ads, marketplaces and SEO compared.</p><span style="color:var(--orange);font-weight:700;font-size:14px">Read →</span></a>
    <div class="card" style="opacity:.75"><span class="tag">Next</span><h3>The mystery call: we phoned 10 Ottawa plumbers</h3><p>How many answered? The results explain who's busy.</p></div>
    <a class="card" href="blog.html"><h3>All articles →</h3><p>Ottawa-specific answers to what contractors actually type into Google.</p></a>
  </div>

  <div class="kicker" style="margin-top:60px">Get out of the truck</div>
  <h2 class="sec-h2" style="font-size:28px">Events &amp; networking</h2>
  <div class="grid2" style="margin-top:26px">
    <a class="card" href="events.html"><div class="ic"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="5" width="18" height="16" rx="2"/><line x1="3" y1="10" x2="21" y2="10"/><line x1="8" y1="3" x2="8" y2="7"/><line x1="16" y1="3" x2="16" y2="7"/></svg></div><span class="tag">Updated regularly</span><h3>The Ottawa contractor calendar</h3><p>GOHBA breakfasts, the OCA Symposium, home shows, BNI seats — where the work actually gets referred, plus our free &ldquo;how to work a trade show&rdquo; playbook.</p><span style="color:var(--orange);font-weight:700;font-size:14px">See events &amp; associations →</span></a>
    <a class="card" href="news.html"><div class="ic"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 4h13a2 2 0 0 1 2 2v12a2 2 0 0 0 2-2"/><path d="M19 20H6a2 2 0 0 1-2-2V4"/><line x1="8" y1="9" x2="15" y2="9"/><line x1="8" y1="13" x2="15" y2="13"/></svg></div><span class="tag">Monthly bulletin</span><h3>Trade news that matters</h3><p>Rebate programs, Google policy changes, rule updates — what happened and what to do about it, in plain English. No fluff, five items, monthly.</p><span style="color:var(--orange);font-weight:700;font-size:14px">Read the June bulletin →</span></a>
  </div>

  <div class="kicker" style="margin-top:60px">Coming soon</div>
  <h2 class="sec-h2" style="font-size:28px">Video lessons</h2>
  <div class="card" style="max-width:860px"><div class="ic"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"><circle cx="12" cy="12" r="9.5"/><path d="M10 8.5l6 3.5-6 3.5z" fill="currentColor" stroke="none"/></svg></div><h3>The Marketing School, on camera</h3><p>Short, practical videos of every guide above — watch from the truck between jobs. In production now; first episodes land here and on our YouTube channel. Want to be notified? Mention it in the <a href="contact.html" style="color:var(--orange);font-weight:700">contact form</a> and we'll text you when episode one drops.</p></div>

  """ + NEWSLETTER + """<div class="note" style="max-width:820px;margin-top:50px"><b>Why we give this away:</b> teaching is our marketing. If you do all of this yourself — good, your schedule gets fuller and you'll tell other trades who taught you. If you'd rather be on the tools than on Google, that's what <a href="services.html" style="color:var(--orange);font-weight:700">we're for</a>.</div>
</div></section>""" + CTA
page("resources.html", "Free Marketing Resources for Contractors | Packed Agency",
     "Free contractor marketing school: Google Business Profile fixes, review playbook, website checklist, lead-cost benchmarks, Ottawa events and monthly trade news.", "resources", res_body)

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
