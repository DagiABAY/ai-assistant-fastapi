import requests


class BankingService:

    BASE_URL = "http://localhost:8080"

    # =====================================================
    # GET ALL ACCOUNTS BALANCE BY PHONE
    # =====================================================
    def get_balances_by_phone(self, phone_number: str):

        url = f"{self.BASE_URL}/api/getBalanceByPhone/{phone_number}"

        response = requests.get(url)

        if response.status_code == 200:
            return response.json()  # list of accounts

        return []

    # =====================================================
    # GET ALL ACCOUNT DETAILS BY PHONE
    # =====================================================
    def get_account_info_by_phone(self, phone_number: str):

        url = f"{self.BASE_URL}/api/getAccountDetailsByPhone/{phone_number}"

        response = requests.get(url)

        if response.status_code == 200:
            return response.json()  # list of accounts

        return []
    
    # =====================================================
    # GET ALL ACCOUNT LIST BY PHONE
    # =====================================================
    
    def get_account_list_by_phone(self, phone_number: str):

        url = f"{self.BASE_URL}/api/getListOfAccounts/{phone_number}"

        response = requests.get(url)

        if response.status_code == 200:
            return response.json()  # list of accounts

        return []

    def get_account_name(self, account_number: str):

        url = f"{self.BASE_URL}/api/getNameOnAccount/{account_number}"

        response = requests.get(url)

        if response.status_code == 200:
            return response.json()  # list of accounts

        return []