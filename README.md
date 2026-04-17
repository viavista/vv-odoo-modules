# ViaVista Odoo Modules

Open-source Odoo 19 modules by [Viavista d.o.o.](https://viavista.ba)

## Modules

| Module | Summary | License |
|--------|---------|---------|
| [l10n_ba](l10n_ba/) | Chart of accounts, taxes and fiscal positions for Bosnia and Herzegovina | AGPL-3 |
| [l10n_ba_account_pdv](l10n_ba_account_pdv/) | KIF, KUF, Form P VAT and D VAT for Bosnia and Herzegovina | AGPL-3 |
| [l10n_ba_account_statement_import](l10n_ba_account_statement_import/) | Import bank statements for Bosnian banks (MT940, XML) | AGPL-3 |
| [mail_telegram](mail_telegram/) | Send messages to Telegram from Odoo | LGPL-3 |
| [viavista_blog](viavista_blog/) | Consistent blog cover image display (aspect-ratio) and per-device cover visibility | LGPL-3 |
| [viavista_monitoring_logs](viavista_monitoring_logs/) | Enhanced error tracking with RPC error capture, log retention, and backup agent integration | LGPL-3 |
| [viavista_product_brand](viavista_product_brand/) | Add brand to products with logos, search and group by | LGPL-3 |
| [viavista_script_runner](viavista_script_runner/) | Run Python scripts from within Odoo with dry-run, timeout, change tracking, and full audit logging | LGPL-3 |
| [viavista_ui](viavista_ui/) | Per-warehouse stock on product kanban and per-user hidden menus | LGPL-3 |

## Installation

Clone this repository into your Odoo addons path:

```bash
git clone https://github.com/viavista/viavista-odoo-modules.git
```

Add the path to your Odoo configuration:

```ini
[options]
addons_path = /path/to/viavista-odoo-modules,...
```

Then install the desired module from **Settings > Technical > Modules**.

## Requirements

- Odoo 19.0 (Community or Enterprise)
- Python 3.12+
- PostgreSQL 14+

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

Each module declares its own license in its `__manifest__.py`.
Most modules are [LGPL-3.0](LICENSE); the Bosnia and Herzegovina localization
modules (`l10n_ba*`) are licensed under **AGPL-3** in line with OCA
localization conventions.
