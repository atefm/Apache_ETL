# offer_id SERIAL PRIMARY KEY,

CREATE_OFFERS_TABLE_SQL = """
    CREATE TABLE IF NOT EXISTS offers (
    offer_id INTEGER NOT NULL,
    offer_created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    offer_valid_from TIMESTAMP WITH TIME ZONE,
    offer_valid_until TIMESTAMP WITH TIME ZONE,
    offer_state VARCHAR(9) NOT NULL,
    offer_national_currency VARCHAR(3) NOT NULL,
    offer_total_quantity_kg DECIMAL NOT NULL,
    transaction_type VARCHAR(17) NOT NULL,
    seller_user_id INTEGER NOT NULL,
    unit_price_nationalcurrency DECIMAL NOT NULL);
    """

CREATE_INVITES_TABLE_SQL = """
    CREATE TABLE IF NOT EXISTS invites (
    offer_id INTEGER NOT NULL,
    invite_id INTEGER NOT NULL,
    invite_created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    invite_invitation_state VARCHAR(7) NOT NULL,
    invite_state VARCHAR(8) NOT NULL,
    invite_first_viewed_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    invite_material_id INTEGER,
    invite_min_deal_quantity_kg DECIMAL NOT NULL,
    invite_max_deal_quantity_kg DECIMAL NOT NULL,
    selling_company_id INTEGER,
    buying_org_id INTEGER NOT NULL);
    """

CREATE_DEALS_TABLE_SQL = """
    CREATE TABLE IF NOT EXISTS deals (
    invite_id INTEGER NOT NULL,
    deal_id INTEGER NOT NULL,
    deal_created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    deal_status VARCHAR(7) NOT NULL,
    deal_material_id INTEGER NOT NULL,
    deal_quantity_kg DECIMAL NOT NULL,
    deal_price_kg_nationalcurrency DECIMAL NOT NULL,
    deal_valid_from TIMESTAMP WITH TIME ZONE,
    deal_valid_to TIMESTAMP WITH TIME ZONE);
    """

CREATE_ORDERS_TABLE_SQL = """
    CREATE TABLE IF NOT EXISTS orders (
    deal_id INTEGER NOT NULL,
    order_id INTEGER NOT NULL,
    order_created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    order_placed_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    order_quantity_kg DECIMAL NOT NULL,
    ordering_user_id INTEGER NOT NULL,
    order_price_kg_nationalcurrency DECIMAL NOT NULL);
    """

COPY_CSV_DATA_TO_DB = """
    COPY {} 
    FROM stdin 
    DELIMITER ',' 
    CSV header;
    """

TRUNCATE_TABLE = """
    TRUNCATE TABLE {};
    """
