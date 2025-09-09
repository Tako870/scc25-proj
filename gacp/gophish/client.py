from __future__ import annotations
import requests
from dataclasses import dataclass
from typing import Any, Dict, Optional, List

@dataclass
class GophishClient:
    base_url: str
    api_key: str
    timeout: int = 15

    def _headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    def _url(self, path: str) -> str:
        return f"{self.base_url.rstrip('/')}/api{path}"

    def create_group(self, name: str, recipients: List[Dict[str,str]], dry_run: bool = True) -> Dict[str, Any]:
        payload = {
            "name": name,
            "targets": [
                {
                    "first_name": r.get("first_name",""),
                    "last_name": r.get("last_name",""),
                    "email": r["email"]
                } for r in recipients
            ]
        }
        if dry_run:
            return {"dry_run": True, "endpoint": "/groups/", "payload": payload}
        resp = requests.post(self._url("/groups/"), headers=self._headers(), json=payload, timeout=self.timeout)
        resp.raise_for_status()
        return resp.json()

    def create_template(self, name: str, subject: str, html: str, dry_run: bool = True) -> Dict[str, Any]:
        payload = {"name": name, "subject": subject, "html": html, "text": ""}
        if dry_run:
            return {"dry_run": True, "endpoint": "/templates/", "payload": payload}
        resp = requests.post(self._url("/templates/"), headers=self._headers(), json=payload, timeout=self.timeout)
        resp.raise_for_status()
        return resp.json()

    def create_landing_page(self, name: str, html: str, dry_run: bool = True) -> Dict[str, Any]:
        payload = {"name": name, "html": html, "capture_credentials": True, "capture_passwords": True}
        if dry_run:
            return {"dry_run": True, "endpoint": "/pages/", "payload": payload}
        resp = requests.post(self._url("/pages/"), headers=self._headers(), json=payload, timeout=self.timeout)
        resp.raise_for_status()
        return resp.json()

    def create_campaign(self,
                        name: str,
                        group_ids: List[int],
                        template_id: int,
                        page_id: int,
                        url: str,
                        launch_date: Optional[str] = None,
                        dry_run: bool = True) -> Dict[str, Any]:
        payload = {
            "name": name,
            "groups": [{"id": gid} for gid in group_ids],
            "template": {"id": template_id},
            "page": {"id": page_id},
            "url": url,
        }
        if launch_date:
            payload["launch_date"] = launch_date
        if dry_run:
            return {"dry_run": True, "endpoint": "/campaigns/", "payload": payload}
        resp = requests.post(self._url("/campaigns/"), headers=self._headers(), json=payload, timeout=self.timeout)
        resp.raise_for_status()
        return resp.json()
