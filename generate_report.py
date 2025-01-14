import os
import json
import pandas as pd
import matplotlib.pyplot as plt

PAGES_DIR = 'pages'
TAGS_FILE = 'tags.json'

# Load tags from file
if os.path.exists(TAGS_FILE):
    with open(TAGS_FILE, 'r') as file:
        tags_data = json.load(file)
else:
    tags_data = {}

# Initialize data structures
page_data = []

# Gather data
for page in os.listdir(PAGES_DIR):
    page_path = os.path.join(PAGES_DIR, page)
    if os.path.isfile(page_path):
        size = os.path.getsize(page_path)
        page_name = page.replace('.md', '')
        tags = tags_data.get(page_name, [])
        page_data.append({'Page': page_name, 'Size': size, 'Tags': tags})

# Convert to DataFrame
df = pd.DataFrame(page_data)

# Summary Statistics
total_pages = len(df)
total_size = df['Size'].sum()
tags_summary = df.explode('Tags')['Tags'].value_counts()

# Print Summary
print(f'Total Pages: {total_pages}')
print(f'Total Size: {total_size} bytes')
print('\nPages by Tags:')
print(tags_summary)

# Generate Graph
plt.figure(figsize=(10, 5))
tags_summary.plot(kind='bar')
plt.title('Pages by Tags')
plt.xlabel('Tags')
plt.ylabel('Number of Pages')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('pages_by_tags.png')
plt.show()