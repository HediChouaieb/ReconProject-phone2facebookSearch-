#!/usr/bin/env python3
"""
Facebook GraphQL Account Search Request Simulation
For educational purposes - demonstrates how the request is structured.

WARNING:
- This simulates a request to Facebook's API.
- Only use on accounts you own or have permission to test.
- Respect Facebook's Terms of Service and rate limits.
- Do not use for unauthorized access, scraping, or abuse.
- The tokens/cipher_text below are session-bound and will expire.
"""

import json
import sys
import uuid
import requests


# ============================================================
# CONFIG
# ============================================================

URL = "https://www.facebook.com/api/graphql/"
OUTPUT_TXT = "response.txt"

HEADERS = {
    }


# ============================================================
# PAYLOAD BUILDER
# ============================================================

def build_payload(search_query: str):
    variables_obj = {
        "params": {
            "cipher_text": (
                "AdDOWVT74CFkAja5PDbBSHAIH0V4X_FKWb-r-gQRGthUT-jUwf4FLqSolzwvSMezAWE1IKmRkT6oLy82_o6oI-"
                "BUISBEqTffFFcPrTJ07RzRejWjgyOI89RNcdGZbx6nhZaXZrn1i6WpJfBUE2JNnTh0iegQIbXOgSUxBaYAm-"
                "lapbmWc2ZSvK_3OO4toh4jIcZY-0HmP-Q2DxhuohHLesfhgOoWqJImBJwyAd9_aG12kwIEJpumvzemooWbz4Fg"
                "Dd8qS_CSw4P4LYXbum4"
            ),
            "context": "recover",
            "event_request_id": str(uuid.uuid4()),
            "friend_name": "",
            "search_query": search_query,
            "waterfall_id": str(uuid.uuid4()),
        }
    }

    variables_json = json.dumps(variables_obj, separators=(",", ":"), ensure_ascii=False)

    payload_pairs = [
        ("av", "0"),
        ("__aaid", "0"),
        ("__user", "0"),
        ("__a", "1"),
        ("__req", "c"),
        ("__hs", "20709.HYP:comet_loggedout_pkg.2.1...0"),
        ("dpr", "1"),
        ("__ccg", "EXCELLENT"),
        ("__rev", "1047425783"),
        ("__s", "qhl288:nvzb5n:4q6wcp"),
        ("__hsi", "7685093130246452876"),
        ("__dyn", (
            "7xeUmwlEnwn8K2Wmh0no6u5U4e0yoW3q32360CEbo19oe8hw2nVE4W0qa0FE2awpUO0n24oaEd82lwv89k2C1"
            "Fwc60D85m1mzXwae4UaEW0LobrwmE2eUlwhE2FBwxw4BwqEGdwtU2ewbS1LwTwNwLweq1Iwqo4eEgwro9o5um"
            "Eb8uwm83Ywgo0Vy3mdw"
        )),
        ("__csr", (
            "gHnqGDsBFN9yiN1b9cECtilYCz_mpkmAu49rgGjxiUGaKiGkx9elrgyUG9aGCXhuhR9BmCquD9GCBlQX-ghl"
            "3UhxK4j5K2-i4HK9yuawDuBxyVUXxkwqx63KucwGxS10zUC9wzzoa8888Ey7Q1ywaum227Hwj8swb-0A8eo1"
            "j8oDhk0O81fE0G91B0l-9U065u0a6w4XwAw3rk2uZ7g0dmU1R980vPw0fL6sS0afw72801Cqw17ww1HQ0qqeG74"
            "7Iw093o02ptCw1ry04HV2G782ZAAwEw7Iwzw18e1nw1waa8U-"
        )),
        ("__hsdp", "gdzE4t1LqfEdU34rxKp7c0Co11UowKgW1Aa1wixe0qm091G2601dxw3c80wC"),
        ("__hblp", (
            "0dC0gi1gw5FwaeU6i4UcU1jU8o2bwtE4S0Yawxw2i81h80c3E1qU0B2u0gi084wCw22o5K7o47w8W7U0Le"
            "09Tw9abwiEcE1gE1nU"
        )),
        ("__sjsp", "gdzE9jN51LqfEdU34o3ew47xy2V3E6gE6106Yw"),
        ("__comet_req", "15"),
        ("lsd", "AdSzQO9PQ8nPLSW1Tqy9mBAlDy0"),
        ("jazoest", "22249"),
        ("__spin_r", "1047425783"),
        ("__spin_b", "trunk"),
        ("__spin_t", "1789325180"),
        ("__crn", "comet.fbweb.CometCAAAccountSearchRoute"),
        ("qpl_active_flow_ids", "516759801"),
        ("fb_api_caller_class", "RelayModern"),
        ("fb_api_req_friendly_name", "CAAFBAccountSearchViewQuery"),
        ("server_timestamps", "true"),
        ("variables", variables_json),
        ("doc_id", "27012969198380071"),
        ("fb_api_analytics_tags", '["qpl_active_flow_ids=516759801"]'),
    ]

    return payload_pairs


# ============================================================
# DECODE + PARSE
# ============================================================

def get_text_body(response):
    try:
        return response.text
    except Exception:
        pass

    content = response.content
    enc = response.headers.get("content-encoding", "").lower()
    if "br" in enc:
        try:
            import brotli
            content = brotli.decompress(content)
        except Exception:
            try:
                import brotlicffi as brotli
                content = brotli.decompress(content)
            except Exception:
                pass

    for charset in ("utf-8", "latin-1"):
        try:
            return content.decode(charset)
        except UnicodeDecodeError:
            continue
    return repr(content)


def try_parse_json(text):
    try:
        return json.loads(text)
    except Exception:
        return None


def extract_account_names(data):
    if not isinstance(data, dict):
        return []
    root = data.get("data", {}).get("caa_ar_fb_account_search")
    if not root:
        return []
    names = []
    for acc in root.get("accounts") or []:
        name = acc.get("name")
        if name:
            names.append(name)
    return names


# ============================================================
# BUILD READABLE TXT REPORT (for debugging)
# ============================================================

def build_report(response, search_query):
    lines = []

    def add(s=""):
        lines.append(s)

    text_body = get_text_body(response)
    data = try_parse_json(text_body)

    add("=" * 70)
    add("FACEBOOK GRAPHQL ACCOUNT SEARCH - SIMULATION REPORT")
    add("=" * 70)
    add()
    add(f"Search query : {search_query}")
    add()
    add(f"Status Code      : {response.status_code}")
    add(f"Final URL        : {response.url}")
    add(f"Content-Type     : {response.headers.get('content-type')}")
    add(f"Content-Encoding : {response.headers.get('content-encoding')}")
    add(f"Elapsed          : {response.elapsed.total_seconds():.3f} s")
    add()

    add("-" * 70)
    add("RESPONSE HEADERS (ALL)")
    add("-" * 70)
    for k, v in response.headers.items():
        add(f"{k}: {v}")
    add()

    add("-" * 70)
    add("RESPONSE BODY")
    add("-" * 70)

    if data is not None:
        add("[JSON parsed successfully]")
        add()
        add(json.dumps(data, indent=2, ensure_ascii=False))
        add()

        names = extract_account_names(data)
        add("-" * 70)
        add("ACCOUNT NAMES")
        add("-" * 70)
        if names:
            for i, n in enumerate(names):
                add(f"  [{i}] {n}")
        else:
            add("  (no accounts found)")
    else:
        add("[Response was NOT valid JSON]")
        add("[Raw body below]")
        add()
        add(text_body)

    add()
    add("=" * 70)
    add("END OF REPORT")
    add("=" * 70)
    return "\n".join(lines)


# ============================================================
# MAIN
# ============================================================

def simulate_request(search_query: str, output_path=OUTPUT_TXT):
    payload = build_payload(search_query)

    print(f"[*] Searching for: {search_query}")
    print("[*] Sending POST request to:", URL)
    print()

    try:
        with requests.Session() as session:
            response = session.post(
                URL,
                headers=HEADERS,
                data=payload,
                timeout=30,
                allow_redirects=True,
            )
    except requests.exceptions.RequestException as e:
        print(f"[!] Request failed: {e}")
        return []

    text_body = get_text_body(response)
    data = try_parse_json(text_body)
    names = extract_account_names(data) if data else []

    # ---- Console output: ONLY the names ----
    if names:
        print("Accounts found:")
        for n in names:
            print(n)
    else:
        if data is None:
            print("[!] Response was not JSON "
                  "(tokens probably expired, or wrong content-encoding).")
        else:
            print("[!] No accounts found for this number.")

    # ---- Save full debug report ----
    report = build_report(response, search_query)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(report)
    print()
    print(f"[*] Full debug report saved to: {output_path}")

    return names


if __name__ == "__main__":
    number = input("Enter the phone number to search: ").strip()
    if not number:
        print("[!] No number provided.")
        sys.exit(1)
    simulate_request(number, output_path="response.txt")
