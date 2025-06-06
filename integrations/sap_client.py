# integrations/sap_client.py

import requests
from typing import Dict, Any, List


class SAPClient:
    """
    Connects to SAP ERP or S/4HANA via OData APIs to fetch business process data.
    """

    def __init__(self, config: Dict[str, str]):
        self.base_url = config.get("base_url")
        self.username = config.get("username")
        self.password = config.get("password")
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    def _auth(self):
        return (self.username, self.password)

    def get_purchase_orders(self) -> List[Dict[str, Any]]:
        url = f"{self.base_url}/sap/opu/odata/sap/API_PURCHASEORDER_PROCESS_SRV/A_PurchaseOrder"
        response = requests.get(url, auth=self._auth(), headers=self.headers)
        return response.json().get("d", {}).get("results", [])

    def get_sales_orders(self) -> List[Dict[str, Any]]:
        url = f"{self.base_url}/sap/opu/odata/sap/API_SALES_ORDER_SRV/A_SalesOrder"
        response = requests.get(url, auth=self._auth(), headers=self.headers)
        return response.json().get("d", {}).get("results", [])
