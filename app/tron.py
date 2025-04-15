from tronpy import Tron
from tronpy.exceptions import AddressNotFound
from tronpy.keys import is_base58check_address
from requests.exceptions import RequestException


class TronClient:
    """Client for interacting with the TRON blockchain."""

    def __init__(self):
        self.client = Tron()

    def get_wallet_info(self, address: str) -> dict:
        """
        Retrieve balance, energy, and bandwidth for a TRON wallet address.

        Args:
            address (str): TRON wallet address in Base58Check format.

        Returns:
            dict: Wallet address, balance, energy, and bandwidth.

        Raises:
            ValueError: For invalid format or address not found.
            ConnectionError: For API/network related issues.
        """
        if not is_base58check_address(address):
            raise ValueError("Invalid Tron address format")

        try:
            acc = self.client.get_account(address)
            resource = self.client.get_account_resource(address)

            return {
                "wallet_address": address,
                "balance": acc.get("balance", 0),
                "energy": resource.get("EnergyLimit", 0),
                "bandwidth": resource.get("free_net_limit", 0),
            }

        except AddressNotFound:
            raise ValueError("Wallet address not found in Tron network")

        except RequestException as e:
            raise ConnectionError(f"Network error when accessing Tron API: {e}")

        except Exception as e:
            raise ConnectionError(f"Unexpected error when fetching wallet info: {e}")
