from db.connection import get_connection


def create_table():
    con = get_connection()
    cursor = con.cursor()

    # ==========================================
    # 1. USER & ACCESS CONTROL MODULE
    # ==========================================
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tbl_role(
            role_id SERIAL PRIMARY KEY,
            department VARCHAR(50) NOT NULL,
            role VARCHAR(20) NOT NULL,
            UNIQUE(department, role)
        );

        CREATE TABLE IF NOT EXISTS tbl_user(
            user_id SERIAL PRIMARY KEY,
            hostname VARCHAR(50),
            ipaddress VARCHAR(50),
            mac VARCHAR(50) UNIQUE,
            username VARCHAR(50) NOT NULL,
            password VARCHAR(100) NOT NULL,
            role_id INT REFERENCES tbl_role(role_id)
        );

        CREATE TABLE IF NOT EXISTS tbl_access_point(
            access_id SERIAL PRIMARY KEY,
            access_name VARCHAR(100) UNIQUE
        );

        CREATE TABLE IF NOT EXISTS tbl_role_permissions(
            permission_id SERIAL PRIMARY KEY,
            role_id INT REFERENCES tbl_role(role_id) ON DELETE CASCADE,
            access_id INT REFERENCES tbl_access_point(access_id) ON DELETE CASCADE,
            is_enabled BOOLEAN DEFAULT FALSE
        );
    """)

    # ==========================================
    # 2. AUDIT TRAIL
    # ==========================================
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tbl_audit_trail(
            id SERIAL PRIMARY KEY,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            user_id INT REFERENCES tbl_user(user_id),
            action_type VARCHAR(50),
            details TEXT
        );
    """)

    # ==========================================
    # 3. CMF (COLOR MATCHING) MODULE
    # ==========================================
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tbl_cmf_salesman(
            sm_no SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL
        );

        CREATE TABLE IF NOT EXISTS tbl_cmf_color_req(
            color_req_no SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL
        );

        CREATE TABLE IF NOT EXISTS tbl_cmf_process(
            process_no SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL
        );

        CREATE TABLE IF NOT EXISTS tbl_cmf_add_info(
            info_no SERIAL PRIMARY KEY,
            information_details TEXT
        );

        CREATE TABLE IF NOT EXISTS tbl_cmf(
            cm_no VARCHAR(20) PRIMARY KEY, -- Usually a formatted string like CMF-2024-001
            matching_type VARCHAR(50),
            sm_no INT REFERENCES tbl_cmf_salesman(sm_no),
            primary_color VARCHAR(50),
            color_desc TEXT,
            color_req_id INT REFERENCES tbl_cmf_color_req(color_req_no),
            qty_resin_testing VARCHAR(50),
            is_resin_provided BOOLEAN DEFAULT FALSE,
            mi_c_resin VARCHAR(50),
            is_sample_available BOOLEAN DEFAULT FALSE,
            colorant_type VARCHAR(50),
            is_guide_to_return BOOLEAN DEFAULT FALSE,
            specification TEXT,
            temperature VARCHAR(20),
            is_low_cost BOOLEAN DEFAULT FALSE,
            remarks TEXT,
            info_no INT REFERENCES tbl_cmf_add_info(info_no),
            user_id INT REFERENCES tbl_user(user_id)
        );

        CREATE TABLE IF NOT EXISTS tbl_cmf_dates(
            cm_dates_no SERIAL PRIMARY KEY,
            date_submitted_form_made DATE,
            date_required DATE,
            date_received_lab DATE,
            due_date_lab DATE,
            cm_no VARCHAR(20) REFERENCES tbl_cmf(cm_no) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS tbl_cmf_pending(
            pending_no SERIAL PRIMARY KEY,
            cm_no VARCHAR(20) REFERENCES tbl_cmf(cm_no),
            reason TEXT,
            is_completed BOOLEAN DEFAULT FALSE
        );

        CREATE TABLE IF NOT EXISTS tbl_cmf_completed(
            completed_no SERIAL PRIMARY KEY,
            pending_no INT REFERENCES tbl_cmf_pending(pending_no),
            code VARCHAR(50),
            date_submitted TIMESTAMP
        );
    """)

    # ==========================================
    # 4. PRODUCT CODES MODULE
    # ==========================================
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tbl_internal_color_code(
            in_code_no SERIAL PRIMARY KEY,
            color VARCHAR(50),
            code VARCHAR(50) UNIQUE
        );

        CREATE TABLE IF NOT EXISTS tbl_generated_prod_code(
            code_no SERIAL PRIMARY KEY,
            product_code VARCHAR(50) UNIQUE,
            in_code_no INT REFERENCES tbl_internal_color_code(in_code_no)
        );
    """)

    # ==========================================
    # 5. EXTRUDER FORMULAS (MB & DC)
    # ==========================================
    cursor.execute("""
        -- Master Batch (MB) Extruder
        CREATE TABLE IF NOT EXISTS tbl_mb_extruder_formula(
            mb_no SERIAL PRIMARY KEY,
            date DATE,
            code_no INT REFERENCES tbl_generated_prod_code(code_no),
            lot_no VARCHAR(50),
            matched_by VARCHAR(100),
            weighted_by VARCHAR(100),
            encoded_by VARCHAR(100),
            total_weight DECIMAL(12,4),
            cm_no VARCHAR(20) REFERENCES tbl_cmf(cm_no)
        );

        CREATE TABLE IF NOT EXISTS tbl_mb_extruder_formula02(
            id SERIAL PRIMARY KEY,
            mb_no INT REFERENCES tbl_mb_extruder_formula(mb_no) ON DELETE CASCADE,
            material VARCHAR(100),
            value DECIMAL(12,4),
            weight DECIMAL(12,4)
        );

        -- Direct Color (DC) Extruder
        CREATE TABLE IF NOT EXISTS tbl_dc_extruder_formula(
            dc_no SERIAL PRIMARY KEY,
            code_no INT REFERENCES tbl_generated_prod_code(code_no),
            date DATE,
            sample_size VARCHAR(50),
            mixing_time VARCHAR(50),
            notes TEXT,
            matched_by VARCHAR(100),
            weighted_by VARCHAR(100),
            encoded_by VARCHAR(100),
            total_weight DECIMAL(12,4),
            cm_no VARCHAR(20) REFERENCES tbl_cmf(cm_no)
        );

        CREATE TABLE IF NOT EXISTS tbl_dc_extruder_formula02(
            id SERIAL PRIMARY KEY,
            dc_no INT REFERENCES tbl_dc_extruder_formula(dc_no) ON DELETE CASCADE,
            material VARCHAR(100),
            value DECIMAL(12,4),
            weight DECIMAL(12,4)
        );
    """)

    # ==========================================
    # 6. MASTER FORMULA & FORMULATION MODULE
    # ==========================================
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tbl_master_formula(
            form_id SERIAL PRIMARY KEY,
            index_no VARCHAR(50),
            date DATE,
            customer VARCHAR(100),
            code_no_prod_code VARCHAR(50),
            prod_color VARCHAR(100),
            dosage DECIMAL(12,4),
            total_concentration DECIMAL(12,4),
            ld DECIMAL(12,4),
            mix_time VARCHAR(50),
            resin VARCHAR(100),
            application VARCHAR(100),
            cm_no VARCHAR(20) REFERENCES tbl_cmf(cm_no),
            colormatch_date DATE,
            notes TEXT,
            date_time TIMESTAMP,
            is_deleted BOOLEAN DEFAULT FALSE,
            is_used BOOLEAN DEFAULT FALSE,
            html_code_hex VARCHAR(7),
            cyan DECIMAL(5,2),
            magenta DECIMAL(5,2),
            yellow DECIMAL(5,2),
            black DECIMAL(5,2)
        );

        CREATE TABLE IF NOT EXISTS tbl_master_formula_info(
            id SERIAL PRIMARY KEY,
            sequence_no INT,
            material_code VARCHAR(50),
            concentration DECIMAL(12,6),
            is_deleted BOOLEAN DEFAULT FALSE,
            form_id INT REFERENCES tbl_master_formula(form_id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS tbl_master_formula_encode(
            encode_id SERIAL PRIMARY KEY,
            form_id INT REFERENCES tbl_master_formula(form_id) ON DELETE CASCADE,
            match_by VARCHAR(100),
            encoded_by VARCHAR(100),
            updated_by VARCHAR(100)
        );

        -- Daily Formulation (Active working table)
        CREATE TABLE IF NOT EXISTS tbl_formulation(
            form_id SERIAL PRIMARY KEY,
            index_no VARCHAR(50),
            date DATE,
            customer VARCHAR(100),
            code_no_prod_code VARCHAR(50),
            prod_color VARCHAR(100),
            dosage DECIMAL(12,4),
            total_concentration DECIMAL(12,4),
            ld DECIMAL(12,4),
            mix_time VARCHAR(50),
            resin VARCHAR(100),
            application VARCHAR(100),
            cm_no VARCHAR(20),
            colormatch_date DATE,
            notes TEXT,
            date_time TIMESTAMP,
            is_deleted BOOLEAN DEFAULT FALSE,
            is_used BOOLEAN DEFAULT FALSE
        );

        CREATE TABLE IF NOT EXISTS tbl_formulation_info(
            id SERIAL PRIMARY KEY,
            sequence_no INT,
            material_code VARCHAR(50),
            concentration DECIMAL(12,6),
            is_deleted BOOLEAN DEFAULT FALSE,
            form_id INT REFERENCES tbl_formulation(form_id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS tbl_formulation_encode(
            encode_id SERIAL PRIMARY KEY,
            form_id INT REFERENCES tbl_formulation(form_id) ON DELETE CASCADE,
            match_by VARCHAR(100),
            encoded_by VARCHAR(100),
            updated_by VARCHAR(100)
        );
    """)

    # ==========================================
    # 7. INDEXES FOR PERFORMANCE
    # ==========================================
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_cmf_no ON tbl_cmf(cm_no);
        CREATE INDEX IF NOT EXISTS idx_master_formula_code ON tbl_master_formula(code_no_prod_code);
        CREATE INDEX IF NOT EXISTS idx_audit_ts ON tbl_audit_trail(timestamp DESC);
    """)

    con.commit()
    cursor.close()
    con.close()