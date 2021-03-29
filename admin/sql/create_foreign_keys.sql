BEGIN;

ALTER TABLE lucky_draw.ticket
    ADD CONSTRAINT ticket_user_id_foreign_key
    FOREIGN KEY (user_id)
    REFERENCES "user" (id)
    ON DELETE CASCADE;

ALTER TABLE lucky_draw.entry
    ADD CONSTRAINT entry_raffle_id_foreign_key
    FOREIGN KEY (raffle_id)
    REFERENCES lucky_draw.raffle (id)
    ON DELETE CASCADE;

ALTER TABLE lucky_draw.entry
    ADD CONSTRAINT entry_ticket_no_foreign_key
    FOREIGN KEY (ticket_no)
    REFERENCES lucky_draw.ticket (ticket_no)
    ON DELETE CASCADE;

ALTER TABLE lucky_draw.entry
    ADD CONSTRAINT entry_user_id_foreign_key
    FOREIGN KEY (user_id)
    REFERENCES "user" (id)
    ON DELETE CASCADE;

ALTER TABLE lucky_draw.result
    ADD CONSTRAINT result_raffle_id_foreign_key
    FOREIGN KEY (raffle_id)
    REFERENCES lucky_draw.raffle (id)
    ON DELETE CASCADE;

ALTER TABLE lucky_draw.result
    ADD CONSTRAINT result_ticket_no_foreign_key
    FOREIGN KEY (ticket_no)
    REFERENCES lucky_draw.ticket (ticket_no)
    ON DELETE CASCADE;

ALTER TABLE lucky_draw.result
    ADD CONSTRAINT result_user_id_foreign_key
    FOREIGN KEY (user_id)
    REFERENCES "user" (id)
    ON DELETE CASCADE;

COMMIT;
