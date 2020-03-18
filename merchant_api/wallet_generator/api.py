from merchant_api.bip32_ducatus import generate_mnemonic, DucatusWallet, create_wallet
from merchant_api.payment_requests.models import DucatusRootKey, MerchantShop


def create_merchant(name, address):
    merchant = MerchantShop()
    root = create_root()
    merchant.name = name
    merchant.duc_address = address
    merchant.root_keys = root
    merchant.save()

    return merchant


def create_root():
    new_root = DucatusRootKey()
    seed = generate_mnemonic()
    wallet = create_wallet(seed=seed)
    new_root.key_public = wallet['xpublic_key']
    new_root.key_private = wallet['xprivate_key']
    new_root.save()

    return new_root
