import os

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

ADMINS = [390959255, ]
BOT_TOKEN = os.getenv("BOT_TOKEN")
PGUSER = os.getenv("PGUSER")
PGPASSWORD = os.getenv("PGPASSWORD")
DATABASE = os.getenv("DATABASE")
DBHOST = os.getenv("DBHOST")

POSTGRES_URI = f"postgresql://{PGUSER}:{PGPASSWORD}@{DBHOST}/{DATABASE}"

# if __name__ == '__main__':
# print(NASTAVNIK_SECRET_KEY)
