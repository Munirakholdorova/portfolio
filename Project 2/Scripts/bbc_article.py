import requests
import trafilatura
import csv
import time
import json

# BBC article URLs
urls = [
    'https://www.bbc.co.uk/news/articles/c04vqzp6x31o',
    'https://www.bbc.co.uk/news/articles/c709r8ekn8no',
    'https://www.bbc.co.uk/news/articles/cq50n5pd2ejo',
    'https://www.bbc.co.uk/news/articles/c0mpzpv3mw7o',
    'https://www.bbc.co.uk/news/articles/cjw95lyyp0vo',
    'https://www.bbc.co.uk/news/articles/c5ypk7zjg84o',
    'https://www.bbc.co.uk/news/articles/c0mx99ple17o',
    'https://www.bbc.co.uk/news/articles/czr1mkml406o',
    'https://www.bbc.co.uk/news/articles/cly7y9ldr4zo',
    'https://www.bbc.co.uk/news/articles/czxnppz3yplo',
    'https://www.bbc.co.uk/news/articles/cly17egjryxo',
    'https://www.bbc.co.uk/news/articles/c740vjrp81po',
    'https://www.bbc.co.uk/news/articles/cwy8ee2w73jo',
    'https://www.bbc.co.uk/news/articles/cx2jnldejrko',
    'https://www.bbc.co.uk/news/articles/cj6xe89z92po',
    'https://www.bbc.co.uk/news/articles/cy850zn36pqo',
    'https://www.bbc.co.uk/news/articles/c5y5379djl3o',
    'https://www.bbc.co.uk/news/articles/cy404wyemd9o',
    'https://www.bbc.co.uk/news/articles/cy8j6dz2428o',
    'https://www.bbc.co.uk/news/articles/cy85zrlp81mo',
    'https://www.bbc.co.uk/news/articles/cewyj8y0dzjo',
    'https://www.bbc.co.uk/news/articles/cr5r6dz1yj8o',
    'https://www.bbc.co.uk/news/articles/ckgjd9933k9o',
    'https://www.bbc.co.uk/news/articles/clyxkd3neveo',
    'https://www.bbc.co.uk/news/articles/c625p0g23vzo',
    'https://www.bbc.co.uk/news/articles/c8e40rree3zo',
    'https://www.bbc.co.uk/news/articles/cx2n3z03yrro',
    'https://www.bbc.co.uk/news/articles/cy9xzdnw924o',
    'https://www.bbc.co.uk/news/articles/cg4rr76lkvro',
    'https://www.bbc.co.uk/news/articles/c20rrdjvpexo',
    'https://www.bbc.co.uk/news/articles/czryl2118z0o',
    'https://www.bbc.co.uk/news/articles/cj615p5y5kko',
    'https://www.bbc.co.uk/news/articles/cy5e635wwd7o',
    'https://www.bbc.co.uk/news/articles/ce397y7zlyeo',
    'https://www.bbc.co.uk/news/articles/c4g2wjx797po',
    'https://www.bbc.co.uk/news/articles/cy75erndlm5o',
    'https://www.bbc.co.uk/news/articles/cql2de3l61lo',
    'https://www.bbc.co.uk/news/articles/cwy66peqqzxo',
    'https://www.bbc.co.uk/news/articles/cr5830j5yljo',
    'https://www.bbc.co.uk/news/articles/c8de54drq80o',
    'https://www.bbc.co.uk/news/articles/cn7x8k2y4kdo',
    'https://www.bbc.co.uk/sport/football/articles/ce8q01d56v7o',
    'https://www.bbc.co.uk/news/articles/cjw2yw51pn0o',
    'https://www.bbc.co.uk/news/articles/cwyez0y6kvlo',
    'https://www.bbc.co.uk/news/articles/cpv4k837xg8o',
    'https://www.bbc.co.uk/news/articles/cq6y276p743o',
    'https://www.bbc.co.uk/news/articles/c4gpw6v6r14o',
    'https://www.bbc.co.uk/news/articles/c1lv153ydm6o',
    'https://www.bbc.co.uk/news/articles/cpvmzm7z04zo',
    'https://www.bbc.co.uk/news/articles/cdjgrgn7yy9o',
    'https://www.bbc.co.uk/news/articles/czj70ynpm8po',
    'https://www.bbc.co.uk/news/articles/c7v6jvpgyy9o',
    'https://www.bbc.co.uk/news/articles/cy78v6dzj41o',
    'https://www.bbc.co.uk/news/articles/cn7kd2l3m10o',
    'https://www.bbc.co.uk/news/articles/cwyql2llqylo',
    'https://www.bbc.co.uk/news/articles/c7854d3p3wjo',
    'https://www.bbc.co.uk/news/articles/cy07ke5g5g1o',
    'https://www.bbc.co.uk/news/articles/cr4ze0x3z0wo',
    'https://www.bbc.co.uk/news/uk-england-norfolk-68685165',
    'https://www.bbc.co.uk/news/uk-northern-ireland-68669224',
    'https://www.bbc.co.uk/news/uk-england-gloucestershire-67101727',
    'https://www.bbc.co.uk/news/articles/c0je7nxx2v9o',
    'https://www.bbc.co.uk/news/uk-england-birmingham-65929536',
    'https://www.bbc.co.uk/news/uk-england-somerset-65311650',
    'https://www.bbc.co.uk/news/uk-england-lincolnshire-62826181',
    'https://www.bbc.co.uk/news/uk-england-tees-56815659',
    'https://www.bbc.co.uk/news/articles/clydd7zeye7o',
    'https://www.bbc.co.uk/news/business-49710817',
    'https://www.bbc.co.uk/news/articles/c5y26w3pwqxo',
    'https://www.bbc.co.uk/news/uk-england-berkshire-46468378',
    'https://www.bbc.co.uk/news/uk-scotland-43010553',
    'https://www.bbc.co.uk/news/uk-scotland-glasgow-west-41173909',
    'https://www.bbc.co.uk/news/world-africa-40715307',
    'https://www.bbc.co.uk/news/uk-wales-north-east-wales-39454215',
    'https://www.bbc.co.uk/news/articles/c93nk3dry4eo',
    'https://www.bbc.co.uk/news/uk-scotland-edinburgh-east-fife-38084165',
    'https://www.bbc.co.uk/news/uk-wales-north-east-wales-36062701',
    'https://www.bbc.co.uk/news/uk-northern-ireland-35104939',
    'https://www.bbc.co.uk/news/uk-wales-south-west-wales-35072413',
    'https://www.bbc.co.uk/news/uk-34047686',
    'https://www.bbc.co.uk/news/uk-northern-ireland-30389325',
    'https://www.bbc.co.uk/news/uk-scotland-north-east-orkney-shetland-27187157',
    'https://www.bbc.co.uk/news/uk-england-kent-26852557',
    'https://www.bbc.co.uk/news/uk-scotland-glasgow-west-26838914',
    'https://www.bbc.co.uk/news/uk-scotland-glasgow-west-25934579',
    'https://www.bbc.co.uk/news/uk-england-surrey-25153642',
    'https://www.bbc.co.uk/news/world-middle-east-25127368',
    'https://www.bbc.co.uk/news/uk-england-lancashire-24537577',
    'https://www.bbc.co.uk/news/uk-scotland-highlands-islands-24397541',
    'https://www.bbc.co.uk/news/uk-northern-ireland-24231490',
    'https://www.bbc.co.uk/news/uk-england-surrey-23765353',
    'https://www.bbc.co.uk/news/uk-scotland-highlands-islands-23550801',
    'https://www.bbc.co.uk/news/uk-23535938'
]

# Safari User-Agent for Apple M1
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Apple M1; Mac OS X 13_6) "
                  "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15"
}

# Open CSV file for writing
csv_file = open('bbc_articles.csv', 'w', newline='', encoding='utf-8')
writer = csv.writer(csv_file)
writer.writerow(['URL', 'Title', 'Date', 'Text'])

# Loop through URLs
for url in urls:
    print("Processing:", url)
    try:
        # Download page HTML
        response = requests.get(url, headers=headers, timeout=10)
        html = response.text

        # Extract article with Trafilatura
        downloaded = trafilatura.extract(html, output_format='json')
        
        if downloaded:
            data = json.loads(downloaded)
            title = data.get('title', '')
            text = data.get('text', '')
            date = data.get('date', '')
        else:
            title = ''
            text = ''
            date = ''
            print("Failed to extract:", url)
            
    except Exception as e:
        print("Error processing", url, "-", e)
        title = ''
        text = ''
        date = ''

    # Write to CSV
    writer.writerow([url, title, date, text])

    # Sleep 1 second to prevent server blocking
    time.sleep(1)

csv_file.close()
print("Done! Articles saved to bbc_articles.csv")
