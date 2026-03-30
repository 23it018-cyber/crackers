import os
import requests
from duckduckgo_search import DDGS
from app import RAW_PRODUCTS

def get_image_for_product(name, category):
    safe_name = name.replace(' ', '_').replace('/', '_') + '.jpg'
    return os.path.join('static', 'images', 'products', safe_name)

def download_image(query, filepath):
    try:
        results = DDGS().images(
            keywords=f"{query} firework cracker india sivakasi",
            region="wt-wt",
            safesearch="off",
            size="Medium",
            color="color",
            type_image="photo",
            layout="Square",
            license_image="any",
            max_results=1,
        )
        if results:
            image_url = results[0].get('image')
            if image_url:
                response = requests.get(image_url, timeout=10)
                if response.status_code == 200:
                    with open(filepath, 'wb') as f:
                        f.write(response.content)
                    return True
    except Exception as e:
        print(f"Failed to download image for {query}: {e}")
    return False

if __name__ == '__main__':
    base_dir = os.path.join('static', 'images', 'products')
    os.makedirs(base_dir, exist_ok=True)
    count = 0
    
    # We only process a few just to be safe, or all of them if the user requested
    for cat, items in RAW_PRODUCTS:
        for item in items:
            filepath = get_image_for_product(item, cat)
            print(f"Fetching image for {item}...")
            # If the file exists, it's a placeholder. We want to overwrite it.
            success = download_image(item, filepath)
            if success:
                print(f" -> Success")
                count += 1
            else:
                print(f" -> Failed")
                
    print(f"\nSuccessfully downloaded {count} real images.")
