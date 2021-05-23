import environ
from stellar_sdk import Network

env = environ.Env()

environ.Env.read_env(".env")

SQLITE3_ENABLED = env.bool("SQLITE3_ENABLED", True)
DATABASE_NAME = env.str("DATABASE_NAME", "votes.db")

SENTRY_ENABLED = env.bool("SENTRY_ENABLED", True)

STELLAR_USE_TESTNET = env.bool("STELLAR_USE_TESTNET", False)
STELLAR_ENDPOINT = "https://horizon-testnet.stellar.org" if STELLAR_USE_TESTNET else "https://horizon.stellar.org"
STELLAR_PASSPHRASE = Network.TESTNET_NETWORK_PASSPHRASE if STELLAR_USE_TESTNET else Network.PUBLIC_NETWORK_PASSPHRASE
BASE_FEE = env.int("BASE_FEE", 10000)
REWARD_PUBLIC_KEY = env.str("REWARD_PUBLIC_KEY")

REACTION_TO_COMPARE = env.json("REACTION_TO_COMPARE", ["🐻"])
LEADERBOARD_LIMIT = env.int("LEADERBOARD_LIMIT", 10)
DISCORD_BOT_TOKEN = env.str("DISCORD_BOT_TOKEN")
REQUIRED_ROLE_ID = env.int("REQUIRED_ROLE_ID")
NOTIFY_USER = env.int("NOTIFY_USER")
DISCORD_WHITELIST_CHANNELS = env.json("DISCORD_WHITELIST_CHANNELS", [])
