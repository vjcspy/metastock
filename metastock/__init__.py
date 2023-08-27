import os
from dotenv import load_dotenv

from rich.console import Console
from rich.table import Table

# Xác định môi trường hiện tại ("development" hoặc "production")
current_env = os.environ.get('ENVIRONMENT')

# Tải các biến môi trường từ tệp .env tương ứng với môi trường hiện tại
if current_env == 'development':
    load_dotenv('.env.development')
elif current_env == 'production':
    load_dotenv('.env.production')
else:
    load_dotenv('.env.development')

table = Table(title = "Environment")

table.add_column("Key", justify = "left", style = "cyan", no_wrap = True)
table.add_column("Value", style = "magenta")

for key, value in os.environ.items():
    # Kiểm tra nếu tên biến môi trường bắt đầu bằng PS_
    if key.startswith("PS_"):
        table.add_row(key, value)

console = Console()
console.print(table)
