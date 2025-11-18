-- Adminer 5.4.2-dev PostgreSQL 16.10 dump

DROP TABLE IF EXISTS "alembic_version";
CREATE TABLE "public"."alembic_version" (
    "version_num" character varying(32) NOT NULL,
    CONSTRAINT "alembic_version_pkc" PRIMARY KEY ("version_num")
)
WITH (oids = false);


DROP TABLE IF EXISTS "bulk_invoice_statuses";
DROP SEQUENCE IF EXISTS bulk_invoice_statuses_id_seq;
CREATE SEQUENCE bulk_invoice_statuses_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 START 4 CACHE 1;

CREATE TABLE "public"."bulk_invoice_statuses" (
    "id" integer DEFAULT nextval('bulk_invoice_statuses_id_seq') NOT NULL,
    "random_dir_name" character varying(500),
    "status" character varying(100),
    CONSTRAINT "bulk_invoice_statuses_pkey" PRIMARY KEY ("id")
)
WITH (oids = false);

INSERT INTO "bulk_invoice_statuses" ("id", "random_dir_name", "status") VALUES
(1,	'09a7d618c2f94cd3af894c7856862748',	'Uploaded'),
(2,	'5f16e2bf8b7740e4a37b9dfcde52d8ba',	'Processed'),
(3,	'466d225604f44289b258165ab3b82b1e',	'Processed');

DROP TABLE IF EXISTS "companies";
DROP SEQUENCE IF EXISTS companies_id_seq;
CREATE SEQUENCE companies_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 START 2 CACHE 1;

CREATE TABLE "public"."companies" (
    "id" integer DEFAULT nextval('companies_id_seq') NOT NULL,
    "name" character varying(255) NOT NULL,
    "address" character varying(500) NOT NULL,
    "phone" character varying(50),
    "email" character varying(100),
    CONSTRAINT "companies_pkey" PRIMARY KEY ("id")
)
WITH (oids = false);

INSERT INTO "companies" ("id", "name", "address", "phone", "email") VALUES
(1,	'PT Pranala Ragam Karya',	'Tanggerang',	'085714148343',	'rezaaawp@gmail.com');

DROP TABLE IF EXISTS "invoice_items";
DROP SEQUENCE IF EXISTS invoice_items_id_seq;
CREATE SEQUENCE invoice_items_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 START 14 CACHE 1;

CREATE TABLE "public"."invoice_items" (
    "id" integer DEFAULT nextval('invoice_items_id_seq') NOT NULL,
    "description" character varying(500),
    "total" double precision NOT NULL,
    "invoice_id" integer,
    CONSTRAINT "invoice_items_pkey" PRIMARY KEY ("id")
)
WITH (oids = false);

INSERT INTO "invoice_items" ("id", "description", "total", "invoice_id") VALUES
(10,	'Cloud Infrastructure Services (January)',	2000,	6),
(11,	'Additional Storage (500 GB)',	250,	6),
(12,	'Annual Team License Renewal (25 users)',	8500,	7),
(13,	'Premium Support Package',	2000,	7);

DROP TABLE IF EXISTS "invoices";
DROP SEQUENCE IF EXISTS invoices_id_seq;
CREATE SEQUENCE invoices_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 START 8 CACHE 1;

CREATE TABLE "public"."invoices" (
    "id" integer DEFAULT nextval('invoices_id_seq') NOT NULL,
    "invoice_number" character varying(100) NOT NULL,
    "invoice_date" date NOT NULL,
    "invoice_type" character varying(50),
    "company_id" integer,
    "issuer_name" character varying(255),
    "issuer_address" character varying(500),
    "issuer_phone" character varying(50),
    "issuer_email" character varying(100),
    "recipient_name" character varying(255),
    "recipient_address" character varying(500),
    "recipient_phone" character varying(50),
    "recipient_email" character varying(100),
    "subtotal" numeric(12,2),
    "tax_rate" numeric(5,2),
    "tax" numeric(12,2),
    "total" numeric(12,2),
    "terms" text,
    CONSTRAINT "invoices_pkey" PRIMARY KEY ("id")
)
WITH (oids = false);

CREATE UNIQUE INDEX invoices_invoice_number_key ON public.invoices USING btree (invoice_number);

INSERT INTO "invoices" ("id", "invoice_number", "invoice_date", "invoice_type", "company_id", "issuer_name", "issuer_address", "issuer_phone", "issuer_email", "recipient_name", "recipient_address", "recipient_phone", "recipient_email", "subtotal", "tax_rate", "tax", "total", "terms") VALUES
(6,	'CS-9876',	'2024-01-31',	NULL,	NULL,	'CloudScale Services',	'567 Cirrus Street, Seattle, WA 98109',	'+1 (206) 555-9876',	'billing@cloudscaleservices.com',	'TechNova Solutions, Inc.',	'1250 Charleston Road, Mountain View, CA 94043, United States',	'+1 (650) 555-0123',	'info@technovasolutions.com',	2250.00,	10.25,	230.63,	2480.63,	'Payment is due within 30 days'),
(7,	'DT-45678',	'2024-01-07',	NULL,	NULL,	'DevTools Pro',	'789 Coder''s Court, Austin, TX 78701',	'+1 (512) 555-3456',	'accounts@devtoolspro.com',	'TechNova Solutions, Inc.',	'1250 Charleston Road, Mountain View, CA 94043, United States',	'+1 (650) 555-0123',	'info@technovasolutions.com',	10500.00,	8.25,	866.25,	11366.25,	'Payment is due within 30 days');

ALTER TABLE ONLY "public"."invoice_items" ADD CONSTRAINT "invoice_items_invoice_id_fkey" FOREIGN KEY (invoice_id) REFERENCES invoices(id) NOT DEFERRABLE;

-- 2025-11-18 11:43:57 UTC
