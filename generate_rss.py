#!/usr/bin/env python3
"""Gera feed RSS compatível com Pinterest Auto Feed RSS a partir do produtos.json."""

import json
import os
from datetime import datetime, timezone

BASE_URL = "https://brunoarcaya.github.io/gigaachadinhos"

def escape_xml(s):
    return (s.replace("&", "&amp;")
             .replace("<", "&lt;")
             .replace(">", "&gt;")
             .replace('"', "&quot;")
             .replace("'", "&apos;"))

def build_feed(products):
    now = datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S GMT")
    items = []

    for p in products:
        product_id = p.get("id", "")
        title = escape_xml(p.get("titulo", ""))
        desc = escape_xml(p.get("descricao", ""))
        link = f"{BASE_URL}/linha.html?id={escape_xml(product_id)}"
        affiliate = p.get("link_afiliado", "")

        # Imagem do produto:优先 imagem (foto do produto), senão imagem_video_capa
        img = p.get("imagem") or p.get("imagem_video_capa")
        if not img:
            continue

        img_url = f"{BASE_URL}/{img}"
        price = p.get("preco", "")

        # Monta description com HTML para Pinterest
        html_desc = f"<p>{desc}</p>"
        if price:
            html_desc += f"<p><strong>Preço:</strong> {escape_xml(price)}</p>"
        if affiliate:
            html_desc += f'<p><a href="{escape_xml(affiliate)}" rel="nofollow">Ver oferta</a></p>'

        item = f"""  <item>
    <title>{title}</title>
    <link>{link}</link>
    <description>{html_desc}</description>
    <guid isPermaLink="false">{BASE_URL}/item/{escape_xml(product_id)}</guid>
    <pubDate>{now}</pubDate>
    <enclosure url="{img_url}" length="0" type="image/jpeg" />
    <media:content url="{img_url}" medium="image">
      <media:title>{title}</media:title>
      <media:description>{desc}</media:description>
    </media:content>
    <link rel="alternate" type="text/html" href="{affiliate}" />
  </item>"""
        items.append(item)

    feed = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:media="http://search.yahoo.com/mrss/">
  <channel>
    <title>Giga Achadinhos</title>
    <link>{BASE_URL}/</link>
    <description>Os melhores achadinhos e ofertas da Shopee, curadoria independente.</description>
    <lastBuildDate>{now}</lastBuildDate>
{chr(10).join(items)}
  </channel>
</rss>"""
    return feed

def main():
    with open("produtos.json", "r", encoding="utf-8") as f:
        products = json.load(f)

    feed = build_feed(products)

    with open("feed.xml", "w", encoding="utf-8") as f:
        f.write(feed)

    print(f"feed.xml gerado com {len(products)} itens.")

if __name__ == "__main__":
    main()