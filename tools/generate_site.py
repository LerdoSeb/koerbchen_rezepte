#!/usr/bin/env python3
import os, csv, json, argparse

def html_escape(s):
    return (s or "").replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")

def make_recipe_html(recipe):
    json_ld = {
        "@context": "https://schema.org",
        "@type": "Recipe",
        "name": recipe["title"],
        "description": recipe.get("description",""),
        "recipeYield": recipe.get("servings",""),
        "totalTime": recipe.get("total_time_iso",""),
        "recipeIngredient": recipe["ingredients"],
        "recipeInstructions": [{"@type":"HowToStep","text": s} for s in recipe["steps"]],
        "keywords": ", ".join(recipe.get("tags", [])) if recipe.get("tags") else ""
    }
    ingredients_list = "\n".join(f"<li>{html_escape(i)}</li>" for i in recipe["ingredients"])
    steps_list = "\n".join(f"<li>{html_escape(s)}</li>" for s in recipe["steps"])
    tags_badges = " ".join(f"<span class='tag'>{html_escape(t)}</span>" for t in recipe.get("tags", [])) if recipe.get("tags") else ""
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html_escape(recipe["title"])}</title>
<script type="application/ld+json">
{json.dumps(json_ld, ensure_ascii=False, indent=2)}
</script>
<style>
body{{font-family:system-ui,-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;max-width:800px;margin:40px auto;padding:0 16px;line-height:1.5;}}
h1{{font-size:1.8rem;margin-bottom:0.25rem}}
.desc{{color:#444;margin-top:0.25rem;margin-bottom:1rem}}
.meta{{color:#666;font-size:0.9rem;margin-bottom:1rem}}
.tags .tag{{display:inline-block;background:#eee;border-radius:999px;padding:2px 10px;margin-right:6px;font-size:0.8rem}}
.section-title{{margin-top:1.2rem}}
.card{{border:1px solid #e5e5e5;border-radius:12px;padding:16px}}
</style>
</head>
<body>
  <a href="../index.html">← All recipes</a>
  <h1>{html_escape(recipe["title"])}</h1>
  <p class="desc">{html_escape(recipe.get("description",""))}</p>
  <div class="meta">Servings: {html_escape(recipe.get("servings","—"))} &middot; Total time: {html_escape(recipe.get("total_time_iso","—"))}</div>
  <div class="tags">{tags_badges}</div>

  <h2 class="section-title">Ingredients</h2>
  <div class="card">
    <ul>
      {ingredients_list}
    </ul>
  </div>

  <h2 class="section-title">Steps</h2>
  <div class="card">
    <ol>
      {steps_list}
    </ol>
  </div>
</body>
</html>"""
    return html

def make_index(recipes, site_dir):
    items = []
    for r in recipes:
        items.append(f"<li><a href='recipes/{html_escape(r['slug'])}.html'>{html_escape(r['title'])}</a></li>")
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Recipe Index</title>
<style>
body{{font-family:system-ui,-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;max-width:800px;margin:40px auto;padding:0 16px;line-height:1.5;}}
h1{{font-size:1.8rem;margin-bottom:1rem}}
ul{{line-height:2}}
</style>
</head>
<body>
  <h1>Recipes</h1>
  <p>Open each recipe and use your device's Share menu to import into Körbchen.</p>
  <ul>
    {''.join(items)}
  </ul>
</body>
</html>"""
    with open(os.path.join(site_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)

def main():
    parser = argparse.ArgumentParser(description="Generate a mini-site of recipes for Körbchen bulk import")
    parser.add_argument("--csv", required=True, help="Path to recipes CSV")
    parser.add_argument("--out", required=True, help="Output site directory")
    args = parser.parse_args()

    os.makedirs(os.path.join(args.out, "recipes"), exist_ok=True)

    recipes = []
    with open(args.csv, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            ingredients = [x.strip() for x in (row.get("ingredients_pipe_separated","").split("|")) if x.strip()]
            steps = [x.strip() for x in (row.get("steps_pipe_separated","").split("|")) if x.strip()]
            tags = [x.strip() for x in (row.get("tags_comma_separated","").split(",")) if x.strip()]
            recipe = {
                "slug": row["slug"],
                "title": row["title"],
                "description": row.get("description",""),
                "servings": row.get("servings",""),
                "total_time_iso": row.get("total_time_iso",""),
                "ingredients": ingredients,
                "steps": steps,
                "tags": tags
            }
            recipes.append(recipe)
            # write page
            page_html = make_recipe_html(recipe)
            with open(os.path.join(args.out, "recipes", f"{recipe['slug']}.html"), "w", encoding="utf-8") as f2:
                f2.write(page_html)

    # index
    make_index(recipes, args.out)

if __name__ == "__main__":
    main()
