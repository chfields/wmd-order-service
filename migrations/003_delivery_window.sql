alter table orders add column if not exists delivery_window text not null default 'morning'
    check (delivery_window in ('morning', 'afternoon', 'evening'));
