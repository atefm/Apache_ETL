CREATE_OFFERS_TABLE_SQL = """
    DROP TABLE IF EXISTS offers;
    CREATE TABLE offers (
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
    DROP TABLE IF EXISTS invites;
    CREATE TABLE invites (
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
    DROP TABLE IF EXISTS deals;
    CREATE TABLE deals (
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
    DROP TABLE IF EXISTS orders;
    CREATE TABLE orders (
    deal_id INTEGER NOT NULL,
    order_id INTEGER NOT NULL,
    order_created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    order_placed_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    order_quantity_kg DECIMAL NOT NULL,
    ordering_user_id INTEGER NOT NULL,
    order_price_kg_nationalcurrency DECIMAL NOT NULL);
    """

GET_ALL_TABLE_DATA_SQL = """
    SELECT * FROM {};
    """

CREATE_SALES_FUNNEL = """
    CREATE TABLE sales_funnel
    as
    SELECT offers.offer_id, 
        COALESCE(SUM(d.deal_price_kg_nationalcurrency * d.deal_quantity_kg), 0) AS deal_total_price_nationalcurrency, 
        COALESCE(SUM(d.deal_quantity_kg),0) AS deal_total_quantity_kg, 
        COALESCE(SUM(o.order_price_kg_nationalcurrency * o.order_quantity_kg), 0) AS order_total_price_nationalcurrency, 
        COALESCE(SUM(o.order_quantity_kg),0) AS order_total_quantity_kg, 
        offers.offer_created_at, 
        offers.offer_valid_from, 
        offers.offer_valid_until, 
        offers.offer_total_quantity_kg, 
        offers.offer_national_currency, 
        offers.unit_price_nationalcurrency FROM "offers"
    LEFT JOIN invites i
        on (offers.offer_id = i.offer_id AND i.invite_invitation_state !='INVALID')
    LEFT JOIN deals d
        on i.invite_id = d.invite_id 
    LEFT JOIN orders o
        on d.deal_id = o.deal_id
    GROUP BY offers.offer_id, offers.offer_created_at, offers.offer_valid_from, 
        offers.offer_valid_until, offers.offer_total_quantity_kg, 
        offers.offer_national_currency, offers.unit_price_nationalcurrency
    """