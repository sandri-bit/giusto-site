"""Gera as páginas de case (cases/<slug>.html) a partir de _fonte/cases.json.

Uso: python _fonte/gerar_cases.py   (rodar na raiz do repositório)
Cada case tem cabeçalho, texto, blocos de imagem/vídeo e o link para o próximo case.
Tipos de bloco: title, full, duo, trio, mosaic, track, reels, video, feed (carrossel num celular), screen (apresentação num monitor), stats, quote.
"""
import json, html, os, sys
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = json.load(open(os.path.join(ROOT, '_fonte', 'cases.json'), encoding='utf-8'))
e = lambda s: html.escape(str(s), quote=True)


def size(src):
    p = os.path.join(ROOT, src)
    try:
        with Image.open(p) as im:
            return im.size
    except Exception:
        return None


def img(src, alt='', cls='', lazy=True):
    wh = size(src)
    dims = f' width="{wh[0]}" height="{wh[1]}"' if wh else ''
    return f'<img src="../{e(src)}" alt="{e(alt)}"{dims}{" loading=lazy decoding=async" if lazy else ""}{f" class={cls}" if cls else ""}>'


def shot(it, extra=''):
    if isinstance(it, str):
        it = {'src': it}
    cap = f'<div class="cap"><span>{e(it["cap"])}</span></div>' if it.get('cap') else ''
    if it['src'].endswith('.mp4'):
        pst = it.get('poster') or poster_of(it['src'])
        poster = f' poster="../{e(pst)}"' if pst else ''
        body = f'<video src="../{e(it["src"])}"{poster} muted loop playsinline preload="none" data-auto></video>'
    else:
        body = img(it['src'], it.get('alt', ''))
    return f'<figure class="rv" style="margin:0{extra}"><div class="shot">{body}</div>{cap}</figure>'


def poster_of(src):
    p = src[:-4] + '.webp'
    return p if os.path.exists(os.path.join(ROOT, p)) else ''


def phone(v, drift=0, mid=False):
    if isinstance(v, str):
        v = {'src': v}
    d = f' data-drift="{drift}"' if drift else ''
    if not v['src'].endswith('.mp4'):
        return f'<div class="phone{" mid" if mid else ""}"{d}><div class="scr">{img(v["src"], v.get("alt", ""))}</div></div>'
    pst = v.get('poster') or poster_of(v['src'])
    poster = f' poster="../{e(pst)}"' if pst else ''
    return (f'<div class="phone{" mid" if mid else ""}"{d}><div class="scr">'
            f'<video src="../{e(v["src"])}"{poster} muted loop playsinline preload="none" data-auto aria-label="{e(v.get("alt", "Vídeo"))}"></video>'
            f'<button class="snd" type="button" aria-label="Ligar ou desligar o som">♪</button></div></div>')


def block(b):
    t = b['t']
    if t == 'title':
        p = f'<p class="rv">{e(b["text"])}</p>' if b.get('text') else ''
        return f'<div class="wrap"><div class="blk-title"><div><div class="lbl dotted rv" style="margin-bottom:18px">{e(b.get("lbl", ""))}</div><h2 class="rv">{e(b["h"])}</h2></div>{p}</div></div>'
    if t == 'full':
        wh = size(b['src']) or (16, 9)
        ar = b.get('ar') or f'{wh[0]}/{wh[1]}'
        cap = f'<div class="cap"><span>{e(b["cap"])}</span></div>' if b.get('cap') else ''
        bleed = ' bleed' if b.get('bleed') else ''
        inner = f'<div class="par" style="--ar:{ar}">{img(b["src"], b.get("alt", ""))}</div>{cap}'
        return f'<section class="blk full{bleed}">{inner if bleed else f"<div class=wrap>{inner}</div>"}</section>'
    if t in ('duo', 'trio'):
        off = ' off' if b.get('off', True) and t == 'duo' else ''
        return f'<section class="blk"><div class="wrap"><div class="{t}{off}">{"".join(shot(i) for i in b["items"])}</div></div></section>'
    if t == 'mosaic':
        return f'<section class="blk"><div class="wrap"><div class="mosaic">{"".join(shot(i) for i in b["items"])}</div></div></section>'
    if t == 'track':
        items = ''.join(f'<div class="shot{" fit" if b.get("fit") else ""}">{img(i if isinstance(i, str) else i["src"], "" if isinstance(i, str) else i.get("alt", ""))}</div>' for i in b['items'])
        return (f'<section class="track" aria-label="{e(b.get("h", "Desdobramento"))}"><div class="stick">'
                f'<div class="wrap"><div class="meter"><span class="lbl dotted">{e(b.get("lbl", "Desdobramento"))}</span><div class="bar"><i></i></div><span class="lbl">{len(b["items"])} peças</span></div></div>'
                f'<div class="row">{items}</div></div></section>')
    if t == 'reels':
        vs = b['items']
        ph = ''.join(phone(v, drift=(-40 if i % 2 == 0 else 40), mid=(i % 2 == 1)) for i, v in enumerate(vs))
        head = f'<div class="blk-title"><div><div class="lbl dotted" style="margin-bottom:18px">{e(b.get("lbl", "Vídeo"))}</div><h2>{e(b.get("h", "Em movimento"))}</h2></div>{f"<p>{e(b[chr(116)+chr(120)+chr(116)])}</p>" if b.get("txt") else ""}</div>'
        return f'<section class="dark"><div class="wrap">{head}<div class="reels">{ph}</div></div></section>'
    if t == 'video':
        pst = b.get('poster') or poster_of(b['src'])
        poster = f' poster="../{e(pst)}"' if pst else ''
        ar = f' style="aspect-ratio:{b["ar"]}"' if b.get('ar') else ''
        return (f'<section class="blk"><div class="wrap"><div class="wide-video rv"{ar}><video src="../{e(b["src"])}"{poster} muted loop playsinline preload="metadata" data-auto></video>'
                f'<button class="snd" type="button" aria-label="Ligar ou desligar o som">♪</button></div></div></section>')
    if t == 'feed':
        n = len(b['items'])
        slides = ''.join(f'<div class="sl">{img(s, "")}</div>' for s in b['items'])
        dots = ''.join('<i></i>' for _ in b['items'])
        side = ''.join(img(s, '') for s in b['items'][:6])
        head = f'<div class="blk-title"><div><div class="lbl dotted" style="margin-bottom:18px">{e(b.get("lbl", "Redes sociais"))}</div><h2>{e(b.get("h", "No feed"))}</h2></div>{f"<p>{e(b[chr(116)+chr(120)+chr(116)])}</p>" if b.get("txt") else ""}</div>'
        return (f'<section class="dark"><div class="wrap">{head}<div class="reels" style="align-items:center"><div class="phone feedp" data-drift="-30"><div class="scr">'
                f'<div class="bar-top"><i>{e(b.get("perfil", " ")[0].upper())}</i><span>@{e(b.get("perfil", ""))}<small>Publicação</small></span></div><div class="carr" data-n="{n}"><div class="vp"><div class="strip">{slides}</div></div><div class="dots">{dots}</div></div>'
                f'<div class="ln"><b></b><b></b><b></b></div></div></div>'
                f'<div class="feed-side rv">{side}</div></div></div></section>')
    if t == 'screen':
        n = len(b['items'])
        slides = ''.join(f'<div class="sl">{img(s, "")}</div>' for s in b['items'])
        head = f'<div class="blk-title"><div><div class="lbl dotted rv" style="margin-bottom:18px">{e(b.get("lbl", "Apresentação"))}</div><h2 class="rv">{e(b.get("h", ""))}</h2></div>{f"<p class=rv>{e(b[chr(116)+chr(120)+chr(116)])}</p>" if b.get("txt") else ""}</div>'
        return (f'<section class="blk"><div class="wrap">{head}<div class="screen rv"><div class="mon carr" data-n="{n}"><div class="vp"><div class="strip">{slides}</div></div></div>'
                f'<div class="foot"><span class="dots">{"".join("<i></i>" for _ in b["items"])}</span><span class="lbl cnt">01 / {n:02d}</span></div></div></div></section>')
    if t == 'stats':
        its = ''.join(f'<div class="rv"><b>{e(s["n"])}{f"<sup>{e(s[chr(117)])}</sup>" if s.get("u") else ""}</b><span>{e(s["l"])}</span></div>' for s in b['items'])
        return f'<section class="blk"><div class="wrap" style="margin-top:clamp(70px,9vw,140px)"><div class="lbl dotted rv" style="margin-bottom:28px">{e(b.get("lbl", "Resultado"))}</div><div class="stats" style="--n:{len(b["items"])}">{its}</div></div></section>'
    if t == 'quote':
        return f'<section class="blk"><div class="wrap" style="margin-block:clamp(70px,9vw,140px)"><p class="quote rv">{e(b["text"])}<span class="dot">.</span></p></div></section>'
    raise ValueError(t)


TPL = '''<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{title} · Giusto Estratégia e Comunicação</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="https://giusto.ag/cases/{slug}">
<link rel="icon" type="image/png" href="/favicon.png?v=2">
<link rel="icon" href="/favicon.ico?v=2" sizes="48x48">
<link rel="apple-touch-icon" href="/apple-touch-icon.png?v=2">
<meta name="theme-color" content="#ffffff">
<meta property="og:type" content="article">
<meta property="og:locale" content="pt_BR">
<meta property="og:site_name" content="Giusto">
<meta property="og:title" content="{title} · {client}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="https://giusto.ag/cases/{slug}">
<meta property="og:image" content="https://giusto.ag/img/og/{slug}.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500&family=Fira+Sans:wght@300;400;500;600&display=swap">
<link rel="stylesheet" href="case.css">
<script>window.va=window.va||function(){(window.vaq=window.vaq||[]).push(arguments)};</script>
<script defer src="/_vercel/insights/script.js"></script>
<script defer src="/eventos.js"></script>
</head>
<body>
<div class="progress" aria-hidden="true"></div>
<header class="top"><div class="wrap">
  <a class="logo" href="../" aria-label="Giusto, início"><img src="../img/logo-xl.png" alt="giusto."></a>
  <a class="back" href="../#trabalhos">← Todos os trabalhos</a>
</div></header>

<div class="pill" role="navigation" aria-label="Principal">
  <a class="sym" href="../" aria-label="Início"><img src="../img/simbolo-neg.png" alt=""></a>
  <nav>
    <a href="../#trabalhos">Trabalhos</a>
    <a href="../#ia">IA</a>
    <a href="../#servicos">Serviços</a>
    <a href="../#socios">Sócios</a>
  </nav>
  <a class="cc" href="https://central.giusto.ag" target="_blank" rel="noopener"><span class="lock" aria-hidden="true"></span><span class="full">Central do Cliente</span><span class="short">Central</span></a>
  <a class="go" href="../#contato">Contato</a>
</div>

<main>
  <section class="c-head"><div class="wrap">
    <div class="lbl dotted">Case · {cat}</div>
    <h1>{title}<span class="dot">.</span></h1>
    <div class="c-meta">
      <div><span class="lbl">Cliente</span><b>{client}</b></div>
      <div><span class="lbl">Ano</span><b>{year}</b></div>
      <div><span class="lbl">Categoria</span><b>{cat}</b></div>
      <div><span class="lbl">Entregas</span><b>{scope}</b></div>
    </div>
  </div></section>

  <section class="c-hero" aria-label="Imagem principal" style="--har:{har}"><div class="frame">{hero}</div></section>

  <section class="c-story"><div class="wrap"><div class="grid">
    <p class="lead">{lead}</p>
    <div class="cols">
{cols}
    </div>
  </div></div></section>

{blocks}

  <div class="wrap">
    <a class="next" href="{nslug}.html">
      <div class="lbl"><span>Próximo case</span><span>{nclient}</span></div>
      <h2>{ntitle}</h2>
      <div class="img">{nimg}</div>
    </a>
  </div>
</main>

<footer><div class="wrap">
  <img src="../img/logo-xl.png" alt="giusto.">
  <span class="motto">O mundo é dos justos<i>.</i></span>
  <span>© 2026 Giusto Estratégia e Comunicação</span>
  <div class="links"><a href="https://www.instagram.com/giusto.ag/" target="_blank" rel="noopener">Instagram</a><a href="https://www.linkedin.com/company/giusto-ag/" target="_blank" rel="noopener">LinkedIn</a><a href="https://api.whatsapp.com/send/?phone=555133768925" target="_blank" rel="noopener">WhatsApp</a></div>
</div></footer>

<script src="https://cdn.jsdelivr.net/npm/lenis@1.1.13/dist/lenis.min.js"></script>
<script src="case.js"></script>
</body>
</html>
'''


def main():
    cases = [c for c in DATA['cases'] if c.get('publicado', True)]
    os.makedirs(os.path.join(ROOT, 'cases'), exist_ok=True)
    for i, c in enumerate(cases):
        n = cases[(i + 1) % len(cases)]
        cols = '\n'.join(f'      <div class="rv"><h3>{e(k)}</h3><p>{e(v)}</p>{"" if k != c["cols"][-1][0] or not c.get("tags") else "<div class=tags>" + "".join(f"<span>{e(t)}</span>" for t in c["tags"]) + "</div>"}</div>' for k, v in c['cols'])
        hero = c['hero']
        wh = size(hero) or (16, 9)
        har = f'{wh[0]}/{wh[1]}'
        hero_html = (f'<video src="../{e(hero)}" poster="../{e(c.get("hero_poster", ""))}" muted loop playsinline autoplay data-auto></video>'
                     if hero.endswith('.mp4') else img(hero, c.get('hero_alt', c['title']), lazy=False))
        page = TPL.format(
            title=e(c['title']), desc=e(c['desc']), slug=e(c['slug']), client=e(c['client']), cover=e(c['cover']),
            cat=e(c['cat']), year=e(c['year']), scope=e(c['scope']), hero=hero_html, har=har, lead=e(c['lead']), cols=cols,
            blocks='\n'.join(block(b) for b in c['blocks']),
            nslug=e(n['slug']), nclient=e(n['client']), ntitle=e(n['title']), nimg=img(n['cover'], n['title']))
        open(os.path.join(ROOT, 'cases', c['slug'] + '.html'), 'w', encoding='utf-8').write(page)
        print('ok', c['slug'])


if __name__ == '__main__':
    main()
