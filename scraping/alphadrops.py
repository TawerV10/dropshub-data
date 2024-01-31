from loguru import logger
import requests
import json

ALL_DATA = []

url = "https://api.typedream.com/v0/app/proxy_public/1e17facc-56e9-4158-9522-8cfee85931a9/notion"

headers = {
    "authority": "api.typedream.com",
    "accept": "application/json, text/plain, */*",
    "accept-language": "en-US,en;q=0.9",
    "content-type": "application/json",
    "dnt": "1",
    "origin": "https://www.alphadrops.net",
    "referer": "https://www.alphadrops.net/",
    "sec-ch-ua": '"Not_A Brand";v="8", "Chromium";v="120", "Avast Secure Browser";v="120"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "cross-site",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Avast/120.0.0.0",
}

json_data = {
    "url": "https://api.notion.com/v1/databases/d444d4b8-15ae-43fe-9eeb-a2035cdde8d9/query",
    "method": "POST",
    "header": {
        "Content-Type": "application/json",
        "Notion-Version": "2021-08-16",
    },
    "body": {
        "filter": {
            "property": "Status",
            "multi_select": {"does_not_contain": "finished"},
        },
        "sorts": [{"property": "Number", "direction": "ascending"}]
    },
}

def extract_data(data):
    for project in data['results']:
        try:
            title = []
            for name in project['properties']['Project']['title']:
                title.append(name['text']['content'])

            tags = []
            for tag in project['properties']['Category']['multi_select']:
                tags.append(tag['name'])

            invest = []
            for inv in project['properties']['Funding']['rich_text']:
                try:
                    invest.append(inv['text']['content'])
                except:
                    invest.append(None)

            network = []
            for netw in project['properties']['Blockchains']['multi_select']:
                network.append(netw['name'])

            status = []
            for stat in project['properties']['Status']['multi_select']:
                status.append(stat['name'])

            description = []
            for desc in project['properties']['About']['rich_text']:
                description.append(desc['text']['content'])

            strategy = []
            for strat in project['properties']['Strategy']['rich_text']:
                strategy.append(strat['text']['content'])

            website = project['properties']['Website']['url']
            discord = project['properties']['Community']['url']

            logo = []
            for img in project['properties']['Cover']['files']:
                try:
                    logo.append(img['external']['url'])
                except:
                    logo.append(img['file']['url'])

            print(title, tags, invest, network, status, description, strategy, website, discord, logo)
            clean_data(title, tags, invest, network, status, description, strategy, website, discord, logo)

        except Exception as ex:
            print(ex)

def clean_data(title, tags, invest, network, status, description, strategy, website, discord, logo):
    clean_title = title[0].strip() if title and title[0] is not None else None

    # Converting tags to normal case (first symbol is upper and others are lower)
    if tags:
        if len(tags) > 1:
            clean_tags = ', '.join([f'{word[0].upper()}{word[1:].lower()}' for word in tags])
        else:
            clean_tags = tags[0][0].upper() + tags[0][1:].lower()
    else:
        clean_tags = None

    # Dealing with numbers
    if invest and invest[0] is not None and invest[0] != '-' and 'Undisclosed' not in invest[0] and invest[0] != 'NA':
        value = invest[0].replace('$', '')
        if 'M' not in value:
            if 'K' in value:
                value = value.replace('K', '000')

            result = f'{float(float(value) / 10 ** 6):.2f}'
            result = result.rstrip("0") if result[-1] == '0' else result
            result = result.replace(".", "") if result[-1] == '.' else result
            clean_invest = f'{result}M'
        else:
            clean_invest = value
    else:
        clean_invest = None

    clean_network = ', '.join(network) if network and network[0] is not None else None
    clean_status = ', '.join(status) if status and status[0] is not None else None

    clean_description = description[0].strip() if description and description[0] is not None else None
    clean_strategy = strategy[0].strip() if strategy and strategy[0] is not None else None

    clean_website = website.strip() if website and website is not None else None
    clean_discord = discord.strip() if discord and discord is not None else None
    clean_logo = logo[0].strip() if logo and logo[0] is not None else None

    text = {
        'title': clean_title,
        'tags': clean_tags,
        'invest': clean_invest,
        'network': clean_network,
        'status': clean_status,
        'description': clean_description,
        'strategy': clean_strategy,
        'website': clean_website,
        'discord': clean_discord,
        'logo': clean_logo,
    }

    ALL_DATA.append(text)

def write_json(text):
    with open('..data/alphadrops.json', 'w', encoding='utf-8') as file:
        json.dump(text, file, indent=4, ensure_ascii=False)

def main():
    for i in range(2):
        if i == 1:
            json_data['body']["start_cursor"] = "f0c7046f-02e3-4f9a-abad-0ff449164724"

        r = requests.post(url=url, headers=headers, json=json_data)
        status_code = r.status_code

        if status_code == 200:
            extract_data(r.json())
        else:
            logger.error(f'alphadrops : {status_code}')

    write_json(ALL_DATA)

if __name__ == '__main__':
    main()
