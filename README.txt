Körbchen Bulk Import — Route B+
=================================
This bundle helps you bulk-import ~60 recipes into Körbchen via its web-import (Share Sheet).

What’s inside
-------------
/site/                  A ready-to-publish mini-site with sample recipes
  index.html
  /recipes/*.html
/templates/
  recipes_template.csv  -> Fill this with your dishes (one row per recipe)
/tools/
  generate_site.py      -> Builds pages from the CSV

Quick start
-----------
1) Open /templates/recipes_template.csv and replace the sample rows with your ~60 dishes.
   - Columns:
     slug                        unique, lowercase, dash-separated (e.g., "chili-con-carne")
     title                       human title
     description                 short
     servings                    e.g., "4 servings"
     total_time_iso              ISO 8601 duration, e.g., PT30M (30 minutes), PT1H10M (1h 10m)
     ingredients_pipe_separated  separate items with | (pipe)
     steps_pipe_separated        separate steps with | (pipe)
     tags_comma_separated        optional comma list (e.g., "kid-friendly,30-min")
2) Run the generator to rebuild the mini-site:
     python tools/generate_site.py --csv templates/recipes_template.csv --out site
3) Publish /site anywhere (GitHub Pages, Netlify, Vercel, local file server).
   - GitHub Pages: push /site into a repository and enable Pages.
4) Import into Körbchen on your phone:
   - iOS: Open the site in Safari → open a recipe page → Share → "Open in Körbchen" (or copy URL and share).
          Repeat for each link (quick).
   - Android: Open in Chrome → Share → Körbchen.
   Körbchen reads the JSON-LD and auto-fills title/ingredients/steps.

Notes
-----
• Each recipe page includes schema.org/Recipe JSON-LD for maximum parser compatibility.
• You can adjust styling; the JSON-LD is what Körbchen uses.
• If you want me to auto-populate the CSV from a plain list of dish names, I can draft ingredients/steps for you.
