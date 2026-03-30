# MySQL Migration & Checkout Features

## What was Changed

### Database Migration
- Fully transitioned the application off of SQLite to **MySQL**. 
- Built connection infrastructure to hook up to `localhost` using `root` and `tiger` for the `vicky` database.
- Implemented robust MySQL schemas inside `init_db()` which automatically creates the `products`, `orders`, and `users` tables, along with executing the initial dataseeding.

### Checkout Enhancements
- Modernized `templates/checkout.html` to display two new inputs:
  1. A required **Manual Delivery Date** selection.
  2. A **Recommended Delivery** input that is permanently auto-calculated to exactly `3 days` from today.
- This information reliably maps back to `app.py` when an order post triggers, recording the specific delivery preferences straight to the `orders` list.

### Intelligent Stock Management
- Implemented `update_stock(cart)` in `app.py`.
- Whenever a user successfully submits a payment and normalizes an order, the system iterates over the items they procured and consistently decrements the MySQL `products` database `Stock` integer for every ordered unit.

## Verification
- Fully validated via a live cart cycle test.
- Checking out 1 unit of Atom Bomb successfully drops its stock from 150 to 149 in the MySQL tables seamlessly.
- You can now navigate to your `localhost:5000` shop locally and interact with your new intelligent, data-driven shop!
