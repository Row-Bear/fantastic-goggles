from decimal import Decimal
from stellar_sdk import TransactionBuilder, Server, Network, Keypair, Account, asset
import os
import sys
from stellar_sdk.operation.create_claimable_balance import Claimant

STELLAR_USE_TESTNET = 'USE_STELLAR_TEST_NET' in os.environ
STELLAR_ENDPOINT = "https://horizon-testnet.stellar.org" if STELLAR_USE_TESTNET else "https://horizon.stellar.org"
STELLAR_PASSPHRASE = Network.TESTNET_NETWORK_PASSPHRASE  if STELLAR_USE_TESTNET else Network.PUBLIC_NETWORK_PASSPHRASE

if STELLAR_USE_TESTNET:
    print("Using stellar testnet")

PUBLIC_KEY = os.environ['REWARD_PUBLIC_KEY']

server = Server(horizon_url=STELLAR_ENDPOINT)

def fetch_account_balance(pubKey = PUBLIC_KEY):
    """
    Returns the balance of the given account available to be send 
    """
    try:
        acc = server.accounts().account_id(PUBLIC_KEY).call()
    except:
        print(f"Specified account ({pubKey}) does not exists")
        return 0
    balance = 0
    
    for b in acc['balances']:
        if b['asset_type'] == 'native':
            balance = float(b['balance'])
            break
    
    balance -= 0.5 * (2 + acc['subentry_count']) # base reserve
    return balance

def generate_reward_tx(rewardee):
    """
    Generates transaction XDR full of claimable balance operations
    takes tewardee (array of tuples (pub_key, amount)) where pub_key is str and amount is float
    returns XDR as string
    """
    source_acc = Account(account_id=PUBLIC_KEY, sequence=1) # fetch sequence or will it be used with a fee bump?

    tx = TransactionBuilder(
        source_account=source_acc,
        network_passphrase=STELLAR_PASSPHRASE,
        base_fee=100)\
            .add_text_memo("Lumenaut reward!")
    
    for rewarded in rewardee:
        reward = round(rewarded[1], 7)
        if reward <= 0:
            continue

        tx.append_create_claimable_balance_op(
            asset=asset.Asset.native(), 
            amount=str(reward),
            claimants=[Claimant(rewarded[0])]
        )

    xdr = tx.set_timeout(30).build().to_xdr()

    return xdr

def validate_pub_key(pub_key: str):
    """
    Valids a public key
    Returns true if valid key
    """
    try:
        Keypair.from_public_key(pub_key)
        return True
    except:
        return False