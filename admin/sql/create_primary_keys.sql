BEGIN;

ALTER TABLE "user" ADD CONSTRAINT user_pkey PRIMARY KEY (id);

ALTER TABLE lucky_draw.raffle ADD CONSTRAINT raffle_pkey PRIMARY KEY (id);
ALTER TABLE lucky_draw.ticket ADD CONSTRAINT ticket_pkey PRIMARY KEY (ticket_no);
COMMIT;
