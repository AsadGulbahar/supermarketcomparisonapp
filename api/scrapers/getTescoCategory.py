import bs4 as bs

import os
print("Current Directory:", os.getcwd())
with open('TescoCategory.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

# Use BeautifulSoup to parse the HTML
soup = bs.BeautifulSoup(html_content, "html.parser")

def extract_categories(category, depth=0):
    sub_categories = category.find_all("li", recursive=False)
    results = []
    for sub_cat in sub_categories:
        name = " ".join(sub_cat.text.strip().split())
        if "All" in name or "Offers on" in name:
            continue
        if sub_cat.find("ul"):
            print("  " * depth + "Category:", name)
            results += extract_categories(sub_cat.find("ul"), depth + 1)
        else:
            link = sub_cat.find("a", href=True).get('href', 'No link found')
            print("  " * depth + f"- {name} (Link: {link})")
            results.append({'name': name, 'link': link, 'depth': depth})
    return results

# Extract categories from the main menu
category_list = soup.find("ul", class_="menu-superdepartment")
if category_list:
    extract_categories(category_list)
else:
    print("No categories found in the provided HTML content.")