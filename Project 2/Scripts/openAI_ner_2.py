import pandas as pd
from tqdm import tqdm
from collections import Counter
from openai import OpenAI

# -------------------- CONFIG --------------------
INPUT_FILE = "bbc_london_illegal_work_articles.csv"
OUTPUT_FILE = "bbc_articles_with_illegal_work_sectors.csv"

# Initialize OpenAI client

import getpass

my_api_key = getpass.getpass("Please past your key here:")

#specifying client amd prompt

client = OpenAI(api_key = my_api_key)

# -------------------------------------------------

# -------------------- STEP 1: Load CSV --------------------
df = pd.read_csv(INPUT_FILE)
df['illegal_work_sectors'] = None  # create new column

# -------------------- STEP 2: Define OpenAI NER function --------------------
def extract_illegal_work_sectors_openai(article_text):
    """
    Extract all sectors mentioned in the context of illegal/undocumented/unauthorized work.
    Each sector counted once per article.
    """
    prompt = f"""
You are an information extraction assistant. 

Task: Identify all sectors that are explicitly mentioned 
in the following article text in the context of illegal, undocumented, or unauthorized work, 
or working without a permit.  

- Only produce sectors where the text clearly relates to illegal or unauthorized work.
- Return the result as a comma-separated list
- Include each sector only once per article.
- Do not include anything else (no numbers, dates, info or extra text).

Article text:
\"\"\"
{article_text}
\"\"\"
"""

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    # Extract sectors from the response
    output_text = response.choices[0].message.content.strip()
    sector_list = [s.strip().lower() for s in output_text.split(",") if s.strip()]
    return list(set(sector_list))  # unique per article

# -------------------- STEP 3: Apply OpenAI NER --------------------
print("Extracting illegal-work-related sectors from articles...")
for idx, row in tqdm(df.iterrows(), total=len(df)):
    text = row['text']
    sectors_found = extract_illegal_work_sectors_openai(text)
    df.at[idx, 'illegal_work_sectors'] = sectors_found

# -------------------- STEP 4: Count sectors once per article --------------------
sector_counts = Counter()
for sectors_in_article in df['illegal_work_sectors']:
    if sectors_in_article:
        sector_counts.update(set(sectors_in_article))

print("\nIllegal-work-related sector counts (once per article):")
for sector, count in sector_counts.items():
    print(f"{sector}: {count}")

# -------------------- STEP 5: Save enhanced CSV --------------------
# Only keep the columns needed: title, year, illegal_work_sectors
df_final = df[['title', 'year', 'illegal_work_sectors']]
df_final.to_csv(OUTPUT_FILE, index=False, encoding="utf-8")
print(f"\nCSV saved as: {OUTPUT_FILE}")
