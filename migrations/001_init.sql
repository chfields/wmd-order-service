create table orders (
    id uuid primary key,
    user_id text not null,
    status text not null check (status in ('pending', 'confirmed')),
    total_cents integer not null check (total_cents >= 0),
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now()
);

create table order_lines (
    order_id uuid not null references orders (id) on delete cascade,
    product_id text not null,
    name text not null,
    quantity integer not null check (quantity > 0),
    price_cents integer not null check (price_cents >= 0),
    primary key (order_id, product_id)
);

create index orders_user on orders (user_id, created_at desc);
