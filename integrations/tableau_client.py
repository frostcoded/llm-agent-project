# integrations/tableau_client.py

import tableauserverclient as TSC
from typing import Dict, List


class TableauClient:
    """
    Handles interaction with Tableau Server or Tableau Cloud via TSC API.
    """

    def __init__(self, config: Dict[str, str]):
        self.server_url = config.get("server_url")
        self.site = config.get("site", "")
        self.username = config.get("username")
        self.password = config.get("password")
        self.token_name = config.get("token_name")
        self.token_value = config.get("token_value")

        self.auth = self._build_auth()
        self.server = TSC.Server(self.server_url, use_server_version=True)

    def _build_auth(self):
        if self.token_name and self.token_value:
            return TSC.PersonalAccessTokenAuth(self.token_name, self.token_value, self.site)
        else:
            return TSC.TableauAuth(self.username, self.password, self.site)

    def list_dashboards(self) -> List[str]:
        with self.server.auth.sign_in(self.auth):
            all_workbooks, _ = self.server.workbooks.get()
            return [wb.name for wb in all_workbooks]

    def get_dashboard_views(self, workbook_name: str) -> List[str]:
        with self.server.auth.sign_in(self.auth):
            all_workbooks, _ = self.server.workbooks.get()
            for wb in all_workbooks:
                if wb.name == workbook_name:
                    self.server.workbooks.populate_views(wb)
                    return [v.name for v in wb.views]
            return []
