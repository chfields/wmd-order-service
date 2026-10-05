alter table orders add column gift_message text null
    check (gift_message is null or char_length(gift_message) <= 200);
