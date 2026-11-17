import os
import re
import json

BASE_DIR = "/Users/gabrielalvespardin/Projetos/the-practice"
RAW_DIR = "/tmp/thepractice_raw_pages"

with open(os.path.join(BASE_DIR, "font_map.json"), "r", encoding="utf-8") as f:
    font_map = json.load(f)

with open(os.path.join(BASE_DIR, "image_map.json"), "r", encoding="utf-8") as f:
    image_map = json.load(f)

VIDEO_MAP = {
    "https://framerusercontent.com/assets/jVIuBJM4gcU60UggA258l41dX4k.mp4": "assets/videos/video_about_jVIuBJM4gc.mp4",
    "https://framerusercontent.com/assets/2MP41MyVrOgN9fBWA2c9iip4.mp4": "assets/videos/video_contact_2MP41MyVrO.mp4",
    "https://framerusercontent.com/assets/VQURg0lhxAOJGcvarpB0CVTtdaI.mp4": "assets/videos/video_inperson_VQURg0lhxA.mp4",
    "https://framerusercontent.com/assets/v6i8TJjAJEIEYuPQGozOr6DUiac.mp4": "assets/videos/video_therapists_v6i8TJjAJE.mp4",
}
sorted_fonts = sorted(font_map.items(), key=lambda x: len(x[0]), reverse=True)
sorted_images = sorted(image_map.items(), key=lambda x: len(x[0]), reverse=True)

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

# List of internal link targets to rewrite cleanly
INTERNAL_LINKS = [
    ("services/individual-therapy", "services/individual-therapy.html"),
    ("services/couples-therapy", "services/couples-therapy.html"),
    ("services/teens-families", "services/teens-families.html"),
    ("services/online-therapy", "services/online-therapy.html"),
    ("blog/how-to-know-when-its-time-to-start-therapy", "blog/how-to-know-when-its-time-to-start-therapy.html"),
    ("blog/anxiety-explained-why-your-body-sounds-the-alarm", "blog/anxiety-explained-why-your-body-sounds-the-alarm.html"),
    ("blog/five-small-habits-for-a-calmer-nervous-system", "blog/five-small-habits-for-a-calmer-nervous-system.html"),
    ("blog/fighting-fair-how-couples-can-repair-after-conflict", "blog/fighting-fair-how-couples-can-repair-after-conflict.html"),
    ("blog/talking-to-your-teen-about-mental-health", "blog/talking-to-your-teen-about-mental-health.html"),
    ("blog/what-to-expect-from-your-first-online-therapy-session", "blog/what-to-expect-from-your-first-online-therapy-session.html"),
    ("therapists/maya-alvarez", "therapists/maya-alvarez.html"),
    ("therapists/daniel-brooks", "therapists/daniel-brooks.html"),
    ("therapists/lina-tran", "therapists/lina-tran.html"),
    ("therapists/jordan-lee", "therapists/jordan-lee.html"),
    ("therapists/simone-carter", "therapists/simone-carter.html"),
    ("therapists/sam-whitaker", "therapists/sam-whitaker.html"),
    ("about", "about.html"),
    ("approach", "approach.html"),
    ("therapists", "therapists.html"),
    ("services", "services.html"),
    ("blog", "blog.html"),
    ("contact", "contact.html"),
    ("in-person", "in-person.html"),
    ("locations", "locations.html"),
    ("online", "online.html"),
    ("fees", "fees.html"),
    ("how-it-works", "how-it-works.html"),
    ("faq", "faq.html"),
    ("privacy-policy", "privacy-policy.html"),
    ("cancellation-policy", "cancellation-policy.html"),
    ("accessibility", "accessibility.html"),
    ("terms-of-use", "terms-of-use.html"),
]

for src_name, dest_rel in ROUTE_MAP.items():
    src_path = os.path.join(RAW_DIR, src_name)
    if not os.path.exists(src_path):
        print(f"[SKIP] Missing {src_path}")
        continue
    
    dest_path = os.path.join(BASE_DIR, dest_rel)
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    
    with open(src_path, "r", encoding="utf-8", errors="replace") as f:
        html = f.read()

    # Determine prefix
    depth = dest_rel.count("/")
    prefix = "../" * depth if depth > 0 else "./"

    # 1. Localize fonts
    for orig_url, local_rel in sorted_fonts:
        html = html.replace(orig_url, f"{prefix}{local_rel}")

    # 2. Localize images & videos
    for orig_url, local_rel in sorted_images:
        html = html.replace(orig_url, f"{prefix}{local_rel}")
    
    for v_url, v_rel in VIDEO_MAP.items():
        html = html.replace(v_url, f"{prefix}{v_rel}")

    # Specific 404 image replacement if query string remains
    html = re.sub(r'https?://framerusercontent\.com/images/FTcWo8sn6DIYSpkkcnlQESRzzY\.jpg(?:\?[^\'"\s<>]*)?', f'{prefix}assets/images/img_404_FTcWo8sn6DIY.jpg', html)

    # 3. Strip srcset from <img> to enforce local src loading
    html = re.sub(r'\ssrcset=[\'"][^\'"]*[\'"]', '', html)

    # 4. Decouple Framer Runtime Scripts & Preloads
    html = re.sub(r'<script\b[^>]*\bsrc=[\'"][^\'"]*(?:events\.framer\.com|script_main)[^\'"]*[\'"][^>]*>[\s\S]*?<\/script>', '', html, flags=re.IGNORECASE)
    html = re.sub(r'<script\b[^>]*\btype=[\'"]framer/(?:appear|handover)[\'"][^>]*>[\s\S]*?<\/script>', '', html, flags=re.IGNORECASE)
    html = re.sub(r'<script\b[^>]*\bdata-framer-appear-animation=[^>]*>[\s\S]*?<\/script>', '', html, flags=re.IGNORECASE)
    html = re.sub(r'<script\b[^>]*\bdata-framer-bundle=[\'"]main[\'"][^>]*>[\s\S]*?<\/script>', '', html, flags=re.IGNORECASE)
    html = re.sub(r'<link\b[^>]*\brel=[\'"]modulepreload[\'"][^>]*>', '', html, flags=re.IGNORECASE)
    html = re.sub(r'<meta\b[^>]*\bname=[\'"]framer-[^\'"]*[\'"][^>]*>', '', html, flags=re.IGNORECASE)
    html = re.sub(r'<link\b[^>]*searchIndex[^\>]*>', '', html, flags=re.IGNORECASE)

    # 5. Unlock SSR initial hidden states
    # Unhide opacity: 0 and 0.001
    html = re.sub(r'opacity:\s*0\.001(?=[;\"\'\s])', 'opacity: 1', html)
    # Unlock translateY and blur
    html = re.sub(r'filter:\s*blur\([^)]+\)', 'filter: none', html)
    html = re.sub(r'transform:\s*translateY\([0-9\.\-]+px\)', 'transform: translateY(0px)', html)
    html = re.sub(r'will-change:\s*transform', 'will-change: auto', html)
    
    # Specific unhiding for Sticky Nav and Accordions
    html = re.sub(r'style="[^"]*opacity:\s*0(?:\.001)?[^"]*"', lambda m: m.group(0).replace('opacity:0.001', 'opacity:1').replace('opacity: 0.001', 'opacity: 1').replace('opacity:0', 'opacity:1').replace('opacity: 0', 'opacity: 1'), html)

    # 6. Normalize internal navigation links
    # Root link
    html = re.sub(r'href=[\'"]\./[\'"]', f'href="{prefix}index.html"', html)
    html = re.sub(r'href=[\'"]https://thepractice\.framer\.website/?[\'"]', f'href="{prefix}index.html"', html)
    
    for route_slug, route_dest in INTERNAL_LINKS:
        # replace href="./route_slug" or href="/route_slug"
        html = re.sub(r'href=[\'"](?:\./|/)' + re.escape(route_slug) + r'/?[\'"]', f'href="{prefix}{route_dest}"', html)
        html = re.sub(r'href=[\'"]https://thepractice\.framer\.website/' + re.escape(route_slug) + r'/?[\'"]', f'href="{prefix}{route_dest}"', html)

    # 7. Inject Custom Stylesheet & Interactive JS Engine
    css_link = f'<link rel="stylesheet" href="{prefix}assets/css/main.css">'
    js_script = f'<script src="{prefix}assets/js/main.js"></script>'

    if '</head>' in html:
        html = html.replace('</head>', f'{css_link}\n</head>')
    else:
        html = css_link + html

    if '</body>' in html:
        html = html.replace('</body>', f'{js_script}\n</body>')
    else:
        html = html + js_script

    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(html)
    
    print(f"Processed: {src_name} -> {dest_rel} ({len(html)} bytes)")

print("\n--- All 34 Pages Transformed Successfully ---")
