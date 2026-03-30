# Task List

- [ ] Verify MySQL connectivity with given credentials
- [ ] Install `pymysql`
- [ ] Update `app.py` to use MySQL instead of SQLite
- [ ] Implement database initialization script (create DB `vicky` or root, create tables `products`, `users`, `orders`, and seed products)
- [ ] Modify `templates/checkout.html` to add manual delivery time input
- [ ] Modify `templates/checkout.html` to add recommended delivery time (auto-calculated as current day + 3 days)
- [ ] Update `/checkout` and `/payment` routes in `app.py` to handle the new delivery time fields
- [ ] Update `/payment` route in `app.py` to decrease product `Stock` based on cart quantities
- [ ] Verify checkout and stock reduction functionality
