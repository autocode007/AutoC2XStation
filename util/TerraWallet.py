from terra_sdk.client.lcd import LCDClient
from terra_sdk.client.lcd.api.tx import CreateTxOptions
from terra_sdk.core.wasm import MsgExecuteContract
from terra_sdk.key.mnemonic import MnemonicKey


class TerraWallet:
    terra = LCDClient("https://lcd.terra.dev", "phoenix-1")

    def __init__(self, mnemonic: str):
        mk = MnemonicKey(mnemonic=mnemonic)
        self.wallet = TerraWallet.terra.wallet(mk)

    def get_address(self):
        return self.wallet.key.acc_address

    @classmethod
    def check_balance(self, contract_address, wallet_address):
        result = TerraWallet.terra.wasm.contract_query(contract_address, {"balance": {"address": wallet_address}})
        print(result)

    def send_token(self, contract_address, to_address, amount):
        msg = MsgExecuteContract(sender=self.get_address(), contract=contract_address, execute_msg={
            "transfer": {
                "amount": str(amount),
                "recipient": to_address
            }
        })
        send_tx = self.wallet.create_and_sign_tx(
            CreateTxOptions(
                msgs=[
                    msg
                ],
                gas_adjustment=1,
            )
        )
        tx_result = TerraWallet.terra.tx.broadcast(send_tx)
        print(tx_result)

if __name__ == '__main__':
    terra_wallet = TerraWallet("alarm collect scheme proud expose erode swim oppose can casual chase error")
    print(terra_wallet.get_address())
    # print(TerraWallet.terra.bank.balance("terra1l32fwnqtk768l4vmth5d4t0euvk60h858sd90c"))
    TerraWallet.check_balance("terra1srp2u95kxps35nvan88gn96nfqhukqya2d0ffc",
                              "terra1l32fwnqtk768l4vmth5d4t0euvk60h858sd90c")
    # terra_wallet.send_token("terra1srp2u95kxps35nvan88gn96nfqhukqya2d0ffc", "terra1l32fwnqtk768l4vmth5d4t0euvk60h858sd90c")
