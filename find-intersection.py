import re

def clean_name(name):
    """
    Safely cleans restaurant names for matching.
    """
    # 1. Remove tags
    name = re.sub(r'\', '', name)
    
    # 2. Convert to lowercase
    name = name.lower()
    
    # 3. Remove common words that cause mismatching
    for word in ['steakhouse', 'restaurant', 'bar', 'grill', 'nyc']:
        name = name.replace(word, '')
    
    # 4. Remove all non-alphanumeric characters safely
    name = "".join(char for char in name if char.isalnum() or char.isspace())
    
    # 5. Collapse extra spaces
    return " ".join(name.split())

def get_restaurant_list(file_path):
    restaurants = {}
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                original = line.strip()
                # Skip empty lines or lines that are just source markers
                if not original or original.startswith('= original
        return restaurants
    except FileNotFoundError:
        print(f"Error: {file_path} not found.")
        return {}

def main():
    # Load both files
    file1_data = get_restaurant_list('all-restaurants.txt')
    file2_data = get_restaurant_list('michelin-restaurants.txt')

    if not file1_data or not file2_data:
        print("Check if your .txt files are in the same folder as this script.")
        return

    # Find the intersection
    intersection_keys = set(file1_data.keys()) & set(file2_data.keys())

    # Sort and save results
    intersected_restaurants = sorted([file1_data[key] for key in intersection_keys])

    with open('intersection.txt', 'w', encoding='utf-8') as f:
        for res in intersected_restaurants:
            f.write(f"{res}\n")

    print(f"Done! Found {len(intersected_restaurants)} matches.")
    print("Results are in intersection.txt")

if __name__ == "__main__":
    main()