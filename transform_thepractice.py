import os
import re
import glob

BASE_DIR = "/Users/gabrielalvespardin/Projetos/the-practice"
RAW_PAGES_DIR = "/tmp/thepractice_raw_pages"
RAW_FRAMER_DIR = "/tmp/thepractice_raw_framer"
OUT_FRAMER_DIR = os.path.join(BASE_DIR, "assets", "framer")

os.makedirs(OUT_FRAMER_DIR, exist_ok=True)

def localize_asset_urls(text):
    # 1. CMS binary database URLs inside .mjs modules
    text = re.sub(
        r'new URL\([\"\x27`]\./([^\"\x27`]+\.framercms)[\"\x27`]\s*,\s*[\"\x27`]https://framerusercontent\.com/modules/[^\"\x27`]+[\"\x27`]\)\.href\.replace\([\"\x27`]/modules/[\"\x27`]\s*,\s*[\"\x27`]/cms/[\"\x27`]\)',
        r'new URL("/assets/cms/\1",location.origin).href',
        text
    )

    # 2. Framer site bundle URLs (.mjs, .json)
    text = text.replace(
        "https://framerusercontent.com/sites/5TRvxnNUmgmvZzluKM8KFv/",
        "/assets/framer/"
    )

    # 3. Videos (.mp4)
    text = re.sub(
        r'https?://framerusercontent\.com/assets/([a-zA-Z0-9_\-]+\.mp4)',
        r'/assets/videos/\1',
        text
    )

    # 4. Fonts (.woff2 from framerusercontent/assets, fontshare, or fonts.gstatic.com)
    text = re.sub(
        r'https?://framerusercontent\.com/assets/([a-zA-Z0-9_\-]+\.woff2)',
        r'/assets/fonts/\1',
        text
    )
    text = re.sub(
        r'https?://framerusercontent\.com/third-party-assets/fontshare/[^\s\"\x27`<>\\)]+/([a-zA-Z0-9_\-]+\.woff2)',
        r'/assets/fonts/\1',
        text
    )
    text = re.sub(
        r'https?://fonts\.gstatic\.com/[^\s\"\x27`<>\\)]+/([a-zA-Z0-9_\-]+\.woff2)',
        r'/assets/fonts/\1',
        text
    )

    # 5. PNG assets under /assets/
    text = re.sub(
        r'https?://framerusercontent\.com/assets/([a-zA-Z0-9_\-]+\.png)',
        r'/assets/images/\1',
        text
    )

    # 6. Images under /images/ (with or without query parameters)
    text = re.sub(
        r'https?://framerusercontent\.com/images/([a-zA-Z0-9_\-]+\.[a-zA-Z0-9]+)(?:\?[^\s\"\x27`<>\\)]*)?',
        r'/assets/images/\1',
        text
    )

    return text

print("--- 1. Transforming 115 Framer Runtime Modules (.mjs & .json) ---")
for src_path in sorted(glob.glob(os.path.join(RAW_FRAMER_DIR, "*"))):
    fname = os.path.basename(src_path)
    dest_path = os.path.join(OUT_FRAMER_DIR, fname)
    with open(src_path, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()

    content = localize_asset_urls(content)

    # Patch static .framercms range reader so full-file HTTP 200 responses slice cleanly
    if 'Unexpected response length' in content:
        content = content.replace(
            'if(l.length!==i)throw Error(`Request failed: Unexpected response length`);',
            'if(l.length!==i)return t.map(e=>l.slice(e.from,e.to));'
        )
        print(f"  [PATCHED] {fname} (static .framercms byte-range slicer)")

    # Specific runtime patches for framer.C04ER222.mjs
    if fname == "framer.C04ER222.mjs":
        # Patch co(e,t) so any CMS image URL or relative path resolves to local /assets/images/ without query string
        old_co = 'function co(e,t){try{let n=new URL(e);return t?n.searchParams.set(`scale-down-to`,`${t}`):n.searchParams.delete(`scale-down-to`),n.toString()}catch{return e}}'
        new_co = 'function co(e,t){return typeof e=="string"?e.replace(/^https?:\\/\\/framerusercontent\\.com\\/images\\/([^?#]+).*$/,"/assets/images/$1"):e}'
        assert old_co in content, "old_co not found in framer.C04ER222.mjs"
        content = content.replace(old_co, new_co)

        # Patch fo(e,t,n) so it returns clean local src and no broken scale-down-to srcSet
        old_fo = 'function fo(e,t,n){if(![`auto`,`lossless`].includes(t.preferredSize??``))return{src:n,srcSet:void 0};if(e){let r=uo(n,t,e);if(!r?.length)return{src:n,srcSet:void 0};let[i,...a]=r;return{src:i?.src,srcSet:a.map(({src:e,scale:t})=>`${e} ${t}x`).join(`, `)}}else return{src:n,srcSet:lo(n,t,so(t.pixelWidth,t.pixelHeight))}}'
        new_fo = 'function fo(e,t,n){return{src:co(n),srcSet:void 0}}'
        assert old_fo in content, "old_fo not found in framer.C04ER222.mjs"
        content = content.replace(old_fo, new_fo)

        # Patch B_(e,t) so CMS responsive images never throw Invalid URL on relative paths and rewrite to local /assets/images/
        old_B = 'function B_(e,t){if(!e||!t?.src)return t;let n=new URL(t.src);return n.searchParams.delete(`scale-down-to`),n.searchParams.delete(`lossless`),{...t,sizes:`min(100vw, ${e.maxWidth-z_(e)}px)`,srcSet:fo(t.nodeFixedSize,t,t.src).srcSet}}'
        new_B = 'function B_(e,t){if(!e||!t?.src)return t;let s=co(t.src);return{...t,src:s,sizes:`min(100vw, ${e.maxWidth-z_(e)}px)`,srcSet:void 0}}'
        assert old_B in content, "old_B not found in framer.C04ER222.mjs"
        content = content.replace(old_B, new_B)

        # Patch Sp(e) so image preloader accepts relative URLs
        content = content.replace('try{new URL(e);let r=new Image;', 'try{new URL(e,location.origin);let r=new Image;')
        print("  [PATCHED] framer.C04ER222.mjs (local image resolver + CMS binary URL mapper)")

    # Specific patch for script_main.DyuqTcwS.mjs: disable Framer badge mount
    if fname == "script_main.DyuqTcwS.mjs":
        old_badge = '(function(){Q&&x(()=>{y(document.getElementById(`__framer-badge-container`),d(p,{},d(_(()=>import(`./PX9hIOIVM.B4rdZQIl.mjs`)))))})})()'
        if old_badge in content:
            content = content.replace(old_badge, '/* badge disabled */')
            print("  [PATCHED] script_main.DyuqTcwS.mjs (disabled Framer watermark badge)")

    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(content)

ROUTE_MAP = {
    "index.html": "index.html",
    "about.html": "about.html",
    "approach.html": "approach.html",
    "therapists.html": "therapists.html",
    "services.html": "services.html",
    "blog.html": "blog.html",
    "contact.html": "contact.html",
    "in-person.html": "in-person.html",
    "locations.html": "locations.html",
    "online.html": "online.html",
    "fees.html": "fees.html",
    "how-it-works.html": "how-it-works.html",
    "faq.html": "faq.html",
    "privacy-policy.html": "privacy-policy.html",
    "cancellation-policy.html": "cancellation-policy.html",
    "accessibility.html": "accessibility.html",
    "terms-of-use.html": "terms-of-use.html",
    "404.html": "404.html",
    "services_individual-therapy.html": "services/individual-therapy.html",
    "services_couples-therapy.html": "services/couples-therapy.html",
    "services_teens-families.html": "services/teens-families.html",
    "services_online-therapy.html": "services/online-therapy.html",
    "blog_how-to-know-when-its-time-to-start-therapy.html": "blog/how-to-know-when-its-time-to-start-therapy.html",
    "blog_anxiety-explained-why-your-body-sounds-the-alarm.html": "blog/anxiety-explained-why-your-body-sounds-the-alarm.html",
    "blog_five-small-habits-for-a-calmer-nervous-system.html": "blog/five-small-habits-for-a-calmer-nervous-system.html",
    "blog_fighting-fair-how-couples-can-repair-after-conflict.html": "blog/fighting-fair-how-couples-can-repair-after-conflict.html",
    "blog_talking-to-your-teen-about-mental-health.html": "blog/talking-to-your-teen-about-mental-health.html",
    "blog_what-to-expect-from-your-first-online-therapy-session.html": "blog/what-to-expect-from-your-first-online-therapy-session.html",
    "therapists_maya-alvarez.html": "therapists/maya-alvarez.html",
    "therapists_daniel-brooks.html": "therapists/daniel-brooks.html",
    "therapists_lina-tran.html": "therapists/lina-tran.html",
    "therapists_jordan-lee.html": "therapists/jordan-lee.html",
    "therapists_simone-carter.html": "therapists/simone-carter.html",
    "therapists_sam-whitaker.html": "therapists/sam-whitaker.html",
}

print("\n--- 2. Transforming 34 HTML Pages (Preserving Native Framer Appear & Runtime) ---")
for src_name, dest_rel in ROUTE_MAP.items():
    src_path = os.path.join(RAW_PAGES_DIR, src_name)
    dest_path = os.path.join(BASE_DIR, dest_rel)
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    with open(src_path, "r", encoding="utf-8", errors="replace") as f:
        html = f.read()

    # Localize all URLs to root-relative /assets/...
    html = localize_asset_urls(html)

    # Strip srcset attributes from SSR <img> tags so browser uses crisp local src
    html = re.sub(r'\ssrcset=[\'"][^\'"]*[\'"]', '', html)

    # Strip ONLY Framer telemetry & editorbar injection script
    html = re.sub(
        r'<script\b[^>]*\bsrc=[\'"][^\'"]*events\.framer\.com[^\'"]*[\'"][^>]*>[\s\S]*?<\/script>',
        '',
        html,
        flags=re.IGNORECASE
    )
    html = re.sub(
        r'<script>try\{if\(localStorage\.getItem\("__framer_force_showing_editorbar_since"\)\)[\s\S]*?<\/script>',
        '',
        html
    )

    # Update canonical and og:url to https://thepractice.landingprofile.com
    html = html.replace("https://thepractice.framer.website", "https://thepractice.landingprofile.com")

    # Normalize all internal relative hrefs (./foo, ../foo, ./) to root-relative (/foo, /)
    # In subpages (services/*, blog/*, therapists/*), ./slug links point within the same collection folder
    depth = dest_rel.count("/")
    if depth == 1:
        folder = dest_rel.split("/")[0]
        # ./couples-therapy -> /services/couples-therapy
        html = re.sub(r'href=[\'"]\./([^\'"#]+)(#[^\'"<>]*)?[\'"]', rf'href="/{folder}/\1\2"', html)
        # ../about -> /about, ../ -> /
        html = re.sub(r'href=[\'"]\.\./([^\'"]*)[\'"]', r'href="/\1"', html)
    else:
        # ./about -> /about, ./ -> /
        html = re.sub(r'href=[\'"]\./([^\'"]*)[\'"]', r'href="/\1"', html)

    # Inject clean CSS override for hiding #__framer-badge-container
    css_link = '<link rel="stylesheet" href="/assets/css/main.css">'
    if '</head>' in html:
        html = html.replace('</head>', f'{css_link}\n</head>')

    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(html)

    # Also write index.html inside services/, blog/, therapists/ so trailing-slash URLs (/therapists/) return 200 natively
    if dest_rel in ("services.html", "blog.html", "therapists.html"):
        folder_index = os.path.join(BASE_DIR, dest_rel[:-5], "index.html")
        os.makedirs(os.path.dirname(folder_index), exist_ok=True)
        with open(folder_index, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"  [OK] {dest_rel[:-5]}/index.html (trailing-slash fallback)")

    print(f"  [OK] {dest_rel}")

print("\n--- Transformation Complete! ---")
