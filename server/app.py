from concurrent.futures import ThreadPoolExecutor, as_completed
from playwright.async_api import async_playwright
from itertools import combinations, product
from flask import Flask, request, jsonify
from dotenv import dotenv_values
from urllib.parse import urlparse
from datetime import datetime, timedelta
import whois
import random
import ssl
import re
import requests
import socket
import asyncio
import base64
import string

config = dotenv_values(".env")
urlhaus_headers = {
    "Auth-Key": config.get("URLHAUS-API-KEY")
}
REGISTRAR_DOMAINS = [
    "godaddy.com",
    "namecheap.com",
    "hostgator.com",
    "bluehost.com",
    "domain.com",
    "porkbun.com",
    "dynadot.com"
]

PARKING_KEYWORDS = [
    "buy this domain",
    "is for sale",
    "domain is parked",
    "this domain has been registered",
    "interested in this domain"
]
redirect_codes = [301, 302, 307, 308]
with open("server/data.txt") as file:
    VALID_TLDS = [v[:-1].lower() for v in file.readlines()]

app = Flask(__name__)


def supports_https(domain, timeout=3):
    try:
        ctx = ssl.create_default_context()
        with socket.create_connection((domain, 443), timeout=timeout) as sock:
            with ctx.wrap_socket(sock, server_hostname=domain):
                return True
    except Exception:
        return False


def check_url(url, timeout=3):
    try:
        r = requests.get(url, timeout=timeout, allow_redirects=True)

        for resp in r.history:
            print("Redirected from:", resp.url.lower())
            loc = resp.headers.get("Location", "").lower()
            if any(registrar in loc for registrar in REGISTRAR_DOMAINS):
                return False

        if any(registrar in r.url.lower() for registrar in REGISTRAR_DOMAINS):
            return False

        content_sample = r.text[:5000].lower()
        if any(re.search(keyword, content_sample) for keyword in PARKING_KEYWORDS):
            return False

        return r.status_code < 400

    except requests.RequestException as e:
        print("Error:", e)
        return False


def process_domain(domain):
    try:
        socket.gethostbyname(domain)  # DNS check
    except socket.gaierror:
        return None

    if supports_https(domain) and check_url(f"https://{domain}"):
        return f"https://{domain}"
    elif check_url(f"http://{domain}"):
        return f"http://{domain}"
    return None


def resolve_url(domains, max_workers=50):
    results = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(process_domain, d): d for d in domains}
        for future in as_completed(futures):
            result = future.result()
            if result:
                results.append(result)
    return results


def is_valid_domain(domain):
    domain = domain.strip()

    if not domain:
        return False

    if domain.startswith('.') or domain.endswith('.'):
        return False

    labels = domain.split('.')

    label_regex = re.compile(r"^(?!-)[A-Za-z0-9-]{1,63}(?<!-)$")
    for label in labels:
        if not label_regex.match(label):
            return False

    if len(domain) > 253:
        return False

    return True


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods',
                         'GET,PUT,POST,DELETE,OPTIONS')
    return response


def build_adjacency(layout):
    adjacency = {}
    # loop over rows
    for row_idx in range(len(layout)):
        row = layout[row_idx]
        # loop over columns
        for col_idx in range(len(row)):
            char = row[col_idx]
            neighbors = []
            # check nearby keys (up, down, left, right, diagonals)
            for i in [-1, 0, 1]:
                for j in [-1, 0, 1]:
                    if i == 0 and j == 0:
                        continue
                    r = row_idx + i
                    c = col_idx + j
                    # make sure we're inside keyboard bounds
                    if 0 <= r < len(layout) and 0 <= c < len(layout[r]):
                        neighbors.append(layout[r][c])
            adjacency[char] = neighbors
    return adjacency


def swap(placeholder, swappedval, i):
    placeholder[i] = swappedval
    return placeholder


def remove_typesquatting(website):
    results = []

    print("----- 1 character removed -----")
    for i in range(len(website)):
        placeholder = list(website)
        del placeholder[i-1]
        results.append("".join(placeholder))

    return results


def duplicate_typesquatting(website):
    results = []

    for i in range(len(website)):
        placeholder = list(website)
        duplicatedchar = placeholder[i]
        placeholder.insert(i+1, duplicatedchar)
        results.append("".join(placeholder))

    return results


def swap_typosquatting(website):
    results = []

    for i, char in enumerate(website):
        if char not in keyboard_adj:  # skip chars not on keyboard
            continue

        new_char = random.choice(keyboard_adj[char])

        # Ensure first char never becomes "-"
        if i == 0:
            while new_char == "-":
                new_char = random.choice(keyboard_adj[char])

        placeholder = list(website)
        placeholder[i] = new_char
        results.append("".join(placeholder))

    return results


def swap2_typosquatting(website):
    results = []

    for i in range(len(website)):
        for j in range(i + 1, len(website)):
            new_placeholder = list(website)

            if website[i] in keyboard_adj:
                neigh_i = random.choice(keyboard_adj[website[i]])
                if i == 0:  # first char should not become "-"
                    while neigh_i == "-":
                        neigh_i = random.choice(keyboard_adj[website[i]])
                new_placeholder[i] = neigh_i

            if website[j] in keyboard_adj:
                neigh_j = random.choice(keyboard_adj[website[j]])
                if j == 0:  # same safety check for j if it’s the first char
                    while neigh_j == "-":
                        neigh_j = random.choice(keyboard_adj[website[j]])
                new_placeholder[j] = neigh_j

            results.append("".join(new_placeholder))

    return results


def leetTranslate(website):
    print("--- Leet ---")
    # Initialise dictionary of letters --> leet
    leet_dict = {
        "A": ["4"],
        "B": ["8", "13"],
        "C": ["<", "(", "C"],
        "D": ["D"],
        "E": ["3"],
        "F": ["F"],
        "G": ["6", "9"],
        "H": ["H"],
        "I": ["1"],
        "J": ["J"],
        "K": ["K"],
        "L": ["1", "L", "7"],
        "M": ["M"],
        "N": ["N"],
        "O": ["0"],
        "P": ["P"],
        "Q": ["Q"],
        "R": ["R", "12"],
        "S": ["5", "2"],
        "T": ["7"],
        "U": ["U", "V"],
        "V": ["V"],
        "W": ["W", "VV"],
        "X": ["X"],
        "Y": ["Y"],
        "Z": ["2", "Z"]
    }

    # Makes a list of the letters in said word
    # Compare it to an existing leetspeak table
    # Dictionary, letter to list of leetspeak chars usable in URLs

    letters = list(website.upper())

    indices_leetable = [i for i, l in enumerate(letters) if l in leet_dict]

    results = set()  # avoid duplicates

    # For i = 1 up to len(indices_leetable)
    for i in range(1, len(indices_leetable) + 1):
        for combo in combinations(indices_leetable, i):
            # For each index in combo, try all possible substitutions
            options = [leet_dict[letters[idx]] for idx in combo]
            for repl in product(*options):
                new_website = letters[:]  # copy original letters
                for idx, sub in zip(combo, repl):
                    new_website[idx] = sub
                results.add("".join(new_website))

    return sorted(results)


def edits1(website):
    "All edits that are one edit away from `website`."
    letters = 'abcdefghijklmnopqrstuvwxyz'
    splits = [(website[:i], website[i:]) for i in range(len(website) + 1)]
    deletes = [L + R[1:] for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
    replaces = [L + c + R[1:] for L, R in splits if R for c in letters]
    inserts = [L + c + R for L, R in splits for c in letters]
    return deletes + transposes + replaces + inserts


def edits2(website):
    "All edits that are two edits away from `website`."
    results = []

    for edit in edits1(website):
        results += edits1(edit)

    return results


keyboard = [  # QWERTY ####
    "1234567890-",
    "qwertyuiop",
    "asdfghjkl",
    "zxcvbnm"
]

keyboard_adj = build_adjacency(keyboard)


def find_squats(website):
    squats_list = remove_typesquatting(website) + duplicate_typesquatting(website) + swap_typosquatting(
        website) + swap2_typosquatting(website) + leetTranslate(website) + edits1(website)

    return squats_list


def check_alive(urls: list):
    alive = []
    for url in urls:
        try:
            request.head(url, timeout=3)
            alive.append(url)
        except TimeoutError:
            continue
    return alive


def ss_bytes(website, ratings):
    if ratings > 80:
        async def capture():
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page()
                # NEED CHANGE "HTTPS" cuz can use http oso and the TLD cannot be hardcoded << alr appended lmao
                await page.goto(f"{website}", wait_until="networkidle")
                img_bytes = await page.screenshot(full_page=True)
                await browser.close()
                return img_bytes

        # Run the async capture function and return bytes
        return asyncio.run(capture())
    else:
        pass

# TO GET BACK IMG
# def save_bytes_to_file(img_bytes, filename="screenshot.png"):
#     with open(filename, "wb") as f:
#         f.write(img_bytes)


def is_valid_tld(s: str) -> bool:
    """
    Check if `s` has a valid top-level domain without using exceptions.
    Cleans up common bad input like trailing punctuation or missing protocol.
    """
    if not isinstance(s, str):
        return False

    # Clean up whitespace and trailing punctuation
    s = s.strip().strip(string.punctuation)
    if not s:
        return False

    # Ensure we have a scheme so urlparse works reliably
    if "://" not in s:
        s = "http://" + s

    netloc = urlparse(s).netloc.lower()
    if not netloc or "." not in netloc:
        return False

    # Extract the last part after the final dot
    tld = netloc.rsplit(".", 1)[-1]
    return tld in VALID_TLDS


def check_domain(domain):
    # Strip scheme if present
    parsed = urlparse(domain)
    domain_name = parsed.netloc or parsed.path

    try:
        w = whois.whois(domain_name)
    except Exception as e:
        return {"domain": domain_name, "error": str(e)}

    # Extract fields safely
    creation_date = None
    if isinstance(w.creation_date, list):
        creation_date = w.creation_date[0]
    else:
        creation_date = w.creation_date

    registrar = w.registrar or ""
    name_servers = w.name_servers or []
    privacy_enabled = any("privacy" in str(w.org).lower() or
                          "privacy" in str(email).lower()
                          for email in (w.emails or []))

    # Suspicious flags
    flags = []
    if creation_date and creation_date > datetime.now() - timedelta(days=30):
        flags.append("RegisterLessThanAMonth")
    if privacy_enabled:
        flags.append("PrivacyEnabled")
    if registrar and "namecheap" in registrar.lower():
        flags.append("AbusiveRegistrar")
    if name_servers and any("cloudflare" in ns.lower() for ns in name_servers):
        flags.append("CloudFlareUse")

    return {
        "domain": domain_name,
        "creation_date": creation_date,
        "registrar": registrar,
        "name_servers": name_servers,
        "flags": flags
    }


@app.route('/squats', methods=["POST"])
def squats():
    # Get JSON data
    data = request.get_json()  # Parse JSON body

    # If there's no body or no website param, error
    if not data or "website" not in data:
        return jsonify({"error": "Missing 'website' attribute"}), 400

    # Store website value in variable
    website = data["website"]

    # Check website for TLD, strip and save

    # This should return a list of possible domains.
    # do each one and then return the final concatenated result
    # Add back the TLD

    domains = set()
    for url in find_squats(website):
        if is_valid_tld(url) and is_valid_domain(url):
            domains.add(url)
    print(len(domains))
    # dont forget to remove the hardcoded[:50] domain limit !IMPORTANT
    domains = resolve_url(list(domains)[:50])
    for url in domains:
        a = check_domain(url)
        if len(a.flags) >= 2:  # stupid hacky ahh function because its 1:30am and my braincell cant think of score values
            ss_bytes(url)
    # insert script to send image over
    # ok so idk how yall are gon manage sending image bytes over to the bingus
    # send domains.url.b64img : b64byte this probavly idk man efuseijodv
    # do note that the stupid domain registrars enforce redirects thru js not by protocol level and its always by sum
    # weird ahh js function and ss sent may not be gut

    response = {"domains": domains}
    return jsonify(response), 200


@app.route('/')
def test():
    b = resolve_url(['yeow.com', 'kfow.com'])
    print(b)
    return b


if __name__ == '__main__':
    app.run(debug=True)
