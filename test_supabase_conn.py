import os
import sys

try:
    import psycopg
except Exception as exc:
    print("psycopg import error:", exc)
    sys.exit(2)

host = os.environ.get("SUPABASE_HOST")
port = int(os.environ.get("SUPABASE_PORT", "5432"))
db = os.environ.get("SUPABASE_DB", "postgres")
user = os.environ.get("SUPABASE_USER", "postgres")
password = os.environ.get("SUPABASE_PASSWORD", "")
sslmode = os.environ.get("SUPABASE_SSLMODE", "require")

print("Connecting to:", host, port, db, user, sslmode)

try:
    with psycopg.connect(dbname=db, user=user, password=password, host=host, port=port, sslmode=sslmode) as conn:
        with conn.cursor() as cur:
            cur.execute("select version()")
            print("Server:", cur.fetchone()[0])
    print("OK")
    sys.exit(0)
except Exception as exc:
    print("Connection error:", repr(exc))
    sys.exit(1)

// End of file