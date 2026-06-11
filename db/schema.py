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
            department VARCHAR(100),
            role VARCHAR(50),
            UNIQUE(department, role)
        );

        INSERT INTO tbl_role (department, role) VALUES
            ('Information Technology', 'ADMIN'),
            ('Production', 'HEAD'),
            ('Production', 'EMPLOYEE'),
            ('Laboratory', 'HEAD'),
            ('Laboratory', 'EMPLOYEE'),
            ('No Department', 'VIEWER')
            ON CONFLICT (department, role) DO NOTHING; 

        CREATE TABLE IF NOT EXISTS tbl_user(
            user_id SERIAL PRIMARY KEY,
            hostname VARCHAR(100),
            ip_address VARCHAR(50),
            mac_address VARCHAR(50) UNIQUE,
            username VARCHAR(50) NOT NULL,
            password VARCHAR(100) NOT NULL,
            role_id INT REFERENCES tbl_role(role_id)
        );

        CREATE TABLE IF NOT EXISTS tbl_access_point(
            access_id SERIAL PRIMARY KEY,
            access_name VARCHAR(100) UNIQUE
        );

        INSERT INTO tbl_access_point (access_name) VALUES 
                ('Production Records'), ('Manual Entry'), ('Auto Entry - MB'),
                ('Auto Entry - DC'), ('Dashboard'), ('CMF'), ('Audit Trail'), ('Permission Access')
            ON CONFLICT (access_name) DO NOTHING;

        CREATE TABLE IF NOT EXISTS tbl_role_permissions(
            permission_id SERIAL PRIMARY KEY,
            access_id INT REFERENCES tbl_access_point(access_id) ON DELETE CASCADE,
            is_enabled BOOLEAN DEFAULT FALSE,
            role_id INT REFERENCES tbl_role(role_id) ON DELETE CASCADE,
            UNIQUE(role_id, access_id)
        );

        INSERT INTO tbl_role_permissions (role_id, access_id, is_enabled)
            SELECT r.role_id, a.access_id, TRUE
            FROM tbl_role r, tbl_access_point a
            WHERE r.role = 'ADMIN' AND r.department = 'Information Technology'
            ON CONFLICT (role_id, access_id) DO NOTHING;

        CREATE TABLE IF NOT EXISTS tbl_audit_trail(
            id SERIAL PRIMARY KEY,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            user_id INT REFERENCES tbl_user(user_id),
            action_type VARCHAR(50),
            details TEXT
        );
    """)

    # ==========================================
    # 2. PRODUCT CODES (Required for FKs below)
    # ==========================================
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tbl_internal_color_code(
            in_code_no SERIAL PRIMARY KEY,
            color VARCHAR(100),
            code VARCHAR(100) UNIQUE
        );

        CREATE TABLE IF NOT EXISTS tbl_generated_prod_code(
            code_no SERIAL PRIMARY KEY,
            product_code VARCHAR(100) UNIQUE,
            in_code_no INT REFERENCES tbl_internal_color_code(in_code_no)
        );
    """)

    # ==========================================
    # 3. CMF (COLOR MATCHING) MODULE
    # ==========================================
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tbl_cmf_salesman(
            sm_no SERIAL PRIMARY KEY,
            name VARCHAR(100)
        );

        CREATE TABLE IF NOT EXISTS tbl_cmf_color_req(
            color_req_no SERIAL PRIMARY KEY,
            name VARCHAR(100)
        );

        CREATE TABLE IF NOT EXISTS tbl_cmf_process(
            process_no SERIAL PRIMARY KEY,
            name VARCHAR(100)
        );

        CREATE TABLE IF NOT EXISTS tbl_cmf_specification(
            spec_no SERIAL PRIMARY KEY,
            name VARCHAR(100)
        );

        CREATE TABLE IF NOT EXISTS tbl_cmf_add_info(
            info_no SERIAL PRIMARY KEY,
            information_details TEXT
        );

        CREATE TABLE IF NOT EXISTS tbl_cmf(
            id SERIAL PRIMARY KEY,
            cm_no VARCHAR(50) UNIQUE NOT NULL,
            matching_type VARCHAR(50),
            sm_no INT REFERENCES tbl_cmf_salesman(sm_no),
            primary_color VARCHAR(100),
            color_desc TEXT,
            qty_resin_testing VARCHAR(100),
            is_resin_provided BOOLEAN,
            mi_c_resin VARCHAR(100),
            is_sample_available BOOLEAN,
            colorant_type VARCHAR(100),
            is_guide_to_return BOOLEAN,
            temperature VARCHAR(50),
            is_low_cost BOOLEAN,
            remarks TEXT,
            info_no INT REFERENCES tbl_cmf_add_info(info_no),
            user_id INT REFERENCES tbl_user(user_id)
        );

        CREATE TABLE IF NOT EXISTS tbl_cmf_scanned (
            file_id SERIAL PRIMARY KEY,
            cm_no VARCHAR(50) REFERENCES tbl_cmf(cm_no) ON DELETE CASCADE,
            file_name VARCHAR(255),
            file_type VARCHAR(50),
            uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            user_id INT REFERENCES tbl_user(user_id)
        );

        CREATE TABLE IF NOT EXISTS tbl_cmf_dates(
            cm_dates_no SERIAL PRIMARY KEY,
            date_submitted_form_made DATE,
            date_required DATE,
            date_received_lab DATE,
            due_date_lab DATE,
            cm_no VARCHAR(50) REFERENCES tbl_cmf(cm_no) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS tbl_cmf_formula(
            cmf_formula_no SERIAL PRIMARY KEY,
            customer VARCHAR(150),
            finished_product VARCHAR(150),
            resin VARCHAR(100),
            dosage DECIMAL(12,6),
            cm_no VARCHAR(50) REFERENCES tbl_cmf(cm_no) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS tbl_cmf_process02(
            chosen_process_no SERIAL PRIMARY KEY,
            cmf_formula_no INT REFERENCES tbl_cmf_formula(cmf_formula_no) ON DELETE CASCADE,
            process_no INT REFERENCES tbl_cmf_process(process_no)
        );

        CREATE TABLE IF NOT EXISTS tbl_cmf_specification02(
            chosen_spec_no SERIAL PRIMARY KEY,
            cm_no VARCHAR(50) REFERENCES tbl_cmf(cm_no) ON DELETE CASCADE,
            spec_no INT REFERENCES tbl_cmf_specification(spec_no)
        );

        CREATE TABLE IF NOT EXISTS tbl_cmf_pending_completed(
            id SERIAL PRIMARY KEY,
            cm_no VARCHAR(50) REFERENCES tbl_cmf(cm_no),
            matching_type VARCHAR(50),
            reason TEXT,
            prod_code VARCHAR(100),
            code_details TEXT,
            date_submitted DATE,
            ar_no VARCHAR(50),
            ar_date DATE,
            is_completed BOOLEAN DEFAULT FALSE
        );
    """)

    # ==========================================
    # 4. RS & FEEDBACK
    # ==========================================
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tbl_rs(
            id SERIAL PRIMARY KEY,
            rs_no VARCHAR(50) UNIQUE,
            customer VARCHAR(150),
            pieces INT,
            quantity_given DECIMAL(12,6),
            date_form_made DATE,
            date_lab_received DATE,
            date_required DATE,
            due_date DATE,
            color_description TEXT,
            finished_product VARCHAR(150),
            matching_type VARCHAR(50),
            lot_no VARCHAR(100),
            ar_no VARCHAR(50),
            date_sample_received DATE,
            primary_color VARCHAR(100),
            color_desc TEXT,
            resin VARCHAR(100),
            chosen_process_no INT,
            colorant_type VARCHAR(50),
            date_submitted DATE,
            status VARCHAR(50),
            user_id INT REFERENCES tbl_user(user_id),
            cm_no VARCHAR(50) REFERENCES tbl_cmf(cm_no)
        );

        CREATE TABLE IF NOT EXISTS tbl_feedback_details(
            feedback_no SERIAL PRIMARY KEY,
            rm_feedback_no VARCHAR(50),
            status VARCHAR(50),
            comment TEXT,
            box_name VARCHAR(100),
            cm_rs_no INT REFERENCES tbl_rs(id)
        );
    """)

    # ==========================================
    # 5. EXTRUDER FORMULAS
    # ==========================================
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tbl_mb_extruder_formula(
            mb_no SERIAL PRIMARY KEY,
            date DATE,
            code_no INT REFERENCES tbl_generated_prod_code(code_no),
            lot_no VARCHAR(100),
            mixing_time VARCHAR(50),
            matched_by VARCHAR(100),
            weighted_by VARCHAR(100),
            encoded_by VARCHAR(100),
            total_weight DECIMAL(12,4),
            cm_no VARCHAR(50) REFERENCES tbl_cmf(cm_no)
        );

        CREATE TABLE IF NOT EXISTS tbl_mb_extruder_formula02(
            id SERIAL PRIMARY KEY,
            mb_no INT REFERENCES tbl_mb_extruder_formula(mb_no) ON DELETE CASCADE,
            material VARCHAR(150),
            value DECIMAL(12,6),
            weight DECIMAL(12,6)
        );

        CREATE TABLE IF NOT EXISTS tbl_dc_extruder_formula(
            dc_no SERIAL PRIMARY KEY,
            code_no INT REFERENCES tbl_generated_prod_code(code_no),
            date DATE,
            sample_size VARCHAR(100),
            mixing_time VARCHAR(50),
            notes TEXT,
            matched_by VARCHAR(100),
            weighted_by VARCHAR(100),
            encoded_by VARCHAR(100),
            total_weight DECIMAL(12,4),
            cm_no VARCHAR(50) REFERENCES tbl_cmf(cm_no)
        );

        CREATE TABLE IF NOT EXISTS tbl_dc_extruder_formula02(
            id SERIAL PRIMARY KEY,
            dc_no INT REFERENCES tbl_dc_extruder_formula(dc_no) ON DELETE CASCADE,
            material VARCHAR(150),
            value DECIMAL(12,6),
            weight DECIMAL(12,6)
        );
    """)

    # ==========================================
    # 6. MASTER & DAILY FORMULAS
    # ==========================================
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tbl_master_formula(
            form_id SERIAL PRIMARY KEY,
            index_no VARCHAR(100),
            date DATE,
            customer VARCHAR(150),
            product_code VARCHAR(100) REFERENCES tbl_generated_prod_code(product_code),
            prod_color VARCHAR(150),
            dosage DECIMAL(12,6),
            total_concentration DECIMAL(12,6),
            ld DECIMAL(12,6),
            mix_time VARCHAR(100),
            resin VARCHAR(150),
            application VARCHAR(150),
            cm_no VARCHAR(50),
            colormatch_date DATE,
            notes TEXT,
            date_time TIMESTAMP,
            is_deleted BOOLEAN DEFAULT FALSE,
            is_used BOOLEAN DEFAULT FALSE,
            html_code_hex VARCHAR(10),
            cyan DECIMAL(12,6),
            magenta DECIMAL(12,6),
            yellow DECIMAL(12,6),
            black DECIMAL(12,6)
        );

        CREATE TABLE IF NOT EXISTS tbl_master_formula_info(
            id SERIAL PRIMARY KEY,
            sequence_no INT,
            material_code VARCHAR(100),
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

        CREATE TABLE IF NOT EXISTS tbl_formula01(
            form_id SERIAL PRIMARY KEY,
            index_no VARCHAR(100),
            date DATE,
            customer VARCHAR(150),
            product_code VARCHAR(100) REFERENCES tbl_generated_prod_code(product_code),
            prod_color VARCHAR(150),
            dosage DECIMAL(12,6),
            total_concentration DECIMAL(12,6),
            ld DECIMAL(12,6),
            mix_time VARCHAR(100),
            resin VARCHAR(150),
            application VARCHAR(150),
            cm_no VARCHAR(50),
            colormatch_date DATE,
            notes TEXT,
            date_time TIMESTAMP,
            is_deleted BOOLEAN DEFAULT FALSE,
            is_used BOOLEAN DEFAULT FALSE
        );

        CREATE TABLE IF NOT EXISTS tbl_formula02(
            id SERIAL PRIMARY KEY,
            sequence_no INT,
            material_code VARCHAR(100),
            concentration DECIMAL(12,6),
            is_deleted BOOLEAN DEFAULT FALSE,
            form_id INT REFERENCES tbl_formula01(form_id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS tbl_formula_encode(
            encode_id SERIAL PRIMARY KEY,
            form_id INT REFERENCES tbl_formula01(form_id) ON DELETE CASCADE,
            match_by VARCHAR(100),
            encoded_by VARCHAR(100),
            updated_by VARCHAR(100)
        );
    """)

    # ==========================================
    # 7. DAILY PRODUCTION
    # ==========================================
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tbl_production01(
            prod_id SERIAL PRIMARY KEY,
            prod_date DATE,
            index_no VARCHAR(100),
            customer VARCHAR(150),
            prod_code VARCHAR(100),
            prod_color VARCHAR(150),
            dosage DECIMAL(12,6),
            ld DECIMAL(12,6),
            lot_no VARCHAR(100),
            order_no VARCHAR(100),
            colormatch_no VARCHAR(50),
            colormatch_date DATE,
            mix_time VARCHAR(50),
            machine_no VARCHAR(50),
            note TEXT,
            is_deleted BOOLEAN DEFAULT FALSE,
            is_printed BOOLEAN DEFAULT FALSE,
            inventory_c_date DATE,
            form_type VARCHAR(50),
            form_id INT REFERENCES tbl_formula01(form_id),
            user_id INT REFERENCES tbl_user(user_id)
        );

        CREATE TABLE IF NOT EXISTS tbl_production02(
            id SERIAL PRIMARY KEY,
            sequence_no INT,
            material_code VARCHAR(32),
            large_scale DECIMAL(12,6),
            small_scale DECIMAL(12,6),
            total_weight DECIMAL(12,6),
            is_deleted BOOLEAN DEFAULT FALSE,
            total_loss DECIMAL(12,6),
            total_consumption DECIMAL(12,6),
            prod_id INT REFERENCES tbl_production01(prod_id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS tbl_production_quantity(
            quantity_id SERIAL PRIMARY KEY,
            prod_id INT REFERENCES tbl_production01(prod_id) ON DELETE CASCADE,
            quantity_req DECIMAL(12,6),
            quantity_batch DECIMAL(12,6),
            quantity_prod DECIMAL(12,6)
        );

        CREATE TABLE IF NOT EXISTS tbl_production_encode(
            encode_id SERIAL PRIMARY KEY,
            prod_id INT REFERENCES tbl_production01(prod_id) ON DELETE CASCADE,
            prepared_by VARCHAR(128),
            encoded_by VARCHAR(128),
            encoded_on TIMESTAMP,
            confirmation_encoded_on TIMESTAMP
        );
    """)

    # ==========================================
    # 8. RAW MATERIALS
    # ==========================================
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tbl_raw_material_list(
            id SERIAL PRIMARY KEY,
            rm_code VARCHAR(100) UNIQUE
        );

        CREATE TABLE IF NOT EXISTS tbl_rm_incoming(
            id SERIAL PRIMARY KEY,
            date DATE,
            material_code VARCHAR(100) REFERENCES tbl_raw_material_list(rm_code),
            note TEXT
        );
    """)

    # ==========================================
    # 9. PERFORMANCE INDEXES
    # ==========================================
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_cmf_cm_no ON tbl_cmf(cm_no);
        CREATE INDEX IF NOT EXISTS idx_cmf_customer ON tbl_cmf_formula(customer);
        CREATE INDEX IF NOT EXISTS idx_prod01_date ON tbl_production01(prod_date);
        CREATE INDEX IF NOT EXISTS idx_prod01_code ON tbl_production01(prod_code);
        CREATE INDEX IF NOT EXISTS idx_prod01_cust ON tbl_production01(customer);
        CREATE INDEX IF NOT EXISTS idx_formula01_code ON tbl_formula01(product_code);
        CREATE INDEX IF NOT EXISTS idx_master_formula_code ON tbl_master_formula(product_code);
        CREATE INDEX IF NOT EXISTS idx_rs_rs_no ON tbl_rs(rs_no);
    """)

    con.commit()
    cursor.close()
    con.close()