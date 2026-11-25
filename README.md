# Site da Giusto (giusto.ag)

Site estático, publicado na Vercel a partir da branch `main`.

- Origem do layout: artifact do Dan no Claude ("Giusto Proposta 2"). As imagens ficam também em
  `G:\Drives compartilhados\Giusto Clientes\Giusto\Site\Novo site 2026\giusto-site`.
- Contato só por WhatsApp (sem formulário).

## Ajustes feitos para publicar (refazer ao trazer uma nova versão do artifact)
1. Cabeçalho completo no topo do `index.html`: título, descrição, favicon, prévia de compartilhamento (`img/og.jpg`).
2. Linha `<meta name="claude:...">` e o `<title>` "Giusto Proposta 2" removidos.
3. Bloco `<style>` "Ajustes do site publicado": cards com página própria levam a `cases/<slug>`; card com classe `off` (hoje, Vida de Sorte) fica sem clique. O aviso "Nesta proposta..." foi retirado do script.

## Páginas de case
- Cada case é `cases/<slug>.html`, gerado por `python _fonte/gerar_cases.py` a partir de `_fonte/cases.json` (texto, números e blocos de imagem/vídeo). Não editar os HTML de `cases/` à mão: mudar o JSON e gerar de novo.
- Estilo e efeitos compartilhados: `cases/case.css` e `cases/case.js` (mesma identidade da home).
- Imagens em `img/cases/<slug>/` (.webp, lado maior até 2400 px); vídeos em `video/cases/<slug>/` (.mp4 H.264, até 30 s, com pôster .webp de mesmo nome).
- Tipos de bloco: `title`, `full`, `duo`, `trio`, `mosaic`, `track` (faixa horizontal, fora de uso), `reels` (celular plano), `video`, `feed` (carrossel que passa para o lado num celular plano), `screen` (apresentação passando num monitor de traço fino), `stats`, `quote`. Imagens aparecem sempre inteiras, sem corte.
- Para publicar um case novo: incluir no JSON, rodar o gerador e ligar o card da home ao `cases/<slug>`.
- `_fonte/` não vai para o site (`.vercelignore`).
