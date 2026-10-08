alter table orders add column delivery_window text not null default 'morning'
    check (delivery_window in ('morning', 'afternoon', 'evening'));
