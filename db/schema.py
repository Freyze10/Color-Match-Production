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
                ('Auto Entry - DC'), ('Audit Trail'), ('Permission Access'), ('Dashboard')
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
            WHERE r.role = 'ADMIN' 
              AND r.department = 'Information Technology'
        ON CONFLICT (role_id, access_id) DO NOTHING;
        
        INSERT INTO tbl_role_permissions (role_id, access_id, is_enabled)
            SELECT r.role_id, a.access_id, TRUE
            FROM tbl_role r, tbl_access_point a
            WHERE r.role = 'VIEWER' 
              AND r.department = 'No Department'
              AND a.access_id BETWEEN 1 AND 4
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
    # 2. CMF (COLOR MATCHING) MODULE
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
            matching_type VARCHAR(100),
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

        -- Many-to-Many: CMF to Color Requirements
        CREATE TABLE IF NOT EXISTS tbl_cmf_color_req02(
            chosen_color_req_no SERIAL PRIMARY KEY,
            cm_no VARCHAR(50) REFERENCES tbl_cmf(cm_no) ON DELETE CASCADE,
            color_req_no INT REFERENCES tbl_cmf_color_req(color_req_no)
        );

        CREATE TABLE IF NOT EXISTS tbl_cmf_attachments (
            file_id SERIAL PRIMARY KEY,
            cm_no VARCHAR(50) REFERENCES tbl_cmf(cm_no) ON DELETE CASCADE,
            file_name VARCHAR(255) NOT NULL,        -- Example: "test_result.pdf"
            file_type VARCHAR(50),                 -- Example: "application/pdf"
            file_data BYTEA NOT NULL,               -- THE ACTUAL FILE
            uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            uploaded_by INT REFERENCES tbl_user(user_id)
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

        -- Many-to-Many: CMF Formula to Process
        CREATE TABLE IF NOT EXISTS tbl_cmf_process02(
            chosen_process_no SERIAL PRIMARY KEY,
            cmf_formula_no INT REFERENCES tbl_cmf_formula(cmf_formula_no) ON DELETE CASCADE,
            process_no INT REFERENCES tbl_cmf_process(process_no)
        );
        
        -- Many-to-Many: CMF Formula to Process
        CREATE TABLE IF NOT EXISTS tbl_cmf_specification02(
            chosen_spec_no SERIAL PRIMARY KEY,
            cm_no VARCHAR(50) REFERENCES tbl_cmf(cm_no) ON DELETE CASCADE,
            spec_no INT REFERENCES tbl_cmf_specification(spec_no)
        );

        CREATE TABLE IF NOT EXISTS tbl_cmf_pending(
            pending_no SERIAL PRIMARY KEY,
            cm_no VARCHAR(50) REFERENCES tbl_cmf(cm_no),
            reason TEXT,
            is_completed BOOLEAN DEFAULT FALSE
        );

        CREATE TABLE IF NOT EXISTS tbl_cmf_completed(
            completed_no SERIAL PRIMARY KEY,
            pending_no INT REFERENCES tbl_cmf_pending(pending_no),
            code VARCHAR(100),
            date_submitted DATE
        );

        CREATE TABLE IF NOT EXISTS tbl_feedback(
            feedbackk_no SERIAL PRIMARY KEY,
            cm_no VARCHAR(50) REFERENCES tbl_cmf(cm_no),
            feedback TEXT
        );
    """)

    # ==========================================
    # 3. PRODUCT CODE MODULE
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
    # 4. EXTRUDER FORMULAS (MB & DC)
    # ==========================================
    cursor.execute("""
        -- Master Batch Extruder
        CREATE TABLE IF NOT EXISTS tbl_mb_extruder_formula(
            mb_no SERIAL PRIMARY KEY,
            date DATE,
            code_no INT REFERENCES tbl_generated_prod_code(code_no),
            lot_no VARCHAR(100),
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

        -- Direct Color Extruder
        CREATE TABLE IF NOT EXISTS tbl_dc_extruder_formula(
            dc_no SERIAL PRIMARY KEY,
            code_no INT REFERENCES tbl_generated_prod_code(code_no),
            date DATE,
            sample_size VARCHAR(100),
            mixing_time VARCHAR(100),
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
    # 5. MASTER FORMULA MODULE
    # ==========================================
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tbl_master_formula(
            form_id SERIAL PRIMARY KEY,
            index_no VARCHAR(100),
            date DATE,
            customer VARCHAR(150),
            code_no_prod_code VARCHAR(100),
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
    """)

    # ==========================================
    # 6. DAILY FORMULATION MODULE
    # ==========================================
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tbl_formula01(
            form_id SERIAL PRIMARY KEY,
            index_no VARCHAR(22),
            date DATE,
            customer VARCHAR(62),
            prod_code VARCHAR(22) NOT NULL,
            prod_color VARCHAR(62),
            dosage DECIMAL(12,6),
            total_concentration DECIMAL(12,6),
            ld DECIMAL(12,6),
            mix_time VARCHAR(22),
            resin VARCHAR(36),
            application VARCHAR(36),
            colormatch_no VARCHAR(8),
            colormatch_date date,
            notes VARCHAR(256),
            date_time VARCHAR(32),
            is_deleted BOOLEAN DEFAULT FALSE,
            is_used BOOLEAN DEFAULT FALSE
        );

        CREATE TABLE IF NOT EXISTS tbl_formula02(
            id SERIAL PRIMARY KEY,
            form_id INT,
            sequence_no INT,
            material_code VARCHAR(32),
            concentration DECIMAL(12,6),
            is_deleted BOOLEAN DEFAULT FALSE,
            FOREIGN KEY (form_id) REFERENCES tbl_formula01(form_id)
        );

        CREATE TABLE IF NOT EXISTS tbl_formula_encode(
            encode_id SERIAL PRIMARY KEY,
            form_id INT,
            match_by VARCHAR(128),
            encoded_by VARCHAR(128),
            updated_by VARCHAR(128),
            FOREIGN KEY (form_id) REFERENCES tbl_formula01(form_id)
        );
    """)

    # ==========================================
    # 7. DAILY Production
    # ==========================================
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tbl_production01(
            prod_id SERIAL PRIMARY KEY,
            prod_date DATE,
            customer VARCHAR(62),
            form_id INT,
            index_no VARCHAR(32),
            prod_code VARCHAR(32),
            prod_color VARCHAR(62),
            dosage DECIMAL(12,6),
            ld DECIMAL(12,6),
            lot_no VARCHAR(128),
            order_no VARCHAR(36),
            colormatch_no VARCHAR(8),
            colormatch_date date,
            mix_time VARCHAR(32),
            machine_no VARCHAR(32),
            note VARCHAR(128),
            user_id VARCHAR(62),
            is_deleted BOOLEAN DEFAULT FALSE,
            is_printed BOOLEAN DEFAULT FALSE,
            inventory_c_date DATE,
            form_type VARCHAR(16)   
        );
        
        CREATE TABLE IF NOT EXISTS tbl_production_encode(
            encode_id SERIAL PRIMARY KEY,
            prod_id INT,
            prepared_by VARCHAR(128),
            encoded_by VARCHAR(128),
            encoded_on TIMESTAMP, 
            confirmation_encoded_on TIMESTAMP, 
            FOREIGN KEY (prod_id) REFERENCES tbl_production01(prod_id)
        );
        
        CREATE TABLE IF NOT EXISTS tbl_production_quantity(
            quantity_id SERIAL PRIMARY KEY,
            prod_id INT,
            quantity_req DECIMAL(12,6),
            quantity_batch DECIMAL(12,6),
            quantity_prod DECIMAL(12,6),
            FOREIGN KEY (prod_id) REFERENCES tbl_production01(prod_id)
        );
        
        CREATE TABLE IF NOT EXISTS tbl_production02(
            id SERIAL PRIMARY KEY,
            prod_id INT,
            sequence_no INT,
            material_code VARCHAR(32),
            large_scale DECIMAL(12,6),
            small_scale DECIMAL(12,6),
            total_weight DECIMAL(12,6),
            is_deleted BOOLEAN DEFAULT FALSE,
            total_loss DECIMAL(12,6),
            total_consumption DECIMAL(12,6),
            FOREIGN KEY (prod_id) REFERENCES tbl_production01(prod_id)
        );
    """)

    # ==========================================
    # 8. RM list
    # ==========================================
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tbl_raw_material_list(
            id SERIAL PRIMARY KEY,
            rm_code VARCHAR(50) UNIQUE
        );
        
        CREATE TABLE IF NOT EXISTS tbl_rm_incoming (
            id SERIAL PRIMARY KEY,
            date DATE,
            material_code VARCHAR(50) NOT NULL UNIQUE,
            note TEXT
        );
    """)

    con.commit()
    cursor.close()
    con.close()
