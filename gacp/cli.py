import argparse, csv, sys
from pathlib import Path
from jinja2 import Template

from .gophish.client import GophishClient
from .enrich.brand import get_brand_info
from .enrich.dns import get_saas_hint
from .schedule.windows import default_launch_iso
from .safety.guards import is_allowed_domain

def load_file(p: Path) -> str:
    return p.read_text(encoding="utf-8")

def main():
    parser = argparse.ArgumentParser(prog="gacp", description="Gophish Auto-Context (MVP)")
    parser.add_argument("--gophish-url", required=True)
    parser.add_argument("--api-key", required=True)
    parser.add_argument("--execute", action="store_true", help="Actually call Gophish API (not just dry-run)")
    sub = parser.add_subparsers(dest="cmd", required=True)

    init = sub.add_parser("init-campaign", help="Create group, template, page, campaign")
    init.add_argument("--campaign-name", required=True)
    init.add_argument("--domain", required=True)
    init.add_argument("--recipients", required=True)
    init.add_argument("--send-start", default=None, help="ISO8601, e.g., 2025-09-12T09:00:00")
    init.add_argument("--phish-url", default="http://phish.example.com", help="Public URL for landing page")

    args = parser.parse_args()

    dry_run = not args.execute
    client = GophishClient(args.gophish_url, args.api_key)

    if args.cmd == "init-campaign":
        if not is_allowed_domain(args.domain):
            print(f"[safety] Domain '{args.domain}' is not in allowlist for MVP. Use example.com/.test/.local.", file=sys.stderr)
            sys.exit(2)

        # Load recipients
        recs = []
        with open(args.recipients, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                if row.get("email"):
                    recs.append(row)

        brand = get_brand_info(args.domain)
        saas = get_saas_hint(args.domain)

        # Prepare email + landing (generic for MVP)
        tmpl_subject = "[Security Notice] Please verify your account activity"
        email_html = Template(Path(__file__).resolve().parent.parent / "templates_email" / "generic_email.j2".read_text(encoding="utf-8")).render(
            first_name="{{first_name}}",  # Gophish will substitute
            company_name=brand.company_name or None,
            landing_url="{{.URL}}"
        )
        page_html = (Path(__file__).resolve().parent.parent / "templates_landing" / "generic_page.html").read_text(encoding="utf-8")

        # Create objects (dry-run by default)
        group_resp = client.create_group(name=f"{args.campaign_name} Group", recipients=recs, dry_run=dry_run)
        tmpl_resp = client.create_template(name=f"{args.campaign_name} Email", subject=tmpl_subject, html=email_html, dry_run=dry_run)
        page_resp = client.create_landing_page(name=f"{args.campaign_name} Page", html=page_html, dry_run=dry_run)

        # Fake IDs for dry-run preview
        group_id = group_resp.get("id", 1)
        template_id = tmpl_resp.get("id", 1)
        page_id = page_resp.get("id", 1)

        launch_iso = default_launch_iso(args.send_start)
        camp_resp = client.create_campaign(
            name=args.campaign_name,
            group_ids=[group_id],
            template_id=template_id,
            page_id=page_id,
            url=args.phish_url,
            launch_date=launch_iso,
            dry_run=dry_run
        )

        print("[group]", group_resp)
        print("[template]", tmpl_resp)
        print("[page]", page_resp)
        print("[campaign]", camp_resp)

if __name__ == "__main__":
    main()
