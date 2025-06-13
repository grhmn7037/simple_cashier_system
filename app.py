# print("if there is problem send viber massege to 07501783534 ") # Informational print
#Ghalib_07507318027  and the line 145 after the lock is o.k
import os
import sys  # Keep sys import at the top
import hashlib
import platform
# Keep Flask/SQLAlchemy imports inside the password/location check

# --- Configuration ---
CONFIG_DIR_NAME = ".my_python_app_config"
LOCK_FILENAME = "location.lock"
# --- End Configuration ---

def get_config_directory():
    """Gets the path to the application's config directory in the user's home."""
    try:
        home_dir = os.path.expanduser('~')
        config_dir = os.path.join(home_dir, CONFIG_DIR_NAME)
        return config_dir
    except Exception as e:
        print(f"Error: Could not determine user home directory or construct config path: {e}")
        return None

def hash_path(path_string):
    """Hashes a path string using SHA-256."""
    normalized_path = os.path.normpath(path_string)
    path_bytes = normalized_path.encode('utf-8')
    sha256_hash = hashlib.sha256(path_bytes)
    hashed_path = sha256_hash.hexdigest()
    return hashed_path

def check_or_set_location_lock(current_executable_dir, fixed_lock_file_path):
    """
    Checks if the current EXECUTABLE location matches the location stored in the FIXED lock file.
    If no fixed lock file exists (first run ever), it creates one for the current location.
    Returns True if the location is verified or newly locked, False otherwise.
    """
    config_dir = os.path.dirname(fixed_lock_file_path)

    if os.path.exists(fixed_lock_file_path):
        # Fixed lock file exists - Verify current executable location against stored hash
        print(f"Verifying application location using lock file in: {config_dir}")
        try:
            with open(fixed_lock_file_path, 'r') as f:
                stored_hash = f.read().strip()

            if not stored_hash:
                print(f"Error: Lock file '{fixed_lock_file_path}' is empty.")
                print("Tampering detected or setup incomplete. Consider deleting the config directory:")
                print(f"'{config_dir}' and running again.")
                return False

            current_path_hash = hash_path(current_executable_dir)

            if current_path_hash == stored_hash:
                print("Location verified successfully.")
                return True
            else:
                print(f"Error: Application is running from a location different from the original!")
                print(f"Current Location Hash: {current_path_hash} ({current_executable_dir})")
                print(f"Locked Location Hash:  {stored_hash}")
                print(f"(Lock file checked at: {fixed_lock_file_path})")
                print("Application will not run from this location.")
                return False

        except FileNotFoundError:
            print(f"Error: Lock file '{fixed_lock_file_path}' disappeared unexpectedly after existence check.")
            return False
        except PermissionError:
            print(f"Error: Permission denied when trying to read lock file '{fixed_lock_file_path}'.")
            return False
        except Exception as e:
            print(f"An error occurred during location verification: {e}")
            return False

    else:
        # Lock file does NOT exist in the fixed location - First run EVER.
        print(f"Performing first-time setup...")
        print(f"Application lock file not found in '{config_dir}'.")
        print(f"Locking application to current directory: {current_executable_dir}")
        try:
            print(f"Attempting to create configuration directory: {config_dir}")
            os.makedirs(config_dir, exist_ok=True)

            current_path_hash = hash_path(current_executable_dir)
            with open(fixed_lock_file_path, 'w') as f:
                f.write(current_path_hash)
            print(f"Location lock created successfully in '{fixed_lock_file_path}'.")
            return True

        except PermissionError:
            print(f"\nError: Permission denied. Cannot create directory or write lock file.")
            print(f"Please check permissions for: '{config_dir}'")
            return False
        except IOError as e:
            print(f"\nError: Could not write lock file to '{fixed_lock_file_path}'.")
            print(f"Details: {e}")
            return False
        except Exception as e:
            print(f"\nAn unexpected error occurred while creating the lock file: {e}")
            return False

# --- Password Check ---
# Use the password check from the first script
path = input("input password for download the app = ")
if path == "Ghalib_07507318027":

    # --- Main Execution Logic ---
    if __name__ == "__main__":
        print("--- Application Startup ---")

        # --- Determine Paths (Handles PyInstaller) ---
        # Use the robust path determination from the first script
        if getattr(sys, 'frozen', False):
            executable_dir = os.path.dirname(sys.executable)
            resource_dir = sys._MEIPASS
            print(f"Running frozen.")
            print(f"Executable directory: {executable_dir}")
            print(f"Resource directory (templates/static): {resource_dir}")
        else:
            try:
                script_path = os.path.abspath(__file__)
                executable_dir = os.path.dirname(script_path)
                resource_dir = executable_dir
                print(f"Running as script. Script directory: {executable_dir}")
            except NameError:
                executable_dir = os.getcwd()
                resource_dir = executable_dir
                print(f"Warning: '__file__' not defined, using CWD: {executable_dir}")
                print("Location locking might be unreliable.")

        # --- Determine Lock File Path ---
        config_dir_path = get_config_directory()
        if not config_dir_path:
            print("Could not determine configuration directory. Exiting.")
            sys.exit(1)

        fixed_lock_file = os.path.join(config_dir_path, LOCK_FILENAME)

        # --- Check Location Lock ---
        location_ok = check_or_set_location_lock(executable_dir, fixed_lock_file)
        print(executable_dir, fixed_lock_file)

        # --- Proceed only if location is verified ---
        # V V V V V THIS IS THE BLOCK WHERE YOUR CORE APP GOES V V V V V
        if location_ok:
            print("\n--- Starting Main Application Logic ---")
            print("Application logic would run now...")

            # --- Imports for the Core Flask App (from Script 2) ---
            from flask import Flask, render_template, request, redirect, flash, url_for, session, abort
            from flask_sqlalchemy import SQLAlchemy
            # os, sys, hashlib, platform are already imported above
            from datetime import datetime, date, timezone
            import logging

            # --- App Configuration (using paths determined above) ---
            # Use executable_dir for the database location
            db_directory = executable_dir
            db_path = os.path.join(db_directory, 'inventory.db') # Keep DB name simple
            db_uri = f'sqlite:///{db_path}'
            print(f"Database URI set to: {db_uri}")

            # Use resource_dir for templates/static (handles frozen case)
            app = Flask(__name__,
                        template_folder=os.path.join(resource_dir, 'templates'),
                        static_folder=os.path.join(resource_dir, 'static'))

            app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
            app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
            # Use a better secret key practice
            app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'a_much_stronger_default_secret_key_!@#$%^&*)') # CHANGE THIS KEY

            db = SQLAlchemy(app)

            # --- Basic Logging Setup (from Script 2) ---
            logging.basicConfig(level=logging.INFO)

            # --- Database Models (from Script 2) ---
            class Customer(db.Model):
                id = db.Column(db.Integer, primary_key=True)
                name = db.Column(db.String(150), nullable=False, unique=True)
                sales = db.relationship('Transaction', back_populates='customer', lazy='dynamic')
                def __repr__(self): return f'<Customer {self.name}>'

            class Part(db.Model):
                id = db.Column(db.Integer, primary_key=True)
                name = db.Column(db.String(100), nullable=False)
                description = db.Column(db.String(200), nullable=True)
                description1 = db.Column(db.String(200), nullable=True)
                part_number = db.Column(db.String(50), nullable=True)
                quantity = db.Column(db.Integer, default=0, nullable=False)
                selling_price = db.Column(db.Float, default=0.0, nullable=False)
                transactions = db.relationship('Transaction', back_populates='part', lazy=True, cascade="all, delete-orphan")
                def __repr__(self): return f'<Part {self.name}>'

            class Transaction(db.Model):
                id = db.Column(db.Integer, primary_key=True)
                transaction_type = db.Column(db.String(20), nullable=False)
                amount = db.Column(db.Float, nullable=False)
                date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False) # Store UTC
                part_id = db.Column(db.Integer, db.ForeignKey('part.id'), nullable=False)
                part = db.relationship('Part', back_populates='transactions')
                customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=True)
                customer = db.relationship('Customer', back_populates='sales')
                def __repr__(self):
                    part_name = self.part.name if self.part else "N/A"
                    cust_info = f" - Cust: {self.customer.name}" if self.transaction_type == 'بيع' and self.customer else ""
                    return f'<Transaction {self.transaction_type} ({self.id}) - Part: {part_name}{cust_info} - Amt: {self.amount}>'


            # --- Routes (from Script 2) ---
            @app.route('/')
            def index():
                return redirect(url_for('list_parts'))

            @app.route('/parts')
            def list_parts():
                search_term = request.args.get('search', '').strip()
                customers = Customer.query.order_by(Customer.name).all()
                query = Part.query
                if search_term:
                    search_filter = db.or_(Part.name.contains(search_term), Part.part_number.contains(search_term))
                    query = query.filter(search_filter)
                parts = query.order_by(Part.name).all()
                current_local_time = datetime.now()
                return render_template(
                    'parts.html',
                    parts=parts,
                    customers=customers,
                    search_term=search_term,
                    current_time=current_local_time
                )

            @app.route('/parts/add', methods=['GET', 'POST'])
            def add_part():
                if request.method == 'POST':
                    try:
                        name = request.form['name'].strip()
                        description = request.form.get('description', '').strip()
                        description1 = request.form.get('description1', '').strip()
                        part_number = request.form.get('part_number', '').strip()
                        if not name: flash('اسم الجزء مطلوب.', 'error'); return render_template('add_part.html', form_data=request.form)
                        try:
                            quantity = int(request.form['quantity'])
                            selling_price = float(request.form['selling_price'])
                        except ValueError: flash('الرجاء إدخال أرقام صالحة للكمية وسعر البيع.', 'error'); return render_template('add_part.html', form_data=request.form)
                        if quantity < 0 or selling_price < 0: flash('الكمية والسعر يجب ألا تكونا سالبتين.', 'error'); return render_template('add_part.html', form_data=request.form)

                        existing_part = Part.query.filter_by(name=name, part_number=part_number).first()
                        if existing_part:
                            existing_part.description = description
                            existing_part.description1 = description1
                            existing_part.selling_price = selling_price
                            existing_part.quantity += quantity
                            db.session.commit()
                            part_id_for_transaction = existing_part.id
                            flash(f'تم تحديث الجزء "{existing_part.name}" وزيادة الكمية بمقدار {quantity}.', 'success')
                        else:
                            new_part = Part(name=name, description=description, description1=description1, part_number=part_number, quantity=quantity, selling_price=selling_price)
                            db.session.add(new_part)
                            db.session.flush()
                            part_id_for_transaction = new_part.id
                            db.session.commit()
                            flash(f'تمت إضافة جزء جديد "{new_part.name}".', 'success')

                        if quantity > 0:
                            purchase_amount = quantity * selling_price
                            transaction = Transaction(transaction_type='شراء', amount=purchase_amount, part_id=part_id_for_transaction)
                            db.session.add(transaction)
                            db.session.commit()
                        return redirect(url_for('list_parts'))
                    except Exception as e:
                         db.session.rollback()
                         app.logger.error(f"Error adding/updating part: {e}", exc_info=True)
                         flash('حدث خطأ غير متوقع أثناء إضافة/تحديث الجزء.', 'error')
                         return render_template('add_part.html', form_data=request.form)
                return render_template('add_part.html')

            @app.route('/parts/sell/<int:id>', methods=['POST'])
            def sell_part(id):
                part = db.session.get(Part, id)
                if not part: app.logger.warning(f"Sell attempt for non-existent part ID: {id}"); abort(404)
                try:
                    try: quantity_to_sell = int(request.form['quantity'])
                    except ValueError: flash('الرجاء إدخال كمية بيع رقمية صالحة.', 'error'); return redirect(url_for('list_parts'))
                    if quantity_to_sell <= 0: flash('كمية البيع يجب أن تكون أكبر من صفر.', 'error'); return redirect(url_for('list_parts'))
                    customer_id_str = request.form.get('customer_id')
                    if not customer_id_str: flash('الرجاء اختيار عميل لإتمام عملية البيع.', 'error'); return redirect(url_for('list_parts'))
                    try:
                        customer_id = int(customer_id_str)
                        customer = db.session.get(Customer, customer_id)
                        if not customer: flash('العميل المختار غير موجود.', 'error'); return redirect(url_for('list_parts'))
                    except ValueError: flash('معرف العميل غير صالح.', 'error'); return redirect(url_for('list_parts'))
                    if quantity_to_sell > part.quantity: flash(f'الكمية المطلوبة ({quantity_to_sell}) غير متوفرة للجزء "{part.name}". المتوفر: {part.quantity}', 'error'); return redirect(url_for('list_parts'))
                    part.quantity -= quantity_to_sell
                    sale_amount = quantity_to_sell * part.selling_price
                    transaction = Transaction(transaction_type='بيع', amount=sale_amount, part_id=part.id, customer_id=customer_id)
                    db.session.add(transaction)
                    db.session.commit()
                    flash(f'تم بيع {quantity_to_sell} من الجزء "{part.name}" للعميل "{customer.name}".', 'success')
                except Exception as e:
                    db.session.rollback()
                    app.logger.error(f"Error selling part {id}: {e}", exc_info=True)
                    flash('حدث خطأ أثناء عملية البيع.', 'error')
                return redirect(url_for('list_parts'))

            @app.route('/parts/delete/<int:id>', methods=['POST'])
            def delete_part(id):
                part = db.session.get(Part, id)
                if not part: app.logger.warning(f"Delete attempt for non-existent part ID: {id}"); flash('الجزء المراد حذفه غير موجود.', 'error'); return redirect(url_for('list_parts'))
                try:
                    part_name = part.name
                    db.session.delete(part)
                    db.session.commit()
                    flash(f'تم حذف الجزء "{part_name}" وجميع معاملاته بنجاح.', 'success')
                except Exception as e:
                    db.session.rollback()
                    app.logger.error(f"Error deleting part {id}: {e}", exc_info=True)
                    flash('حدث خطأ أثناء حذف الجزء.', 'error')
                return redirect(url_for('list_parts'))

            @app.route('/parts/edit/<int:id>', methods=['GET', 'POST'])
            def edit_part(id):
                part = db.session.get(Part, id)
                if not part: app.logger.warning(f"Edit attempt for non-existent part ID: {id}"); abort(404)
                if request.method == 'POST':
                    try:
                        part.name = request.form['name'].strip()
                        part.description = request.form.get('description', '').strip()
                        part.description1 = request.form.get('description1', '').strip()
                        part.part_number = request.form.get('part_number', '').strip()
                        if not part.name: flash('اسم الجزء مطلوب.', 'error'); return render_template('edit_part.html', part=part)
                        try:
                            new_quantity = int(request.form['quantity'])
                            new_selling_price = float(request.form['selling_price'])
                        except ValueError: flash('الرجاء إدخال أرقام صالحة للكمية والسعر.', 'error'); return render_template('edit_part.html', part=part)
                        if new_quantity < 0 or new_selling_price < 0: flash('الكمية والسعر يجب ألا تكونا سالبتين.', 'error'); return render_template('edit_part.html', part=part)
                        part.quantity = new_quantity
                        part.selling_price = new_selling_price
                        db.session.commit()
                        flash(f'تم تحديث بيانات الجزء "{part.name}" بنجاح.', 'success')
                        return redirect(url_for('list_parts'))
                    except Exception as e:
                        db.session.rollback()
                        app.logger.error(f"Error editing part {id}: {e}", exc_info=True)
                        flash('حدث خطأ أثناء التعديل.', 'error')
                        part = db.session.get(Part, id) # Re-fetch original data on error
                        return render_template('edit_part.html', part=part)
                return render_template('edit_part.html', part=part)

            @app.route('/transactions')
            def list_transactions():
                transactions = Transaction.query.options(db.joinedload(Transaction.part), db.joinedload(Transaction.customer)).order_by(Transaction.date.desc()).all()
                return render_template('transactions.html', transactions=transactions)

            @app.route('/transactions/delete/<int:id>', methods=['POST'])
            def delete_transaction(id):
                transaction = db.session.get(Transaction, id)
                if not transaction: app.logger.warning(f"Delete attempt for non-existent transaction ID: {id}"); flash('المعاملة غير موجودة.', 'error'); return redirect(url_for('list_transactions'))
                part = transaction.part
                if part:
                    try:
                        if part.selling_price is not None and part.selling_price > 0:
                            quantity_change_estimate = round(transaction.amount / part.selling_price)
                            if transaction.transaction_type == 'شراء': part.quantity = max(0, part.quantity - quantity_change_estimate)
                            elif transaction.transaction_type == 'بيع': part.quantity += quantity_change_estimate
                        else: flash('لم يتم تعديل كمية الجزء تلقائياً لأن سعر البيع الحالي للجزء غير صالح أو صفر.', 'warning')
                    except Exception as qty_e: app.logger.error(f"Error adjusting quantity for part {part.id} while deleting tx {id}: {qty_e}", exc_info=True); flash('حدث خطأ أثناء محاولة تعديل كمية الجزء.', 'error')
                else: flash('الجزء المرتبط بهذه المعاملة غير موجود. سيتم حذف المعاملة فقط.', 'warning')
                try:
                    db.session.delete(transaction)
                    db.session.commit()
                    flash('تم حذف المعاملة بنجاح.', 'success')
                except Exception as e:
                    db.session.rollback()
                    app.logger.error(f"Error deleting transaction {id}: {e}", exc_info=True)
                    flash('حدث خطأ أثناء حذف المعاملة.', 'error')
                return redirect(url_for('list_transactions'))

            @app.route('/customers')
            def list_customers():
                customers = Customer.query.order_by(Customer.name).all()
                return render_template('customers.html', customers=customers)

            @app.route('/customers/add', methods=['GET', 'POST'])
            def add_customer():
                if request.method == 'POST':
                    name = request.form.get('name', '').strip()
                    if not name: flash('اسم العميل مطلوب.', 'error'); return render_template('add_customer.html', name=name)
                    else:
                        existing = Customer.query.filter(Customer.name.ilike(name)).first()
                        if existing: flash(f'العميل "{name}" موجود بالفعل.', 'warning'); return render_template('add_customer.html', name=name)
                        else:
                            try:
                                new_customer = Customer(name=name)
                                db.session.add(new_customer)
                                db.session.commit()
                                flash(f'تمت إضافة العميل "{name}" بنجاح.', 'success')
                                return redirect(url_for('list_customers'))
                            except Exception as e:
                                db.session.rollback()
                                app.logger.error(f"Error adding customer '{name}': {e}", exc_info=True)
                                flash('حدث خطأ أثناء إضافة العميل.', 'error')
                                return render_template('add_customer.html', name=name)
                return render_template('add_customer.html')

            @app.route('/customers/edit/<int:id>', methods=['GET', 'POST'])
            def edit_customer(id):
                customer = db.session.get(Customer, id)
                if not customer: app.logger.warning(f"Edit attempt for non-existent customer ID: {id}"); abort(404)
                if request.method == 'POST':
                    new_name = request.form.get('name', '').strip()
                    if not new_name: flash('اسم العميل مطلوب.', 'error'); return render_template('edit_customer.html', customer=customer)
                    else:
                        existing = Customer.query.filter(Customer.name.ilike(new_name), Customer.id != id).first()
                        if existing: flash(f'اسم العميل "{new_name}" مستخدم بالفعل لعميل آخر.', 'error'); return render_template('edit_customer.html', customer=customer, submitted_name=new_name)
                        else:
                            try:
                                customer.name = new_name
                                db.session.commit()
                                flash(f'تم تحديث بيانات العميل بنجاح.', 'success'); return redirect(url_for('list_customers'))
                            except Exception as e:
                                db.session.rollback()
                                app.logger.error(f"Error editing customer {id}: {e}", exc_info=True)
                                flash('حدث خطأ أثناء تعديل العميل.', 'error')
                                return render_template('edit_customer.html', customer=customer)
                return render_template('edit_customer.html', customer=customer)

            @app.route('/customers/delete/<int:id>', methods=['POST'])
            def delete_customer(id):
                 customer = db.session.get(Customer, id)
                 if not customer: app.logger.warning(f"Delete attempt for non-existent customer ID: {id}"); flash('العميل غير موجود.', 'error'); return redirect(url_for('list_customers'))
                 if customer.sales.first(): flash(f'لا يمكن حذف العميل "{customer.name}" لأنه مرتبط بمعاملات بيع.', 'error')
                 else:
                    try:
                        customer_name = customer.name
                        db.session.delete(customer)
                        db.session.commit()
                        flash(f'تم حذف العميل "{customer_name}" بنجاح.', 'success')
                    except Exception as e:
                        db.session.rollback()
                        app.logger.error(f"Error deleting customer {id}: {e}", exc_info=True)
                        flash('حدث خطأ أثناء حذف العميل.', 'error')
                 return redirect(url_for('list_customers'))

            @app.route('/customers/<int:id>/sales')
            def customer_sales_report(id):
                customer = db.session.get(Customer, id)
                if not customer: app.logger.warning(f"Sales report attempt for non-existent customer ID: {id}"); abort(404)
                sales_list = Transaction.query.options(db.joinedload(Transaction.part)).filter_by(customer_id=id, transaction_type='بيع').order_by(Transaction.date.desc()).all()
                grand_total = sum(sale.amount for sale in sales_list if sale.amount is not None)
                return render_template('customer_sales.html', customer=customer, sales_list=sales_list, grand_total=grand_total, datetime=datetime, timezone=timezone)

            @app.route('/list/prepare/<int:customer_id>', methods=['GET', 'POST'])
            def prepare_customer_list(customer_id):
                customer = db.session.get(Customer, customer_id)
                if not customer: app.logger.warning(f"Prepare list attempt for non-existent customer ID: {customer_id}"); flash(f'العميل بالمعرف {customer_id} غير موجود.', 'error'); return redirect(url_for('list_customers'))
                session_key = f'current_list_{customer_id}'
                if session_key not in session: session[session_key] = []
                if request.method == 'POST':
                    try:
                        part_id_str = request.form.get('part_id'); quantity_str = request.form.get('quantity', '1')
                        if not part_id_str or not quantity_str: flash('الرجاء اختيار الجزء وإدخال الكمية.', 'error'); return redirect(url_for('prepare_customer_list', customer_id=customer_id))
                        part_id = int(part_id_str); quantity = int(quantity_str)
                        part = db.session.get(Part, part_id)
                        if not part: flash('الجزء المختار غير موجود.', 'error')
                        elif quantity <= 0: flash('الكمية يجب أن تكون أكبر من صفر.', 'error')
                        # Check available quantity BEFORE adding/updating list
                        elif quantity > part.quantity: flash(f'الكمية المطلوبة ({quantity}) غير متوفرة للجزء "{part.name}". المتوفر: {part.quantity}', 'error')
                        else:
                            current_list = session.get(session_key, []); found = False
                            for item in current_list:
                                if item['part_id'] == part_id:
                                    # Check if adding more exceeds current stock
                                    new_total_qty = item['qty'] + quantity
                                    if new_total_qty > part.quantity:
                                        flash(f'لا يمكن إضافة {quantity} من "{part.name}". الإجمالي المطلوب ({new_total_qty}) يتجاوز الكمية المتوفرة حالياً ({part.quantity}).', 'error')
                                    else:
                                        item['qty'] = new_total_qty
                                        item['total'] = round(item['qty'] * item['price'], 2)
                                        flash(f'تم تحديث كمية "{part.name}" في القائمة.', 'success')
                                    found = True; break
                            if not found:
                                # Already checked quantity > part.quantity above
                                item_total = round(quantity * part.selling_price, 2)
                                current_list.append({'part_id': part.id, 'name': part.name, 'part_number': part.part_number, 'qty': quantity, 'price': part.selling_price, 'total': item_total})
                                flash(f'تمت إضافة {quantity} من "{part.name}" إلى القائمة.', 'success')

                            session[session_key] = current_list; session.modified = True
                    except ValueError: flash('الرجاء إدخال معرف جزء وكمية صحيحة.', 'error')
                    except Exception as e: flash(f'حدث خطأ غير متوقع أثناء إضافة الجزء: {e}', 'error'); app.logger.error(f"Error adding item to list for customer {customer_id}: {e}", exc_info=True)
                    return redirect(url_for('prepare_customer_list', customer_id=customer_id))

                parts_available = Part.query.filter(Part.quantity > 0).order_by(Part.name).all()
                current_list_items = session.get(session_key, [])
                grand_total = sum(item['total'] for item in current_list_items)
                current_time_utc = datetime.now(timezone.utc)
                return render_template('prepare_list.html', customer=customer, parts=parts_available, current_list=current_list_items, grand_total=grand_total, session_key=session_key, current_time=current_time_utc)

            @app.route('/list/clear/<int:customer_id>', methods=['POST'])
            def clear_customer_list(customer_id):
                session_key = f'current_list_{customer_id}'
                if session_key in session: session.pop(session_key, None); session.modified = True; flash('تم مسح القائمة الحالية.', 'success')
                else: flash('القائمة فارغة بالفعل.', 'info')
                return redirect(url_for('prepare_customer_list', customer_id=customer_id))

            @app.route('/list/finalize/<int:customer_id>', methods=['POST'])
            def finalize_customer_list(customer_id):
                customer = db.session.get(Customer, customer_id)
                if not customer: flash(f'العميل بالمعرف {customer_id} غير موجود.', 'error'); return redirect(url_for('list_customers'))
                session_key = f'current_list_{customer_id}'
                current_list_items = session.get(session_key, [])
                if not current_list_items: flash('القائمة فارغة، لا يوجد شيء لإتمامه.', 'warning'); return redirect(url_for('prepare_customer_list', customer_id=customer_id))
                try:
                    parts_to_update = {}
                    with db.session.no_autoflush:
                        for item in current_list_items:
                            part = db.session.get(Part, item['part_id'])
                            if not part: db.session.rollback(); flash(f'خطأ حرج: الجزء "{item["name"]}" (ID: {item["part_id"]}) لم يعد موجوداً. تم إلغاء العملية.', 'error'); return redirect(url_for('prepare_customer_list', customer_id=customer_id))
                            if item['qty'] > part.quantity: db.session.rollback(); flash(f'الكمية المطلوبة ({item["qty"]}) غير متوفرة الآن للجزء "{item["name"]}" (المتوفر: {part.quantity}). يرجى مراجعة القائمة وتحديثها. تم إلغاء العملية.', 'error'); return redirect(url_for('prepare_customer_list', customer_id=customer_id))
                            parts_to_update[part.id] = part
                    total_sale_amount = 0; transactions_to_add = []
                    sale_time = datetime.now(timezone.utc)
                    for item in current_list_items:
                        part = parts_to_update[item['part_id']]
                        part.quantity -= item['qty']
                        transaction = Transaction(transaction_type='بيع', amount=item['total'], part_id=item['part_id'], customer_id=customer_id, date=sale_time)
                        transactions_to_add.append(transaction)
                        total_sale_amount += item['total']
                    db.session.add_all(transactions_to_add)
                    db.session.commit()
                    session.pop(session_key, None); session.modified = True
                    flash(f'تم إتمام عملية البيع بنجاح للعميل "{customer.name}" بمبلغ إجمالي {total_sale_amount:.2f}.', 'success')
                    return redirect(url_for('list_customers'))
                except Exception as e:
                    db.session.rollback()
                    app.logger.error(f"Error finalizing list for customer {customer_id}: {e}", exc_info=True)
                    flash('حدث خطأ فادح أثناء إتمام عملية البيع. لم يتم تحديث المخزون أو إضافة المعاملات.', 'error')
                    return redirect(url_for('prepare_customer_list', customer_id=customer_id))

            @app.route('/reports/sales_by_type')
            def sales_by_type():
                sales_data = []
                try:
                    sales_data = db.session.query(Part.name, db.func.sum(Transaction.amount).label('total_sales')).select_from(Transaction).join(Part, Part.id == Transaction.part_id).filter(Transaction.transaction_type == 'بيع').group_by(Part.name).order_by(db.desc('total_sales')).all()
                except Exception as e: app.logger.error(f"Error generating sales by type report: {e}", exc_info=True); flash("حدث خطأ أثناء إنشاء تقرير المبيعات حسب النوع.", "error")
                return render_template('sales_by_type.html', sales_data=sales_data)

            @app.route('/reports/sales_by_date')
            def sales_by_date():
                processed_sales_data = []
                try:
                    sales_query_result = db.session.query(db.func.date(Transaction.date).label('sale_date_str'), db.func.sum(Transaction.amount).label('daily_total')).filter(Transaction.transaction_type == 'بيع').group_by(db.func.date(Transaction.date)).order_by(db.desc(db.func.date(Transaction.date))).all()
                    for row in sales_query_result:
                        sale_date_obj = None; daily_total = row.daily_total
                        if row.sale_date_str:
                            try: sale_date_obj = datetime.strptime(row.sale_date_str, '%Y-%m-%d').date()
                            except ValueError: app.logger.warning(f"Could not parse date string in sales_by_date report: {row.sale_date_str}")
                        processed_sales_data.append({'sale_date': sale_date_obj, 'daily_total': daily_total})
                except Exception as e: app.logger.error(f"Error generating sales by date report: {e}", exc_info=True); flash("حدث خطأ أثناء إنشاء تقرير المبيعات حسب التاريخ.", "error")
                return render_template('sales_by_date.html', sales_data=processed_sales_data)


            # --- App Run Logic (Database Setup and Starting the server) ---
            # This should be the final part inside the 'if location_ok:' block
            try:
                with app.app_context():
                    app.logger.info("Checking/Creating database tables...")
                    db.create_all()
                    app.logger.info("Database tables checked/created.")
                    if not Customer.query.filter_by(name="بيع نقدي").first():
                        app.logger.info("Default 'بيع نقدي' customer not found, creating...")
                        try:
                            cash_customer = Customer(name="بيع نقدي")
                            db.session.add(cash_customer)
                            db.session.commit()
                            app.logger.info("Default 'بيع نقدي' customer created.")
                        except Exception as e_cust:
                            db.session.rollback()
                            app.logger.error(f"Error creating default customer: {e_cust}", exc_info=True)
            except Exception as e_db:
                app.logger.error(f"Error during database initialization: {e_db}", exc_info=True)

            app.logger.info("Starting Flask application...")
            # Set debug=False for final PyInstaller build
            app.run(debug=False, host='0.0.0.0', port=5007) # Use debug=False

            print("\n--- Application Finished ---")
            # --- End of Core Flask App Logic ---

        # This else corresponds to 'if location_ok:'
        else:
            print("\nApplication cannot run due to location mismatch or setup error.")
            print("Exiting.")
            input("Press Enter to exit...")
            sys.exit(1)

# This else corresponds to the initial password check 'if path == ...'
else:
    print("Incorrect initial password. Exiting.")
    input("Press Enter to exit...")
    sys.exit(1)

# --- Ensure no stray code exists below this line ---111111111111111111
# # print("if there is problem send viber massege to 07501783534 ") # Informational print
# path = input("input password for download the app at first time = ")
# if path =="Ghalib_07507318027":
#
#     # --- Imports ---
#     from flask import Flask, render_template, request, redirect, flash, url_for, session, abort # Added session, abort
#     from flask_sqlalchemy import SQLAlchemy
#     import os
#     # Import datetime components needed
#     from datetime import datetime, date, timezone # <<< Ensure datetime is imported
#     import logging
#
#     # --- App Configuration ---
#     app = Flask(__name__)
#     app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'
#     app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#     app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'replace_this_with_a_real_secret_key_3984ur') # CHANGE THIS KEY
#     db = SQLAlchemy(app)
#
#     # --- Basic Logging Setup ---
#     logging.basicConfig(level=logging.INFO)
#
#     # --- Database Models ---
#     # Customer, Part, Transaction models remain unchanged...
#     class Customer(db.Model):
#         id = db.Column(db.Integer, primary_key=True)
#         name = db.Column(db.String(150), nullable=False, unique=True)
#         sales = db.relationship('Transaction', back_populates='customer', lazy='dynamic')
#         def __repr__(self): return f'<Customer {self.name}>'
#
#     class Part(db.Model):
#         id = db.Column(db.Integer, primary_key=True)
#         name = db.Column(db.String(100), nullable=False)
#         description = db.Column(db.String(200), nullable=True)
#         description1 = db.Column(db.String(200), nullable=True)
#         part_number = db.Column(db.String(50), nullable=True)
#         quantity = db.Column(db.Integer, default=0, nullable=False)
#         selling_price = db.Column(db.Float, default=0.0, nullable=False)
#         transactions = db.relationship('Transaction', back_populates='part', lazy=True, cascade="all, delete-orphan")
#         def __repr__(self): return f'<Part {self.name}>'
#
#     class Transaction(db.Model):
#         id = db.Column(db.Integer, primary_key=True)
#         transaction_type = db.Column(db.String(20), nullable=False)
#         amount = db.Column(db.Float, nullable=False)
#         date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False) # Store UTC
#         part_id = db.Column(db.Integer, db.ForeignKey('part.id'), nullable=False)
#         part = db.relationship('Part', back_populates='transactions')
#         customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=True)
#         customer = db.relationship('Customer', back_populates='sales')
#         def __repr__(self):
#             part_name = self.part.name if self.part else "N/A"
#             cust_info = f" - Cust: {self.customer.name}" if self.transaction_type == 'بيع' and self.customer else ""
#             return f'<Transaction {self.transaction_type} ({self.id}) - Part: {part_name}{cust_info} - Amt: {self.amount}>'
#
#
#     # --- Routes ---
#
#     @app.route('/')
#     def index():
#         """Redirects to the main parts list."""
#         return redirect(url_for('list_parts'))
#
#     @app.route('/parts')
#     def list_parts():
#         """Displays the list of parts with search, sell options, and current time."""
#         search_term = request.args.get('search', '').strip()
#         customers = Customer.query.order_by(Customer.name).all()
#         query = Part.query
#         if search_term:
#             search_filter = db.or_(Part.name.contains(search_term), Part.part_number.contains(search_term))
#             query = query.filter(search_filter)
#         parts = query.order_by(Part.name).all()
#
#         # === ADDED: Get current *local* time from the server ===
#         # Note: datetime.now() uses the server's system time zone settings
#         current_local_time = datetime.now()
#
#         # Pass the current_local_time to the template context
#         return render_template(
#             'parts.html',
#             parts=parts,
#             customers=customers,
#             search_term=search_term,
#             current_time=current_local_time # <<< Pass the time variable
#         )
#
#     # --- Parts CRUD ---
#     # add_part, sell_part, delete_part, edit_part routes remain unchanged...
#     @app.route('/parts/add', methods=['GET', 'POST'])
#     def add_part():
#         # ... (code as provided previously) ...
#         if request.method == 'POST':
#             try:
#                 name = request.form['name'].strip()
#                 description = request.form.get('description', '').strip()
#                 description1 = request.form.get('description1', '').strip() # Often 'Supplier' or 'Source'
#                 part_number = request.form.get('part_number', '').strip()
#
#                 if not name: flash('اسم الجزء مطلوب.', 'error'); return render_template('add_part.html', form_data=request.form)
#                 try:
#                     quantity = int(request.form['quantity'])
#                     selling_price = float(request.form['selling_price'])
#                 except ValueError: flash('الرجاء إدخال أرقام صالحة للكمية وسعر البيع.', 'error'); return render_template('add_part.html', form_data=request.form)
#                 if quantity < 0 or selling_price < 0: flash('الكمية والسعر يجب ألا تكونا سالبتين.', 'error'); return render_template('add_part.html', form_data=request.form)
#
#                 existing_part = Part.query.filter_by(name=name, part_number=part_number).first()
#                 if existing_part:
#                     existing_part.description = description
#                     existing_part.description1 = description1
#                     existing_part.selling_price = selling_price
#                     existing_part.quantity += quantity
#                     db.session.commit()
#                     part_id_for_transaction = existing_part.id
#                     flash(f'تم تحديث الجزء "{existing_part.name}" وزيادة الكمية بمقدار {quantity}.', 'success')
#                 else:
#                     new_part = Part(name=name, description=description, description1=description1, part_number=part_number, quantity=quantity, selling_price=selling_price)
#                     db.session.add(new_part)
#                     db.session.flush()
#                     part_id_for_transaction = new_part.id
#                     db.session.commit()
#                     flash(f'تمت إضافة جزء جديد "{new_part.name}".', 'success')
#
#                 if quantity > 0:
#                     purchase_amount = quantity * selling_price
#                     transaction = Transaction(transaction_type='شراء', amount=purchase_amount, part_id=part_id_for_transaction)
#                     db.session.add(transaction)
#                     db.session.commit()
#                 return redirect(url_for('list_parts'))
#             except Exception as e:
#                  db.session.rollback()
#                  app.logger.error(f"Error adding/updating part: {e}", exc_info=True)
#                  flash('حدث خطأ غير متوقع أثناء إضافة/تحديث الجزء.', 'error')
#                  return render_template('add_part.html', form_data=request.form)
#         return render_template('add_part.html')
#
#     @app.route('/parts/sell/<int:id>', methods=['POST'])
#     def sell_part(id):
#         # ... (code as provided previously) ...
#         part = db.session.get(Part, id)
#         if not part: app.logger.warning(f"Sell attempt for non-existent part ID: {id}"); abort(404)
#         try:
#             try: quantity_to_sell = int(request.form['quantity'])
#             except ValueError: flash('الرجاء إدخال كمية بيع رقمية صالحة.', 'error'); return redirect(url_for('list_parts'))
#             if quantity_to_sell <= 0: flash('كمية البيع يجب أن تكون أكبر من صفر.', 'error'); return redirect(url_for('list_parts'))
#             customer_id_str = request.form.get('customer_id')
#             if not customer_id_str: flash('الرجاء اختيار عميل لإتمام عملية البيع.', 'error'); return redirect(url_for('list_parts'))
#             try:
#                 customer_id = int(customer_id_str)
#                 customer = db.session.get(Customer, customer_id)
#                 if not customer: flash('العميل المختار غير موجود.', 'error'); return redirect(url_for('list_parts'))
#             except ValueError: flash('معرف العميل غير صالح.', 'error'); return redirect(url_for('list_parts'))
#             if quantity_to_sell > part.quantity: flash(f'الكمية المطلوبة ({quantity_to_sell}) غير متوفرة للجزء "{part.name}". المتوفر: {part.quantity}', 'error'); return redirect(url_for('list_parts'))
#             part.quantity -= quantity_to_sell
#             sale_amount = quantity_to_sell * part.selling_price
#             transaction = Transaction(transaction_type='بيع', amount=sale_amount, part_id=part.id, customer_id=customer_id)
#             db.session.add(transaction)
#             db.session.commit()
#             flash(f'تم بيع {quantity_to_sell} من الجزء "{part.name}" للعميل "{customer.name}".', 'success')
#         except Exception as e:
#             db.session.rollback()
#             app.logger.error(f"Error selling part {id}: {e}", exc_info=True)
#             flash('حدث خطأ أثناء عملية البيع.', 'error')
#         return redirect(url_for('list_parts'))
#
#     @app.route('/parts/delete/<int:id>', methods=['POST'])
#     def delete_part(id):
#         # ... (code as provided previously) ...
#         part = db.session.get(Part, id)
#         if not part: app.logger.warning(f"Delete attempt for non-existent part ID: {id}"); flash('الجزء المراد حذفه غير موجود.', 'error'); return redirect(url_for('list_parts'))
#         try:
#             part_name = part.name
#             db.session.delete(part)
#             db.session.commit()
#             flash(f'تم حذف الجزء "{part_name}" وجميع معاملاته بنجاح.', 'success')
#         except Exception as e:
#             db.session.rollback()
#             app.logger.error(f"Error deleting part {id}: {e}", exc_info=True)
#             flash('حدث خطأ أثناء حذف الجزء.', 'error')
#         return redirect(url_for('list_parts'))
#
#     @app.route('/parts/edit/<int:id>', methods=['GET', 'POST'])
#     def edit_part(id):
#         # ... (code as provided previously) ...
#         part = db.session.get(Part, id)
#         if not part: app.logger.warning(f"Edit attempt for non-existent part ID: {id}"); abort(404)
#         if request.method == 'POST':
#             try:
#                 part.name = request.form['name'].strip()
#                 part.description = request.form.get('description', '').strip()
#                 part.description1 = request.form.get('description1', '').strip()
#                 part.part_number = request.form.get('part_number', '').strip()
#                 if not part.name: flash('اسم الجزء مطلوب.', 'error'); return render_template('edit_part.html', part=part)
#                 try:
#                     new_quantity = int(request.form['quantity'])
#                     new_selling_price = float(request.form['selling_price'])
#                 except ValueError: flash('الرجاء إدخال أرقام صالحة للكمية والسعر.', 'error'); return render_template('edit_part.html', part=part)
#                 if new_quantity < 0 or new_selling_price < 0: flash('الكمية والسعر يجب ألا تكونا سالبتين.', 'error'); return render_template('edit_part.html', part=part)
#                 part.quantity = new_quantity
#                 part.selling_price = new_selling_price
#                 db.session.commit()
#                 flash(f'تم تحديث بيانات الجزء "{part.name}" بنجاح.', 'success')
#                 return redirect(url_for('list_parts'))
#             except Exception as e:
#                 db.session.rollback()
#                 app.logger.error(f"Error editing part {id}: {e}", exc_info=True)
#                 flash('حدث خطأ أثناء التعديل.', 'error')
#                 part = db.session.get(Part, id) # Re-fetch original data on error
#                 return render_template('edit_part.html', part=part)
#         return render_template('edit_part.html', part=part)
#
#
#     # --- Transactions ---
#     # list_transactions, delete_transaction routes remain unchanged...
#     @app.route('/transactions')
#     def list_transactions():
#         # ... (code as provided previously) ...
#         transactions = Transaction.query.options(db.joinedload(Transaction.part), db.joinedload(Transaction.customer)).order_by(Transaction.date.desc()).all()
#         return render_template('transactions.html', transactions=transactions)
#
#     @app.route('/transactions/delete/<int:id>', methods=['POST'])
#     def delete_transaction(id):
#         # ... (code as provided previously, including security warning) ...
#         # !!! SECURITY WARNING: Client-side password check is insecure !!!
#         transaction = db.session.get(Transaction, id)
#         if not transaction: app.logger.warning(f"Delete attempt for non-existent transaction ID: {id}"); flash('المعاملة غير موجودة.', 'error'); return redirect(url_for('list_transactions'))
#         part = transaction.part
#         if part:
#             try:
#                 if part.selling_price is not None and part.selling_price > 0:
#                     quantity_change_estimate = round(transaction.amount / part.selling_price)
#                     if transaction.transaction_type == 'شراء': part.quantity = max(0, part.quantity - quantity_change_estimate)
#                     elif transaction.transaction_type == 'بيع': part.quantity += quantity_change_estimate
#                 else: flash('لم يتم تعديل كمية الجزء تلقائياً لأن سعر البيع الحالي للجزء غير صالح أو صفر.', 'warning')
#             except Exception as qty_e: app.logger.error(f"Error adjusting quantity for part {part.id} while deleting tx {id}: {qty_e}", exc_info=True); flash('حدث خطأ أثناء محاولة تعديل كمية الجزء.', 'error')
#         else: flash('الجزء المرتبط بهذه المعاملة غير موجود. سيتم حذف المعاملة فقط.', 'warning')
#         try:
#             db.session.delete(transaction)
#             db.session.commit()
#             flash('تم حذف المعاملة بنجاح.', 'success')
#         except Exception as e:
#             db.session.rollback()
#             app.logger.error(f"Error deleting transaction {id}: {e}", exc_info=True)
#             flash('حدث خطأ أثناء حذف المعاملة.', 'error')
#         return redirect(url_for('list_transactions'))
#
#
#     # --- Customer Routes ---
#     # list_customers, add_customer, edit_customer, delete_customer, customer_sales_report routes remain unchanged...
#     @app.route('/customers')
#     def list_customers():
#         # ... (code as provided previously) ...
#         customers = Customer.query.order_by(Customer.name).all()
#         return render_template('customers.html', customers=customers)
#
#     @app.route('/customers/add', methods=['GET', 'POST'])
#     def add_customer():
#         # ... (code as provided previously) ...
#         if request.method == 'POST':
#             name = request.form.get('name', '').strip()
#             if not name: flash('اسم العميل مطلوب.', 'error'); return render_template('add_customer.html', name=name)
#             else:
#                 existing = Customer.query.filter(Customer.name.ilike(name)).first()
#                 if existing: flash(f'العميل "{name}" موجود بالفعل.', 'warning'); return render_template('add_customer.html', name=name)
#                 else:
#                     try:
#                         new_customer = Customer(name=name)
#                         db.session.add(new_customer)
#                         db.session.commit()
#                         flash(f'تمت إضافة العميل "{name}" بنجاح.', 'success')
#                         return redirect(url_for('list_customers'))
#                     except Exception as e:
#                         db.session.rollback()
#                         app.logger.error(f"Error adding customer '{name}': {e}", exc_info=True)
#                         flash('حدث خطأ أثناء إضافة العميل.', 'error')
#                         return render_template('add_customer.html', name=name)
#         return render_template('add_customer.html')
#
#     @app.route('/customers/edit/<int:id>', methods=['GET', 'POST'])
#     def edit_customer(id):
#         # ... (code as provided previously) ...
#         customer = db.session.get(Customer, id)
#         if not customer: app.logger.warning(f"Edit attempt for non-existent customer ID: {id}"); abort(404)
#         if request.method == 'POST':
#             new_name = request.form.get('name', '').strip()
#             if not new_name: flash('اسم العميل مطلوب.', 'error'); return render_template('edit_customer.html', customer=customer)
#             else:
#                 existing = Customer.query.filter(Customer.name.ilike(new_name), Customer.id != id).first()
#                 if existing: flash(f'اسم العميل "{new_name}" مستخدم بالفعل لعميل آخر.', 'error'); return render_template('edit_customer.html', customer=customer, submitted_name=new_name)
#                 else:
#                     try:
#                         customer.name = new_name
#                         db.session.commit()
#                         flash(f'تم تحديث بيانات العميل بنجاح.', 'success'); return redirect(url_for('list_customers'))
#                     except Exception as e:
#                         db.session.rollback()
#                         app.logger.error(f"Error editing customer {id}: {e}", exc_info=True)
#                         flash('حدث خطأ أثناء تعديل العميل.', 'error')
#                         return render_template('edit_customer.html', customer=customer)
#         return render_template('edit_customer.html', customer=customer)
#
#     @app.route('/customers/delete/<int:id>', methods=['POST'])
#     def delete_customer(id):
#          # ... (code as provided previously) ...
#          customer = db.session.get(Customer, id)
#          if not customer: app.logger.warning(f"Delete attempt for non-existent customer ID: {id}"); flash('العميل غير موجود.', 'error'); return redirect(url_for('list_customers'))
#          if customer.sales.first(): flash(f'لا يمكن حذف العميل "{customer.name}" لأنه مرتبط بمعاملات بيع.', 'error')
#          else:
#             try:
#                 customer_name = customer.name
#                 db.session.delete(customer)
#                 db.session.commit()
#                 flash(f'تم حذف العميل "{customer_name}" بنجاح.', 'success')
#             except Exception as e:
#                 db.session.rollback()
#                 app.logger.error(f"Error deleting customer {id}: {e}", exc_info=True)
#                 flash('حدث خطأ أثناء حذف العميل.', 'error')
#          return redirect(url_for('list_customers'))
#
#     @app.route('/customers/<int:id>/sales')
#     def customer_sales_report(id):
#         # ... (code as provided previously) ...
#         customer = db.session.get(Customer, id)
#         if not customer: app.logger.warning(f"Sales report attempt for non-existent customer ID: {id}"); abort(404)
#         sales_list = Transaction.query.options(db.joinedload(Transaction.part)).filter_by(customer_id=id, transaction_type='بيع').order_by(Transaction.date.desc()).all()
#         grand_total = sum(sale.amount for sale in sales_list if sale.amount is not None)
#         # Pass datetime object for use in template if needed
#         return render_template('customer_sales.html', customer=customer, sales_list=sales_list, grand_total=grand_total, datetime=datetime, timezone=timezone)
#
#
#     # --- Temporary List/Invoice Preparation Routes ---
#     # prepare_customer_list, clear_customer_list, finalize_customer_list routes remain unchanged...
#     @app.route('/list/prepare/<int:customer_id>', methods=['GET', 'POST'])
#     def prepare_customer_list(customer_id):
#         # ... (code as provided previously) ...
#         customer = db.session.get(Customer, customer_id)
#         if not customer: app.logger.warning(f"Prepare list attempt for non-existent customer ID: {customer_id}"); flash(f'العميل بالمعرف {customer_id} غير موجود.', 'error'); return redirect(url_for('list_customers'))
#         session_key = f'current_list_{customer_id}'
#         if session_key not in session: session[session_key] = []
#         if request.method == 'POST':
#             try:
#                 part_id_str = request.form.get('part_id'); quantity_str = request.form.get('quantity', '1')
#                 if not part_id_str or not quantity_str: flash('الرجاء اختيار الجزء وإدخال الكمية.', 'error'); return redirect(url_for('prepare_customer_list', customer_id=customer_id))
#                 part_id = int(part_id_str); quantity = int(quantity_str)
#                 part = db.session.get(Part, part_id)
#                 if not part: flash('الجزء المختار غير موجود.', 'error')
#                 elif quantity <= 0: flash('الكمية يجب أن تكون أكبر من صفر.', 'error')
#                 elif quantity > part.quantity: flash(f'الكمية المطلوبة ({quantity}) غير متوفرة للجزء "{part.name}". المتوفر: {part.quantity}', 'error')
#                 else:
#                     current_list = session.get(session_key, []); found = False
#                     for item in current_list:
#                         if item['part_id'] == part_id:
#                             new_total_qty = item['qty'] + quantity
#                             if new_total_qty > part.quantity: flash(f'لا يمكن إضافة {quantity} من "{part.name}". الإجمالي المطلوب ({new_total_qty}) يتجاوز الكمية المتوفرة حالياً ({part.quantity}).', 'error')
#                             else: item['qty'] = new_total_qty; item['total'] = round(item['qty'] * item['price'], 2); flash(f'تم تحديث كمية "{part.name}" في القائمة.', 'success')
#                             found = True; break
#                     if not found:
#                         if quantity > part.quantity: flash(f'الكمية المطلوبة ({quantity}) غير متوفرة للجزء "{part.name}". المتوفر: {part.quantity}', 'error')
#                         else:
#                             item_total = round(quantity * part.selling_price, 2)
#                             current_list.append({'part_id': part.id, 'name': part.name, 'part_number': part.part_number, 'qty': quantity, 'price': part.selling_price, 'total': item_total})
#                             flash(f'تمت إضافة {quantity} من "{part.name}" إلى القائمة.', 'success')
#                     session[session_key] = current_list; session.modified = True
#             except ValueError: flash('الرجاء إدخال معرف جزء وكمية صحيحة.', 'error')
#             except Exception as e: flash(f'حدث خطأ غير متوقع أثناء إضافة الجزء: {e}', 'error'); app.logger.error(f"Error adding item to list for customer {customer_id}: {e}", exc_info=True)
#             return redirect(url_for('prepare_customer_list', customer_id=customer_id))
#         parts_available = Part.query.filter(Part.quantity > 0).order_by(Part.name).all()
#         current_list_items = session.get(session_key, [])
#         grand_total = sum(item['total'] for item in current_list_items)
#         current_time_utc = datetime.now(timezone.utc) # Still pass UTC for print consistency if desired
#         return render_template('prepare_list.html', customer=customer, parts=parts_available, current_list=current_list_items, grand_total=grand_total, session_key=session_key, current_time=current_time_utc)
#
#     @app.route('/list/clear/<int:customer_id>', methods=['POST'])
#     def clear_customer_list(customer_id):
#         # ... (code as provided previously) ...
#         session_key = f'current_list_{customer_id}'
#         if session_key in session: session.pop(session_key, None); session.modified = True; flash('تم مسح القائمة الحالية.', 'success')
#         else: flash('القائمة فارغة بالفعل.', 'info')
#         return redirect(url_for('prepare_customer_list', customer_id=customer_id))
#
#     @app.route('/list/finalize/<int:customer_id>', methods=['POST'])
#     def finalize_customer_list(customer_id):
#         # ... (code as provided previously) ...
#         customer = db.session.get(Customer, customer_id)
#         if not customer: flash(f'العميل بالمعرف {customer_id} غير موجود.', 'error'); return redirect(url_for('list_customers'))
#         session_key = f'current_list_{customer_id}'
#         current_list_items = session.get(session_key, [])
#         if not current_list_items: flash('القائمة فارغة، لا يوجد شيء لإتمامه.', 'warning'); return redirect(url_for('prepare_customer_list', customer_id=customer_id))
#         try:
#             parts_to_update = {}
#             with db.session.no_autoflush:
#                 for item in current_list_items:
#                     part = db.session.get(Part, item['part_id'])
#                     if not part: db.session.rollback(); flash(f'خطأ حرج: الجزء "{item["name"]}" (ID: {item["part_id"]}) لم يعد موجوداً. تم إلغاء العملية.', 'error'); return redirect(url_for('prepare_customer_list', customer_id=customer_id))
#                     if item['qty'] > part.quantity: db.session.rollback(); flash(f'الكمية المطلوبة ({item["qty"]}) غير متوفرة الآن للجزء "{item["name"]}" (المتوفر: {part.quantity}). يرجى مراجعة القائمة وتحديثها. تم إلغاء العملية.', 'error'); return redirect(url_for('prepare_customer_list', customer_id=customer_id))
#                     parts_to_update[part.id] = part
#             total_sale_amount = 0; transactions_to_add = []
#             sale_time = datetime.now(timezone.utc) # Use same time for all transactions in this sale
#             for item in current_list_items:
#                 part = parts_to_update[item['part_id']]
#                 part.quantity -= item['qty']
#                 transaction = Transaction(transaction_type='بيع', amount=item['total'], part_id=item['part_id'], customer_id=customer_id, date=sale_time)
#                 transactions_to_add.append(transaction)
#                 total_sale_amount += item['total']
#             db.session.add_all(transactions_to_add)
#             db.session.commit()
#             session.pop(session_key, None); session.modified = True
#             flash(f'تم إتمام عملية البيع بنجاح للعميل "{customer.name}" بمبلغ إجمالي {total_sale_amount:.2f}.', 'success')
#             return redirect(url_for('list_customers'))
#         except Exception as e:
#             db.session.rollback()
#             app.logger.error(f"Error finalizing list for customer {customer_id}: {e}", exc_info=True)
#             flash('حدث خطأ فادح أثناء إتمام عملية البيع. لم يتم تحديث المخزون أو إضافة المعاملات.', 'error')
#             return redirect(url_for('prepare_customer_list', customer_id=customer_id))
#
#
#     # --- Reporting Routes ---
#     # sales_by_type, sales_by_date routes remain unchanged...
#     @app.route('/reports/sales_by_type')
#     def sales_by_type():
#         # ... (code as provided previously) ...
#         sales_data = []
#         try:
#             sales_data = db.session.query(Part.name, db.func.sum(Transaction.amount).label('total_sales')).select_from(Transaction).join(Part, Part.id == Transaction.part_id).filter(Transaction.transaction_type == 'بيع').group_by(Part.name).order_by(db.desc('total_sales')).all()
#         except Exception as e: app.logger.error(f"Error generating sales by type report: {e}", exc_info=True); flash("حدث خطأ أثناء إنشاء تقرير المبيعات حسب النوع.", "error")
#         return render_template('sales_by_type.html', sales_data=sales_data)
#
#     @app.route('/reports/sales_by_date')
#     def sales_by_date():
#         # ... (code as provided previously) ...
#         processed_sales_data = []
#         try:
#             sales_query_result = db.session.query(db.func.date(Transaction.date).label('sale_date_str'), db.func.sum(Transaction.amount).label('daily_total')).filter(Transaction.transaction_type == 'بيع').group_by(db.func.date(Transaction.date)).order_by(db.desc(db.func.date(Transaction.date))).all()
#             for row in sales_query_result:
#                 sale_date_obj = None; daily_total = row.daily_total
#                 if row.sale_date_str:
#                     try: sale_date_obj = datetime.strptime(row.sale_date_str, '%Y-%m-%d').date()
#                     except ValueError: app.logger.warning(f"Could not parse date string in sales_by_date report: {row.sale_date_str}")
#                 processed_sales_data.append({'sale_date': sale_date_obj, 'daily_total': daily_total})
#         except Exception as e: app.logger.error(f"Error generating sales by date report: {e}", exc_info=True); flash("حدث خطأ أثناء إنشاء تقرير المبيعات حسب التاريخ.", "error")
#         return render_template('sales_by_date.html', sales_data=processed_sales_data)
#
#
#     # --- Main Execution ---
#     if __name__ == '__main__':
#         with app.app_context():
#             try:
#                 app.logger.info("Checking/Creating database tables...")
#                 db.create_all()
#                 app.logger.info("Database tables checked/created.")
#                 if not Customer.query.filter_by(name="بيع نقدي").first():
#                     app.logger.info("Default 'بيع نقدي' customer not found, creating...")
#                     try:
#                         cash_customer = Customer(name="بيع نقدي")
#                         db.session.add(cash_customer)
#                         db.session.commit()
#                         app.logger.info("Default 'بيع نقدي' customer created.")
#                     except Exception as e_cust:
#                         db.session.rollback()
#                         app.logger.error(f"Error creating default customer: {e_cust}", exc_info=True)
#             except Exception as e_db:
#                 app.logger.error(f"Error during database initialization: {e_db}", exc_info=True)
#
#         app.logger.info("Starting Flask application...")
#         # Use debug=False in production and a proper WSGI server
#         app.run(debug=True, host='0.0.0.0', port=5000)
#
#     # # print("if there is problem send viber massege to 07501783534 ") # Informational print
#     #
#     # # --- Imports ---
#     # from flask import Flask, render_template, request, redirect, flash, url_for, session, abort # Added session, abort
#     # from flask_sqlalchemy import SQLAlchemy
#     # import os
#     # from datetime import datetime, date, timezone # Make sure date and timezone are imported
#     # import logging
#     #
#     # # --- App Configuration ---
#     # app = Flask(__name__)
#     # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'
#     # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#     # # !!! غير هذا المفتاح السري إلى قيمة قوية وفريدة في بيئة الإنتاج !!!
#     # # !!! يفضل استخدام متغيرات البيئة: os.environ.get('FLASK_SECRET_KEY', 'default_dev_key') !!!
#     # app.config['SECRET_KEY'] = 'replace_this_with_a_real_secret_key_3984ur'
#     # db = SQLAlchemy(app)
#     #
#     # # --- Basic Logging Setup ---
#     # logging.basicConfig(level=logging.INFO)
#     #
#     # # --- Database Models ---
#     # class Customer(db.Model):
#     #     id = db.Column(db.Integer, primary_key=True)
#     #     name = db.Column(db.String(150), nullable=False, unique=True)
#     #     # Relationship: One-to-Many (Customer -> Transactions)
#     #     # 'sales' is a dynamic relationship, meaning query objects are returned.
#     #     sales = db.relationship('Transaction', back_populates='customer', lazy='dynamic')
#     #     def __repr__(self): return f'<Customer {self.name}>'
#     #
#     # class Part(db.Model):
#     #     id = db.Column(db.Integer, primary_key=True)
#     #     name = db.Column(db.String(100), nullable=False)
#     #     description = db.Column(db.String(200), nullable=True) # الوصف
#     #     description1 = db.Column(db.String(200), nullable=True) # اشترى من / المصدر
#     #     part_number = db.Column(db.String(50), nullable=True)
#     #     quantity = db.Column(db.Integer, default=0, nullable=False)
#     #     selling_price = db.Column(db.Float, default=0.0, nullable=False) # Consider using Numeric/Decimal for currency
#     #     # Relationship: One-to-Many (Part -> Transactions)
#     #     # cascade="all, delete-orphan": If a Part is deleted, its Transactions are also deleted.
#     #     transactions = db.relationship('Transaction', back_populates='part', lazy=True, cascade="all, delete-orphan")
#     #     def __repr__(self): return f'<Part {self.name}>'
#     #
#     # class Transaction(db.Model):
#     #     id = db.Column(db.Integer, primary_key=True)
#     #     transaction_type = db.Column(db.String(20), nullable=False) # 'شراء' or 'بيع'
#     #     amount = db.Column(db.Float, nullable=False) # Consider using Numeric/Decimal
#     #     # Use timezone aware default for consistency
#     #     date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
#     #     # Foreign Keys to establish relationships
#     #     part_id = db.Column(db.Integer, db.ForeignKey('part.id'), nullable=False)
#     #     customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=True) # Nullable for 'شراء'
#     #     # Relationships back to Part and Customer
#     #     part = db.relationship('Part', back_populates='transactions')
#     #     customer = db.relationship('Customer', back_populates='sales')
#     #     def __repr__(self):
#     #         part_name = self.part.name if self.part else "N/A"
#     #         cust_info = f" - Cust: {self.customer.name}" if self.transaction_type == 'بيع' and self.customer else ""
#     #         return f'<Transaction {self.transaction_type} ({self.id}) - Part: {part_name}{cust_info} - Amt: {self.amount}>'
#     #
#     # # --- Routes ---
#     #
#     # @app.route('/')
#     # def index():
#     #     """Redirects to the main parts list."""
#     #     return redirect(url_for('list_parts'))
#     #
#     # @app.route('/parts')
#     # def list_parts():
#     #     """Displays the list of parts with search and sell options."""
#     #     # === Get search term from query parameters ===
#     #     search_term = request.args.get('search', '').strip()
#     #
#     #     # Fetch customers for the sell dropdown
#     #     customers = Customer.query.order_by(Customer.name).all()
#     #
#     #     # === Build the base query ===
#     #     query = Part.query
#     #
#     #     # === Apply filter if search term exists ===
#     #     if search_term:
#     #         # Search in name or part number field (case-insensitive for SQLite by default)
#     #         search_filter = db.or_(
#     #             Part.name.contains(search_term),
#     #             Part.part_number.contains(search_term)
#     #         )
#     #         query = query.filter(search_filter)
#     #
#     #     # === Execute the (potentially filtered) query ===
#     #     parts = query.order_by(Part.name).all()
#     #
#     #     # === Pass search_term back to template to display in search box ===
#     #     return render_template('parts.html', parts=parts, customers=customers, search_term=search_term)
#     #
#     # # --- Parts CRUD ---
#     # @app.route('/parts/add', methods=['GET', 'POST'])
#     # def add_part():
#     #     """Adds a new part or updates quantity if it exists."""
#     #     if request.method == 'POST':
#     #         try:
#     #             name = request.form['name'].strip()
#     #             description = request.form.get('description', '').strip()
#     #             description1 = request.form.get('description1', '').strip() # Often 'Supplier' or 'Source'
#     #             part_number = request.form.get('part_number', '').strip()
#     #
#     #             if not name:
#     #                 flash('اسم الجزء مطلوب.', 'error')
#     #                 return render_template('add_part.html') # Re-render form
#     #
#     #             try:
#     #                 quantity = int(request.form['quantity'])
#     #                 selling_price = float(request.form['selling_price'])
#     #             except ValueError:
#     #                 flash('الرجاء إدخال أرقام صالحة للكمية وسعر البيع.', 'error')
#     #                 return render_template('add_part.html') # Re-render form
#     #
#     #             if quantity < 0 or selling_price < 0:
#     #                 flash('الكمية والسعر يجب ألا تكونا سالبتين.', 'error')
#     #                 return render_template('add_part.html') # Re-render form
#     #
#     #             # Check if part with same name and part number exists
#     #             existing_part = Part.query.filter_by(name=name, part_number=part_number).first()
#     #
#     #             if existing_part:
#     #                 # Update existing part
#     #                 existing_part.description = description
#     #                 existing_part.description1 = description1
#     #                 existing_part.selling_price = selling_price
#     #                 existing_part.quantity += quantity # Increase quantity
#     #                 db.session.commit()
#     #                 part_id_for_transaction = existing_part.id
#     #                 flash(f'تم تحديث الجزء "{existing_part.name}" وزيادة الكمية بمقدار {quantity}.', 'success')
#     #             else:
#     #                 # Add new part
#     #                 new_part = Part(
#     #                     name=name, description=description, description1=description1,
#     #                     part_number=part_number, quantity=quantity, selling_price=selling_price
#     #                 )
#     #                 db.session.add(new_part)
#     #                 db.session.flush() # Get the ID before committing fully
#     #                 part_id_for_transaction = new_part.id
#     #                 db.session.commit()
#     #                 flash(f'تمت إضافة جزء جديد "{new_part.name}".', 'success')
#     #
#     #             # Add a 'Purchase' transaction if quantity was added
#     #             if quantity > 0:
#     #                 # Calculate purchase amount (using selling price here might be inaccurate if purchase cost differs)
#     #                 # Consider adding a 'purchase_price' field to Part or Transaction
#     #                 purchase_amount = quantity * selling_price # Or use a dedicated purchase price
#     #                 transaction = Transaction(
#     #                     transaction_type='شراء',
#     #                     amount=purchase_amount,
#     #                     part_id=part_id_for_transaction
#     #                 )
#     #                 db.session.add(transaction)
#     #                 db.session.commit()
#     #
#     #             return redirect(url_for('list_parts'))
#     #
#     #         except Exception as e:
#     #              db.session.rollback() # Rollback on any error
#     #              app.logger.error(f"Error adding/updating part: {e}", exc_info=True)
#     #              flash('حدث خطأ غير متوقع أثناء إضافة/تحديث الجزء.', 'error')
#     #              # Re-render form, potentially preserving entered data if needed
#     #              return render_template('add_part.html', form_data=request.form)
#     #
#     #     # GET request: just show the empty form
#     #     return render_template('add_part.html')
#     #
#     #
#     # @app.route('/parts/sell/<int:id>', methods=['POST'])
#     # def sell_part(id):
#     #     """Sells a specified quantity of a part to a selected customer (Single Item Sale)."""
#     #     # Use db.session.get() for fetching by primary key
#     #     part = db.session.get(Part, id)
#     #     if not part:
#     #         app.logger.warning(f"Sell attempt for non-existent part ID: {id}")
#     #         abort(404) # Use abort for standard HTTP errors
#     #
#     #     try:
#     #         try:
#     #             quantity_to_sell = int(request.form['quantity'])
#     #         except ValueError:
#     #             flash('الرجاء إدخال كمية بيع رقمية صالحة.', 'error')
#     #             return redirect(url_for('list_parts'))
#     #
#     #         if quantity_to_sell <= 0:
#     #             flash('كمية البيع يجب أن تكون أكبر من صفر.', 'error')
#     #             return redirect(url_for('list_parts'))
#     #
#     #         customer_id_str = request.form.get('customer_id')
#     #         if not customer_id_str:
#     #             flash('الرجاء اختيار عميل لإتمام عملية البيع.', 'error')
#     #             return redirect(url_for('list_parts'))
#     #
#     #         try:
#     #             customer_id = int(customer_id_str)
#     #             # Optional: Check if customer exists
#     #             customer = db.session.get(Customer, customer_id)
#     #             if not customer:
#     #                 flash('العميل المختار غير موجود.', 'error')
#     #                 return redirect(url_for('list_parts'))
#     #         except ValueError:
#     #             flash('معرف العميل غير صالح.', 'error')
#     #             return redirect(url_for('list_parts'))
#     #
#     #
#     #         if quantity_to_sell > part.quantity:
#     #             flash(f'الكمية المطلوبة ({quantity_to_sell}) غير متوفرة للجزء "{part.name}". المتوفر: {part.quantity}', 'error')
#     #             return redirect(url_for('list_parts'))
#     #
#     #         # Process the sale
#     #         part.quantity -= quantity_to_sell
#     #         sale_amount = quantity_to_sell * part.selling_price
#     #         transaction = Transaction(
#     #             transaction_type='بيع',
#     #             amount=sale_amount,
#     #             part_id=part.id,
#     #             customer_id=customer_id
#     #         )
#     #         db.session.add(transaction)
#     #         db.session.commit()
#     #         flash(f'تم بيع {quantity_to_sell} من الجزء "{part.name}" للعميل "{customer.name}".', 'success')
#     #
#     #     except Exception as e:
#     #         db.session.rollback()
#     #         app.logger.error(f"Error selling part {id}: {e}", exc_info=True)
#     #         flash('حدث خطأ أثناء عملية البيع.', 'error')
#     #
#     #     return redirect(url_for('list_parts'))
#     #
#     #
#     # @app.route('/parts/delete/<int:id>', methods=['POST'])
#     # def delete_part(id):
#     #     """Deletes a part and its associated transactions (via cascade)."""
#     #     part = db.session.get(Part, id)
#     #     if not part:
#     #         app.logger.warning(f"Delete attempt for non-existent part ID: {id}")
#     #         flash('الجزء المراد حذفه غير موجود.', 'error')
#     #         return redirect(url_for('list_parts'))
#     #
#     #     try:
#     #         part_name = part.name # Get name before deletion for the flash message
#     #         db.session.delete(part) # Cascade should handle associated transactions
#     #         db.session.commit()
#     #         flash(f'تم حذف الجزء "{part_name}" وجميع معاملاته بنجاح.', 'success')
#     #     except Exception as e:
#     #         db.session.rollback()
#     #         app.logger.error(f"Error deleting part {id}: {e}", exc_info=True)
#     #         flash('حدث خطأ أثناء حذف الجزء.', 'error')
#     #
#     #     return redirect(url_for('list_parts'))
#     #
#     # @app.route('/parts/edit/<int:id>', methods=['GET', 'POST'])
#     # def edit_part(id):
#     #     """Edits details of an existing part."""
#     #     part = db.session.get(Part, id)
#     #     if not part:
#     #         app.logger.warning(f"Edit attempt for non-existent part ID: {id}")
#     #         abort(404)
#     #
#     #     if request.method == 'POST':
#     #         try:
#     #             # Validate and update fields
#     #             part.name = request.form['name'].strip()
#     #             part.description = request.form.get('description', '').strip()
#     #             part.description1 = request.form.get('description1', '').strip()
#     #             part.part_number = request.form.get('part_number', '').strip()
#     #
#     #             if not part.name:
#     #                 flash('اسم الجزء مطلوب.', 'error')
#     #                 return render_template('edit_part.html', part=part) # Re-render form
#     #
#     #             try:
#     #                 new_quantity = int(request.form['quantity'])
#     #                 new_selling_price = float(request.form['selling_price'])
#     #             except ValueError:
#     #                 flash('الرجاء إدخال أرقام صالحة للكمية والسعر.', 'error')
#     #                 return render_template('edit_part.html', part=part) # Re-render form
#     #
#     #             if new_quantity < 0 or new_selling_price < 0:
#     #                 flash('الكمية والسعر يجب ألا تكونا سالبتين.', 'error')
#     #                 return render_template('edit_part.html', part=part) # Re-render form
#     #
#     #             # Update quantity and price
#     #             part.quantity = new_quantity
#     #             part.selling_price = new_selling_price
#     #
#     #             db.session.commit()
#     #             flash(f'تم تحديث بيانات الجزء "{part.name}" بنجاح.', 'success')
#     #             return redirect(url_for('list_parts'))
#     #
#     #         except Exception as e:
#     #             db.session.rollback()
#     #             app.logger.error(f"Error editing part {id}: {e}", exc_info=True)
#     #             flash('حدث خطأ أثناء التعديل.', 'error')
#     #             # Re-render form with original data in case of error during save
#     #             # Note: We re-fetch the part to discard potentially modified but uncommitted data
#     #             part = db.session.get(Part, id)
#     #             return render_template('edit_part.html', part=part)
#     #
#     #     # GET request: show the edit form with current data
#     #     return render_template('edit_part.html', part=part)
#     #
#     #
#     # # --- Transactions ---
#     # @app.route('/transactions')
#     # def list_transactions():
#     #     """Displays a list of all transactions, newest first."""
#     #     # Eager load related Part and Customer data to avoid N+1 queries in the template
#     #     transactions = Transaction.query.options(
#     #         db.joinedload(Transaction.part),
#     #         db.joinedload(Transaction.customer)
#     #     ).order_by(Transaction.date.desc()).all()
#     #     return render_template('transactions.html', transactions=transactions)
#     #
#     # @app.route('/transactions/delete/<int:id>', methods=['POST'])
#     # def delete_transaction(id):
#     #     """
#     #     Deletes a transaction.
#     #     WARNING: Reversing quantity changes automatically is complex and error-prone.
#     #              Current implementation is a basic estimate and might be inaccurate.
#     #              Consider implementing a 'void' status instead of deletion for auditability.
#     #     """
#     #     # !!! IMPORTANT SECURITY WARNING: Password check is client-side and insecure. !!!
#     #     # !!! Implement proper server-side authentication/authorization before using !!!
#     #     # !!! this feature in a real application.                                   !!!
#     #
#     #     transaction = db.session.get(Transaction, id)
#     #     if not transaction:
#     #          app.logger.warning(f"Delete attempt for non-existent transaction ID: {id}")
#     #          flash('المعاملة غير موجودة.', 'error')
#     #          return redirect(url_for('list_transactions'))
#     #
#     #     part = transaction.part # Access related part (SQLAlchemy will lazy load if not already loaded)
#     #
#     #     # Attempt to reverse quantity change (use with caution!)
#     #     if part:
#     #         try:
#     #             # This assumes amount directly relates to quantity via current selling price, which might be wrong.
#     #             if part.selling_price is not None and part.selling_price > 0:
#     #                 # Estimate quantity based on amount and current price
#     #                 quantity_change_estimate = round(transaction.amount / part.selling_price) # Round to nearest integer
#     #                 if transaction.transaction_type == 'شراء':
#     #                      # Reversing a purchase: decrease quantity
#     #                      part.quantity = max(0, part.quantity - quantity_change_estimate)
#     #                 elif transaction.transaction_type == 'بيع':
#     #                      # Reversing a sale: increase quantity
#     #                      part.quantity += quantity_change_estimate
#     #                 # part.quantity should already be committed if part exists,
#     #                 # but we modify it here before deleting the transaction.
#     #             else:
#     #                 flash('لم يتم تعديل كمية الجزء تلقائياً لأن سعر البيع الحالي للجزء غير صالح أو صفر.', 'warning')
#     #         except Exception as qty_e:
#     #              app.logger.error(f"Error adjusting quantity for part {part.id} while deleting tx {id}: {qty_e}", exc_info=True)
#     #              flash('حدث خطأ أثناء محاولة تعديل كمية الجزء.', 'error')
#     #     else:
#     #          flash('الجزء المرتبط بهذه المعاملة غير موجود (ربما تم حذفه). سيتم حذف المعاملة فقط.', 'warning')
#     #
#     #     try:
#     #         # Delete the transaction itself
#     #         db.session.delete(transaction)
#     #         db.session.commit()
#     #         flash('تم حذف المعاملة بنجاح.', 'success')
#     #     except Exception as e:
#     #         db.session.rollback() # Rollback quantity changes and transaction deletion
#     #         app.logger.error(f"Error deleting transaction {id}: {e}", exc_info=True)
#     #         flash('حدث خطأ أثناء حذف المعاملة.', 'error')
#     #
#     #     return redirect(url_for('list_transactions'))
#     #
#     # # --- Customer Routes ---
#     # @app.route('/customers')
#     # def list_customers():
#     #     """Displays a list of all customers."""
#     #     customers = Customer.query.order_by(Customer.name).all()
#     #     return render_template('customers.html', customers=customers)
#     #
#     # @app.route('/customers/add', methods=['GET', 'POST'])
#     # def add_customer():
#     #     """Adds a new customer to the database."""
#     #     if request.method == 'POST':
#     #         name = request.form.get('name', '').strip()
#     #         if not name:
#     #             flash('اسم العميل مطلوب.', 'error')
#     #             # Re-render form, passing back entered name if desired
#     #             return render_template('add_customer.html', name=name)
#     #         else:
#     #             # Check if customer already exists (case-insensitive check)
#     #             existing = Customer.query.filter(Customer.name.ilike(name)).first()
#     #             if existing:
#     #                 flash(f'العميل "{name}" موجود بالفعل.', 'warning')
#     #                 # Re-render form, passing back entered name
#     #                 return render_template('add_customer.html', name=name)
#     #             else:
#     #                 try:
#     #                     new_customer = Customer(name=name)
#     #                     db.session.add(new_customer)
#     #                     db.session.commit()
#     #                     flash(f'تمت إضافة العميل "{name}" بنجاح.', 'success')
#     #                     return redirect(url_for('list_customers'))
#     #                 except Exception as e:
#     #                     db.session.rollback()
#     #                     app.logger.error(f"Error adding customer '{name}': {e}", exc_info=True)
#     #                     flash('حدث خطأ أثناء إضافة العميل.', 'error')
#     #                     # Re-render form, passing back entered name
#     #                     return render_template('add_customer.html', name=name)
#     #
#     #     # GET request: show the empty form
#     #     return render_template('add_customer.html')
#     #
#     # @app.route('/customers/edit/<int:id>', methods=['GET', 'POST'])
#     # def edit_customer(id):
#     #     """Edits an existing customer's details."""
#     #     customer = db.session.get(Customer, id)
#     #     if not customer:
#     #          app.logger.warning(f"Edit attempt for non-existent customer ID: {id}")
#     #          abort(404)
#     #
#     #     if request.method == 'POST':
#     #         new_name = request.form.get('name', '').strip()
#     #         if not new_name:
#     #             flash('اسم العميل مطلوب.', 'error')
#     #             # Re-render edit form with original customer data
#     #             return render_template('edit_customer.html', customer=customer)
#     #         else:
#     #             # Check if *another* customer already has the new name (case-insensitive)
#     #             existing = Customer.query.filter(Customer.name.ilike(new_name), Customer.id != id).first()
#     #             if existing:
#     #                 flash(f'اسم العميل "{new_name}" مستخدم بالفعل لعميل آخر.', 'error')
#     #                 # Re-render edit form, passing back the *attempted* new name
#     #                 return render_template('edit_customer.html', customer=customer, submitted_name=new_name)
#     #             else:
#     #                 try:
#     #                     customer.name = new_name
#     #                     db.session.commit()
#     #                     flash(f'تم تحديث بيانات العميل بنجاح.', 'success') # Removed name from flash as it's now the new name
#     #                     return redirect(url_for('list_customers'))
#     #                 except Exception as e:
#     #                     db.session.rollback()
#     #                     app.logger.error(f"Error editing customer {id}: {e}", exc_info=True)
#     #                     flash('حدث خطأ أثناء تعديل العميل.', 'error')
#     #                     # Re-render edit form with original data
#     #                     return render_template('edit_customer.html', customer=customer)
#     #
#     #     # GET request: show the edit form with current customer data
#     #     return render_template('edit_customer.html', customer=customer)
#     #
#     # @app.route('/customers/delete/<int:id>', methods=['POST'])
#     # def delete_customer(id):
#     #      """Deletes a customer only if they have no associated sales."""
#     #      customer = db.session.get(Customer, id)
#     #      if not customer:
#     #          app.logger.warning(f"Delete attempt for non-existent customer ID: {id}")
#     #          flash('العميل غير موجود.', 'error')
#     #          return redirect(url_for('list_customers'))
#     #
#     #      # Use the relationship count for efficiency or check first()
#     #      # customer.sales.count() > 0 is often efficient
#     #      if customer.sales.first(): # Checks if at least one sale exists
#     #         flash(f'لا يمكن حذف العميل "{customer.name}" لأنه مرتبط بمعاملات بيع.', 'error')
#     #      else:
#     #         try:
#     #             customer_name = customer.name # Get name for flash message
#     #             db.session.delete(customer)
#     #             db.session.commit()
#     #             flash(f'تم حذف العميل "{customer_name}" بنجاح.', 'success')
#     #         except Exception as e:
#     #             db.session.rollback()
#     #             app.logger.error(f"Error deleting customer {id}: {e}", exc_info=True)
#     #             flash('حدث خطأ أثناء حذف العميل.', 'error')
#     #
#     #      return redirect(url_for('list_customers'))
#     #
#     # @app.route('/customers/<int:id>/sales')
#     # def customer_sales_report(id):
#     #     """Displays a historical sales report for a specific customer."""
#     #     customer = db.session.get(Customer, id)
#     #     if not customer:
#     #         app.logger.warning(f"Sales report attempt for non-existent customer ID: {id}")
#     #         abort(404)
#     #
#     #     # Query sales transactions for this customer, eager load Part info
#     #     sales_list = Transaction.query.options(db.joinedload(Transaction.part))\
#     #                                   .filter_by(customer_id=id, transaction_type='بيع')\
#     #                                   .order_by(Transaction.date.desc())\
#     #                                   .all()
#     #
#     #     # Calculate grand total on the server side
#     #     grand_total = sum(sale.amount for sale in sales_list if sale.amount is not None)
#     #
#     #     return render_template('customer_sales.html', customer=customer, sales_list=sales_list, grand_total=grand_total)
#     #
#     # # --- Temporary List/Invoice Preparation Routes ---
#     #
#     # @app.route('/list/prepare/<int:customer_id>', methods=['GET', 'POST'])
#     # def prepare_customer_list(customer_id):
#     #     """Page to build a temporary list of parts for a customer using session."""
#     #     customer = db.session.get(Customer, customer_id)
#     #     if not customer:
#     #         app.logger.warning(f"Prepare list attempt for non-existent customer ID: {customer_id}")
#     #         flash(f'العميل بالمعرف {customer_id} غير موجود.', 'error')
#     #         return redirect(url_for('list_customers'))
#     #
#     #     session_key = f'current_list_{customer_id}'
#     #
#     #     # Initialize session list if not present
#     #     if session_key not in session:
#     #         session[session_key] = []
#     #
#     #     if request.method == 'POST':
#     #         # --- POST: Add item to the list ---
#     #         try:
#     #             part_id_str = request.form.get('part_id')
#     #             quantity_str = request.form.get('quantity', '1') # Default to 1 if not provided
#     #
#     #             if not part_id_str or not quantity_str:
#     #                  flash('الرجاء اختيار الجزء وإدخال الكمية.', 'error')
#     #                  return redirect(url_for('prepare_customer_list', customer_id=customer_id))
#     #
#     #             part_id = int(part_id_str)
#     #             quantity = int(quantity_str)
#     #
#     #             part = db.session.get(Part, part_id)
#     #
#     #             if not part:
#     #                 flash('الجزء المختار غير موجود.', 'error')
#     #             elif quantity <= 0:
#     #                 flash('الكمية يجب أن تكون أكبر من صفر.', 'error')
#     #             # Check available quantity *before* adding to list
#     #             elif quantity > part.quantity:
#     #                 flash(f'الكمية المطلوبة ({quantity}) غير متوفرة للجزء "{part.name}". المتوفر: {part.quantity}', 'error')
#     #             else:
#     #                 # Process adding to list
#     #                 current_list = session.get(session_key, []) # Get fresh copy
#     #                 found = False
#     #                 for item in current_list:
#     #                     if item['part_id'] == part_id:
#     #                         # Item exists, update quantity if possible
#     #                         new_total_qty = item['qty'] + quantity
#     #                         if new_total_qty > part.quantity:
#     #                             flash(f'لا يمكن إضافة {quantity} من "{part.name}". الإجمالي المطلوب ({new_total_qty}) يتجاوز الكمية المتوفرة حالياً ({part.quantity}).', 'error')
#     #                         else:
#     #                             item['qty'] = new_total_qty
#     #                             item['total'] = round(item['qty'] * item['price'], 2) # Recalculate total
#     #                             flash(f'تم تحديث كمية "{part.name}" في القائمة.', 'success')
#     #                         found = True
#     #                         break
#     #
#     #                 if not found:
#     #                     # Item not in list, add it
#     #                     if quantity > part.quantity: # Double check just in case
#     #                          flash(f'الكمية المطلوبة ({quantity}) غير متوفرة للجزء "{part.name}". المتوفر: {part.quantity}', 'error')
#     #                     else:
#     #                         item_total = round(quantity * part.selling_price, 2)
#     #                         current_list.append({
#     #                             'part_id': part.id,
#     #                             'name': part.name,
#     #                             'part_number': part.part_number,
#     #                             'qty': quantity,
#     #                             'price': part.selling_price,
#     #                             'total': item_total
#     #                         })
#     #                         flash(f'تمت إضافة {quantity} من "{part.name}" إلى القائمة.', 'success')
#     #
#     #                 # Save updated list back to session if changes were potentially made
#     #                 # The flash message logic above implies whether a change was intended or blocked
#     #                 session[session_key] = current_list
#     #                 session.modified = True # Important: Mark session as modified
#     #
#     #         except ValueError:
#     #              flash('الرجاء إدخال معرف جزء وكمية صحيحة.', 'error')
#     #         except Exception as e:
#     #              flash(f'حدث خطأ غير متوقع أثناء إضافة الجزء: {e}', 'error')
#     #              app.logger.error(f"Error adding item to list for customer {customer_id}: {e}", exc_info=True)
#     #
#     #         # Redirect back to the prepare page (GET request) after processing POST
#     #         return redirect(url_for('prepare_customer_list', customer_id=customer_id))
#     #
#     #     # --- GET Request Logic ---
#     #     # Fetch available parts (quantity > 0) for the dropdown
#     #     parts_available = Part.query.filter(Part.quantity > 0).order_by(Part.name).all()
#     #     # Get the current list items from session
#     #     current_list_items = session.get(session_key, [])
#     #     # Calculate grand total for display
#     #     grand_total = sum(item['total'] for item in current_list_items)
#     #     # Get current time for potential printing
#     #     current_time_utc = datetime.now(timezone.utc)
#     #
#     #     return render_template('prepare_list.html',
#     #                            customer=customer,
#     #                            parts=parts_available,
#     #                            current_list=current_list_items,
#     #                            grand_total=grand_total,
#     #                            session_key=session_key, # Pass session key if needed in template (e.g., for JS)
#     #                            current_time=current_time_utc)
#     #
#     #
#     # @app.route('/list/clear/<int:customer_id>', methods=['POST'])
#     # def clear_customer_list(customer_id):
#     #     """Clears the temporary list for a customer from the session."""
#     #     session_key = f'current_list_{customer_id}'
#     #     if session_key in session:
#     #         session.pop(session_key, None)
#     #         session.modified = True
#     #         flash('تم مسح القائمة الحالية.', 'success')
#     #     else:
#     #         flash('القائمة فارغة بالفعل.', 'info')
#     #     return redirect(url_for('prepare_customer_list', customer_id=customer_id))
#     #
#     #
#     # @app.route('/list/finalize/<int:customer_id>', methods=['POST'])
#     # def finalize_customer_list(customer_id):
#     #     """Finalizes the sale: Creates transactions, updates stock, and clears the temporary list."""
#     #     customer = db.session.get(Customer, customer_id)
#     #     if not customer:
#     #         flash(f'العميل بالمعرف {customer_id} غير موجود.', 'error')
#     #         return redirect(url_for('list_customers')) # Redirect to customer list if customer not found
#     #
#     #     session_key = f'current_list_{customer_id}'
#     #     current_list_items = session.get(session_key, [])
#     #
#     #     if not current_list_items:
#     #         flash('القائمة فارغة، لا يوجد شيء لإتمامه.', 'warning')
#     #         return redirect(url_for('prepare_customer_list', customer_id=customer_id))
#     #
#     #     # --- Transaction Block: Ensure atomicity ---
#     #     try:
#     #         # 1. Re-verify stock availability for all items in the list
#     #         parts_to_update = {}
#     #         with db.session.no_autoflush: # Prevent premature flushes within the loop
#     #             for item in current_list_items:
#     #                 part = db.session.get(Part, item['part_id'])
#     #                 if not part:
#     #                     # Part deleted since adding to list? Critical error.
#     #                     db.session.rollback() # Rollback any potential changes
#     #                     flash(f'خطأ حرج: الجزء "{item["name"]}" (ID: {item["part_id"]}) لم يعد موجوداً. تم إلغاء العملية.', 'error')
#     #                     return redirect(url_for('prepare_customer_list', customer_id=customer_id))
#     #
#     #                 if item['qty'] > part.quantity:
#     #                     # Stock changed since adding to list. Abort.
#     #                     db.session.rollback()
#     #                     flash(f'الكمية المطلوبة ({item["qty"]}) غير متوفرة الآن للجزء "{item["name"]}" (المتوفر: {part.quantity}). يرجى مراجعة القائمة وتحديثها. تم إلغاء العملية.', 'error')
#     #                     return redirect(url_for('prepare_customer_list', customer_id=customer_id))
#     #
#     #                 parts_to_update[part.id] = part # Store fetched part for update
#     #
#     #         # 2. If all stock checks pass, proceed with updates and transaction creation
#     #         total_sale_amount = 0
#     #         transactions_to_add = []
#     #         for item in current_list_items:
#     #             part = parts_to_update[item['part_id']] # Get the already fetched part
#     #             # Decrease stock quantity
#     #             part.quantity -= item['qty']
#     #             # Create sale transaction
#     #             transaction = Transaction(
#     #                 transaction_type='بيع',
#     #                 amount=item['total'], # Use the total calculated when added to list
#     #                 part_id=item['part_id'],
#     #                 customer_id=customer_id,
#     #                 date=datetime.now(timezone.utc) # Ensure consistent date for all items in the sale
#     #             )
#     #             transactions_to_add.append(transaction)
#     #             total_sale_amount += item['total']
#     #
#     #         # 3. Add all new transactions to the session
#     #         db.session.add_all(transactions_to_add)
#     #
#     #         # 4. Commit all changes (stock updates and new transactions)
#     #         db.session.commit()
#     #
#     #         # 5. Clear the list from the session only after successful commit
#     #         session.pop(session_key, None)
#     #         session.modified = True
#     #
#     #         # Use total_sale_amount calculated correctly
#     #         flash(f'تم إتمام عملية البيع بنجاح للعميل "{customer.name}" بمبلغ إجمالي {total_sale_amount:.2f}.', 'success')
#     #         # Redirect to customer list or perhaps customer's sales report?
#     #         return redirect(url_for('list_customers'))
#     #         # return redirect(url_for('customer_sales_report', id=customer_id)) # Alternative redirect
#     #
#     #     except Exception as e:
#     #         # Rollback the entire transaction if any error occurs during the process
#     #         db.session.rollback()
#     #         app.logger.error(f"Error finalizing list for customer {customer_id}: {e}", exc_info=True)
#     #         flash('حدث خطأ فادح أثناء إتمام عملية البيع. لم يتم تحديث المخزون أو إضافة المعاملات.', 'error')
#     #         return redirect(url_for('prepare_customer_list', customer_id=customer_id))
#     #
#     #
#     # # --- Reporting Routes ---
#     # @app.route('/reports/sales_by_type')
#     # def sales_by_type():
#     #     """Displays a report summing sales amount by part name."""
#     #     sales_data = []
#     #     try:
#     #         # Query to sum transaction amounts, grouped by part name, for 'بيع' type
#     #         sales_data = db.session.query(
#     #                 Part.name,
#     #                 db.func.sum(Transaction.amount).label('total_sales')
#     #             )\
#     #             .select_from(Transaction)\
#     #             .join(Part, Part.id == Transaction.part_id)\
#     #             .filter(Transaction.transaction_type == 'بيع')\
#     #             .group_by(Part.name)\
#     #             .order_by(db.desc('total_sales'))\
#     #             .all()
#     #     except Exception as e:
#     #         app.logger.error(f"Error generating sales by type report: {e}", exc_info=True)
#     #         flash("حدث خطأ أثناء إنشاء تقرير المبيعات حسب النوع.", "error")
#     #     return render_template('sales_by_type.html', sales_data=sales_data)
#     #
#     #
#     # @app.route('/reports/sales_by_date')
#     # def sales_by_date():
#     #     """Displays a report summing sales amount by date."""
#     #     processed_sales_data = []
#     #     try:
#     #         # Query to sum transaction amounts, grouped by date part of the timestamp
#     #         sales_query_result = db.session.query(
#     #                 db.func.date(Transaction.date).label('sale_date_str'), # Extract date part as string
#     #                 db.func.sum(Transaction.amount).label('daily_total')
#     #             )\
#     #             .filter(Transaction.transaction_type == 'بيع')\
#     #             .group_by(db.func.date(Transaction.date))\
#     #             .order_by(db.desc(db.func.date(Transaction.date)))\
#     #             .all()
#     #
#     #         # Process results to convert date string back to date object if needed
#     #         for row in sales_query_result:
#     #             sale_date_obj = None
#     #             daily_total = row.daily_total
#     #             if row.sale_date_str:
#     #                 try:
#     #                     # Convert 'YYYY-MM-DD' string back to Python date object
#     #                     sale_date_obj = datetime.strptime(row.sale_date_str, '%Y-%m-%d').date()
#     #                 except ValueError:
#     #                     app.logger.warning(f"Could not parse date string in sales_by_date report: {row.sale_date_str}")
#     #             processed_sales_data.append({
#     #                 'sale_date': sale_date_obj,
#     #                 'daily_total': daily_total
#     #             })
#     #
#     #     except Exception as e:
#     #         app.logger.error(f"Error generating sales by date report: {e}", exc_info=True)
#     #         flash("حدث خطأ أثناء إنشاء تقرير المبيعات حسب التاريخ.", "error")
#     #
#     #     return render_template('sales_by_date.html', sales_data=processed_sales_data)
#     #
#     #
#     # # --- Main Execution ---
#     # if __name__ == '__main__':
#     #     # Use application context for database operations during startup
#     #     with app.app_context():
#     #         try:
#     #             app.logger.info("Checking/Creating database tables...")
#     #             # create_all() only creates tables that don't exist.
#     #             # For schema changes on existing tables, use migrations (e.g., Alembic).
#     #             db.create_all()
#     #             app.logger.info("Database tables checked/created.")
#     #
#     #             # Check if the default 'Cash Sale' customer exists, create if not
#     #             if not Customer.query.filter_by(name="بيع نقدي").first():
#     #                 app.logger.info("Default 'بيع نقدي' customer not found, creating...")
#     #                 try:
#     #                     cash_customer = Customer(name="بيع نقدي")
#     #                     db.session.add(cash_customer)
#     #                     db.session.commit()
#     #                     app.logger.info("Default 'بيع نقدي' customer created.")
#     #                 except Exception as e_cust:
#     #                     db.session.rollback()
#     #                     app.logger.error(f"Error creating default customer: {e_cust}", exc_info=True)
#     #         except Exception as e_db:
#     #             app.logger.error(f"Error during database initialization: {e_db}", exc_info=True)
#     #             # Decide if the app should exit or continue if DB init fails
#     #
#     #     app.logger.info("Starting Flask application...")
#     #     # Use debug=False and potentially a different host/port in production
#     #     # Use a proper WSGI server (like Gunicorn or Waitress) in production instead of app.run()
#     #     app.run(debug=True, host='0.0.0.0', port=5000)
#     #
#     # # # print("if there is problem send viber massege to 07501783534 ") # Informational print
#     # #
#     # # # --- Imports ---
#     # # from flask import Flask, render_template, request, redirect, flash, url_for, session, abort # Added session, abort
#     # # from flask_sqlalchemy import SQLAlchemy
#     # # import os
#     # # from datetime import datetime, date, timezone # Make sure date and timezone are imported
#     # # import logging
#     # #
#     # # # --- App Configuration ---
#     # # app = Flask(__name__)
#     # # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'
#     # # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#     # # app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'replace_this_with_a_real_secret_key_3984ur') # CHANGE THIS KEY
#     # # db = SQLAlchemy(app)
#     # #
#     # # # --- Basic Logging Setup ---
#     # # logging.basicConfig(level=logging.INFO)
#     # #
#     # # # --- Database Models ---
#     # # class Customer(db.Model):
#     # #     id = db.Column(db.Integer, primary_key=True)
#     # #     name = db.Column(db.String(150), nullable=False, unique=True)
#     # #     sales = db.relationship('Transaction', back_populates='customer', lazy='dynamic')
#     # #     def __repr__(self): return f'<Customer {self.name}>'
#     # #
#     # # class Part(db.Model):
#     # #     id = db.Column(db.Integer, primary_key=True)
#     # #     name = db.Column(db.String(100), nullable=False)
#     # #     description = db.Column(db.String(200), nullable=True)
#     # #     description1 = db.Column(db.String(200), nullable=True)
#     # #     part_number = db.Column(db.String(50), nullable=True)
#     # #     quantity = db.Column(db.Integer, default=0, nullable=False)
#     # #     selling_price = db.Column(db.Float, default=0.0, nullable=False)
#     # #     transactions = db.relationship('Transaction', back_populates='part', lazy=True, cascade="all, delete-orphan")
#     # #     def __repr__(self): return f'<Part {self.name}>'
#     # #
#     # # class Transaction(db.Model):
#     # #     id = db.Column(db.Integer, primary_key=True)
#     # #     transaction_type = db.Column(db.String(20), nullable=False)
#     # #     amount = db.Column(db.Float, nullable=False)
#     # #     date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False) # Use timezone aware default
#     # #     part_id = db.Column(db.Integer, db.ForeignKey('part.id'), nullable=False)
#     # #     part = db.relationship('Part', back_populates='transactions')
#     # #     customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=True)
#     # #     customer = db.relationship('Customer', back_populates='sales')
#     # #     def __repr__(self):
#     # #         part_name = self.part.name if self.part else "N/A"
#     # #         cust_info = f" - Cust: {self.customer.name}" if self.transaction_type == 'بيع' and self.customer else ""
#     # #         return f'<Transaction {self.transaction_type} ({self.id}) - Part: {part_name}{cust_info} - Amt: {self.amount}>'
#     # #
#     # # # --- Routes ---
#     # #
#     # # @app.route('/')
#     # # def index():
#     # #     """Redirects to the main parts list."""
#     # #     return redirect(url_for('list_parts'))
#     # #
#     # # @app.route('/parts')
#     # # def list_parts():
#     # #     """Displays the list of parts with search and sell options."""
#     # #     search_term = request.args.get('search', '').strip()
#     # #     customers = Customer.query.order_by(Customer.name).all()
#     # #     query = Part.query
#     # #     if search_term:
#     # #         search_filter = db.or_(Part.name.contains(search_term), Part.part_number.contains(search_term))
#     # #         query = query.filter(search_filter)
#     # #     parts = query.order_by(Part.name).all()
#     # #     return render_template('parts.html', parts=parts, customers=customers, search_term=search_term)
#     # #
#     # # # --- Parts CRUD ---
#     # # @app.route('/parts/add', methods=['GET', 'POST'])
#     # # def add_part():
#     # #     """Adds a new part or updates quantity if it exists."""
#     # #     if request.method == 'POST':
#     # #         try:
#     # #             name = request.form['name'].strip()
#     # #             description = request.form.get('description', '').strip()
#     # #             description1 = request.form.get('description1', '').strip()
#     # #             part_number = request.form.get('part_number', '').strip()
#     # #             if not name: flash('اسم الجزء مطلوب.', 'error'); return render_template('add_part.html')
#     # #             try:
#     # #                 quantity = int(request.form['quantity'])
#     # #                 selling_price = float(request.form['selling_price'])
#     # #             except ValueError: flash('الرجاء إدخال أرقام صالحة للكمية وسعر البيع.', 'error'); return render_template('add_part.html')
#     # #             if quantity < 0 or selling_price < 0: flash('الكمية والسعر يجب ألا تكونا سالبتين.', 'error'); return render_template('add_part.html')
#     # #
#     # #             existing_part = Part.query.filter_by(name=name, part_number=part_number).first()
#     # #             if existing_part:
#     # #                 existing_part.description = description
#     # #                 existing_part.description1 = description1
#     # #                 existing_part.selling_price = selling_price
#     # #                 existing_part.quantity += quantity
#     # #                 db.session.commit()
#     # #                 part_id_for_transaction = existing_part.id
#     # #                 flash(f'تم تحديث الجزء "{existing_part.name}" وزيادة الكمية بمقدار {quantity}.', 'success')
#     # #             else:
#     # #                 new_part = Part(name=name, description=description, description1=description1, part_number=part_number, quantity=quantity, selling_price=selling_price)
#     # #                 db.session.add(new_part)
#     # #                 db.session.flush()
#     # #                 part_id_for_transaction = new_part.id
#     # #                 db.session.commit()
#     # #                 flash(f'تمت إضافة جزء جديد "{new_part.name}".', 'success')
#     # #
#     # #             if quantity > 0:
#     # #                 purchase_amount = quantity * selling_price
#     # #                 transaction = Transaction(transaction_type='شراء', amount=purchase_amount, part_id=part_id_for_transaction)
#     # #                 db.session.add(transaction)
#     # #                 db.session.commit()
#     # #             return redirect(url_for('list_parts'))
#     # #         except Exception as e:
#     # #              db.session.rollback()
#     # #              app.logger.error(f"Error adding/updating part: {e}", exc_info=True)
#     # #              flash(f'حدث خطأ غير متوقع أثناء إضافة/تحديث الجزء.', 'error')
#     # #              return render_template('add_part.html')
#     # #     return render_template('add_part.html')
#     # #
#     # #
#     # # @app.route('/parts/sell/<int:id>', methods=['POST'])
#     # # def sell_part(id):
#     # #     """Sells a specified quantity of a part to a selected customer (Single Item Sale)."""
#     # #     # Use db.session.get() instead of Part.query.get_or_404()
#     # #     part = db.session.get(Part, id)
#     # #     if not part:
#     # #         app.logger.warning(f"Sell attempt for non-existent part ID: {id}")
#     # #         abort(404) # Not found
#     # #
#     # #     try:
#     # #         try: quantity_to_sell = int(request.form['quantity'])
#     # #         except ValueError: flash('الرجاء إدخال كمية بيع رقمية صالحة.', 'error'); return redirect(url_for('list_parts'))
#     # #         if quantity_to_sell <= 0: flash('كمية البيع يجب أن تكون أكبر من صفر.', 'error'); return redirect(url_for('list_parts'))
#     # #
#     # #         customer_id_str = request.form.get('customer_id')
#     # #         if not customer_id_str: flash('الرجاء اختيار عميل لإتمام عملية البيع.', 'error'); return redirect(url_for('list_parts'))
#     # #         try: customer_id = int(customer_id_str)
#     # #         except ValueError: flash('معرف العميل غير صالح.', 'error'); return redirect(url_for('list_parts'))
#     # #         # Optional: Check if customer exists using db.session.get(Customer, customer_id)
#     # #
#     # #         if quantity_to_sell > part.quantity: flash(f'الكمية المطلوبة ({quantity_to_sell}) غير متوفرة للجزء "{part.name}". المتوفر: {part.quantity}', 'error'); return redirect(url_for('list_parts'))
#     # #
#     # #         part.quantity -= quantity_to_sell
#     # #         sale_amount = quantity_to_sell * part.selling_price
#     # #         transaction = Transaction(transaction_type='بيع', amount=sale_amount, part_id=part.id, customer_id=customer_id)
#     # #         db.session.add(transaction)
#     # #         db.session.commit()
#     # #         flash(f'تم بيع {quantity_to_sell} من الجزء "{part.name}".', 'success')
#     # #     except Exception as e:
#     # #         db.session.rollback()
#     # #         app.logger.error(f"Error selling part {id}: {e}", exc_info=True)
#     # #         flash(f'حدث خطأ أثناء عملية البيع.', 'error')
#     # #     return redirect(url_for('list_parts'))
#     # #
#     # #
#     # # @app.route('/parts/delete/<int:id>', methods=['POST'])
#     # # def delete_part(id):
#     # #     """Deletes a part and its associated transactions (via cascade)."""
#     # #     # Use db.session.get() instead of Part.query.get_or_404()
#     # #     part = db.session.get(Part, id)
#     # #     if not part:
#     # #         app.logger.warning(f"Delete attempt for non-existent part ID: {id}")
#     # #         flash('الجزء المراد حذفه غير موجود.', 'error')
#     # #         return redirect(url_for('list_parts'))
#     # #
#     # #     try:
#     # #         part_name = part.name
#     # #         db.session.delete(part)
#     # #         db.session.commit()
#     # #         flash(f'تم حذف الجزء "{part_name}" وجميع معاملاته بنجاح.', 'success')
#     # #     except Exception as e:
#     # #         db.session.rollback()
#     # #         app.logger.error(f"Error deleting part {id}: {e}", exc_info=True)
#     # #         flash(f'حدث خطأ أثناء حذف الجزء.', 'error')
#     # #     return redirect(url_for('list_parts'))
#     # #
#     # # @app.route('/parts/edit/<int:id>', methods=['GET', 'POST'])
#     # # def edit_part(id):
#     # #     """Edits details of an existing part."""
#     # #     # Use db.session.get() instead of Part.query.get_or_404()
#     # #     part = db.session.get(Part, id)
#     # #     if not part:
#     # #         app.logger.warning(f"Edit attempt for non-existent part ID: {id}")
#     # #         abort(404)
#     # #
#     # #     if request.method == 'POST':
#     # #         try:
#     # #             part.name = request.form['name'].strip()
#     # #             part.description = request.form.get('description', '').strip()
#     # #             part.description1 = request.form.get('description1', '').strip()
#     # #             part.part_number = request.form.get('part_number', '').strip()
#     # #             if not part.name: flash('اسم الجزء مطلوب.', 'error'); return render_template('edit_part.html', part=part)
#     # #             try:
#     # #                 new_quantity = int(request.form['quantity'])
#     # #                 new_selling_price = float(request.form['selling_price'])
#     # #             except ValueError: flash('الرجاء إدخال أرقام صالحة للكمية والسعر.', 'error'); return render_template('edit_part.html', part=part)
#     # #             if new_quantity < 0 or new_selling_price < 0: flash('الكمية والسعر يجب ألا تكونا سالبتين.', 'error'); return render_template('edit_part.html', part=part)
#     # #
#     # #             part.quantity = new_quantity
#     # #             part.selling_price = new_selling_price
#     # #             db.session.commit()
#     # #             flash(f'تم تحديث بيانات الجزء "{part.name}" بنجاح.', 'success')
#     # #             return redirect(url_for('list_parts'))
#     # #         except Exception as e:
#     # #             db.session.rollback()
#     # #             app.logger.error(f"Error editing part {id}: {e}", exc_info=True)
#     # #             flash(f'حدث خطأ أثناء التعديل.', 'error')
#     # #     return render_template('edit_part.html', part=part)
#     # #
#     # #
#     # # # --- Transactions ---
#     # # @app.route('/transactions')
#     # # def list_transactions():
#     # #     """Displays a list of all transactions."""
#     # #     transactions = Transaction.query.options(db.joinedload(Transaction.part), db.joinedload(Transaction.customer)).order_by(Transaction.date.desc()).all()
#     # #     return render_template('transactions.html', transactions=transactions)
#     # #
#     # # @app.route('/transactions/delete/<int:id>', methods=['POST'])
#     # # def delete_transaction(id):
#     # #     """Deletes a transaction and attempts to reverse the quantity change."""
#     # #     # Use db.session.get() instead of Transaction.query.options(...).get_or_404()
#     # #     transaction = db.session.get(Transaction, id)
#     # #     if not transaction:
#     # #          app.logger.warning(f"Delete attempt for non-existent transaction ID: {id}")
#     # #          flash('المعاملة غير موجودة.', 'error')
#     # #          return redirect(url_for('list_transactions'))
#     # #
#     # #     # Eager load part if not already loaded (get doesn't support options directly)
#     # #     # Alternatively, access transaction.part and SQLAlchemy will lazy load it if needed
#     # #     part = transaction.part # Access related part
#     # #
#     # #     if not part: flash('الجزء المرتبط بهذه المعاملة غير موجود. سيتم حذف المعاملة فقط.', 'warning')
#     # #     else:
#     # #         try:
#     # #             if part.selling_price is not None and part.selling_price > 0:
#     # #                 quantity_change_estimate = transaction.amount / part.selling_price
#     # #                 if transaction.transaction_type == 'شراء': part.quantity -= quantity_change_estimate
#     # #                 elif transaction.transaction_type == 'بيع': part.quantity += quantity_change_estimate
#     # #                 part.quantity = max(0, round(part.quantity))
#     # #             else: flash('لم يتم تعديل كمية الجزء تلقائياً لأن سعر البيع الحالي للجزء غير صالح.', 'warning')
#     # #         except Exception as qty_e: app.logger.error(f"Error adjusting quantity for part {part.id} while deleting tx {id}: {qty_e}", exc_info=True); flash('حدث خطأ أثناء محاولة تعديل كمية الجزء.', 'error')
#     # #     try:
#     # #         db.session.delete(transaction)
#     # #         db.session.commit()
#     # #         flash('تم حذف المعاملة بنجاح.', 'success')
#     # #     except Exception as e:
#     # #         db.session.rollback()
#     # #         app.logger.error(f"Error deleting transaction {id}: {e}", exc_info=True)
#     # #         flash(f'حدث خطأ أثناء حذف المعاملة.', 'error')
#     # #     return redirect(url_for('list_transactions'))
#     # #
#     # # # --- Customer Routes ---
#     # # @app.route('/customers')
#     # # def list_customers():
#     # #     """Displays a list of all customers."""
#     # #     customers = Customer.query.order_by(Customer.name).all()
#     # #     return render_template('customers.html', customers=customers)
#     # #
#     # # @app.route('/customers/add', methods=['GET', 'POST'])
#     # # def add_customer():
#     # #     """Adds a new customer to the database."""
#     # #     if request.method == 'POST':
#     # #         name = request.form.get('name', '').strip()
#     # #         if not name: flash('اسم العميل مطلوب.', 'error')
#     # #         else:
#     # #             existing = Customer.query.filter(Customer.name.ilike(name)).first()
#     # #             if existing: flash(f'العميل "{name}" موجود بالفعل.', 'warning')
#     # #             else:
#     # #                 try:
#     # #                     new_customer = Customer(name=name)
#     # #                     db.session.add(new_customer)
#     # #                     db.session.commit()
#     # #                     flash(f'تمت إضافة العميل "{name}" بنجاح.', 'success')
#     # #                     return redirect(url_for('list_customers'))
#     # #                 except Exception as e:
#     # #                     db.session.rollback()
#     # #                     app.logger.error(f"Error adding customer '{name}': {e}", exc_info=True)
#     # #                     flash(f'حدث خطأ أثناء إضافة العميل.', 'error')
#     # #     return render_template('add_customer.html')
#     # #
#     # # @app.route('/customers/edit/<int:id>', methods=['GET', 'POST'])
#     # # def edit_customer(id):
#     # #     """Edits an existing customer's details."""
#     # #     # Use db.session.get() instead of Customer.query.get_or_404()
#     # #     customer = db.session.get(Customer, id)
#     # #     if not customer:
#     # #          app.logger.warning(f"Edit attempt for non-existent customer ID: {id}")
#     # #          abort(404)
#     # #
#     # #     if request.method == 'POST':
#     # #         new_name = request.form.get('name', '').strip()
#     # #         if not new_name: flash('اسم العميل مطلوب.', 'error')
#     # #         else:
#     # #             existing = Customer.query.filter(Customer.name.ilike(new_name), Customer.id != id).first()
#     # #             if existing: flash(f'اسم العميل "{new_name}" مستخدم بالفعل لعميل آخر.', 'error')
#     # #             else:
#     # #                 try:
#     # #                     customer.name = new_name
#     # #                     db.session.commit()
#     # #                     flash(f'تم تحديث بيانات العميل "{customer.name}" بنجاح.', 'success')
#     # #                     return redirect(url_for('list_customers'))
#     # #                 except Exception as e:
#     # #                     db.session.rollback()
#     # #                     app.logger.error(f"Error editing customer {id}: {e}", exc_info=True)
#     # #                     flash(f'حدث خطأ أثناء تعديل العميل.', 'error')
#     # #     return render_template('edit_customer.html', customer=customer)
#     # #
#     # # @app.route('/customers/delete/<int:id>', methods=['POST'])
#     # # def delete_customer(id):
#     # #      """Deletes a customer if they have no associated sales."""
#     # #      # Use db.session.get() and check existence
#     # #      customer = db.session.get(Customer, id)
#     # #      if not customer:
#     # #          app.logger.warning(f"Delete attempt for non-existent customer ID: {id}")
#     # #          flash('العميل غير موجود.', 'error')
#     # #          return redirect(url_for('list_customers'))
#     # #
#     # #      # Use the relationship to check for sales efficiently
#     # #      if customer.sales.first(): # Check if any sale exists
#     # #         flash(f'لا يمكن حذف العميل "{customer.name}" لأنه مرتبط بمعاملات بيع.', 'error')
#     # #      else:
#     # #         try:
#     # #             customer_name = customer.name
#     # #             db.session.delete(customer)
#     # #             db.session.commit()
#     # #             flash(f'تم حذف العميل "{customer_name}" بنجاح.', 'success')
#     # #         except Exception as e:
#     # #             db.session.rollback()
#     # #             app.logger.error(f"Error deleting customer {id}: {e}", exc_info=True)
#     # #             flash(f'حدث خطأ أثناء حذف العميل.', 'error')
#     # #      return redirect(url_for('list_customers'))
#     # #
#     # # @app.route('/customers/<int:id>/sales')
#     # # def customer_sales_report(id):
#     # #     """Displays a historical sales report for a specific customer."""
#     # #     # Use db.session.get() instead of Customer.query.get_or_404()
#     # #     customer = db.session.get(Customer, id)
#     # #     if not customer:
#     # #         app.logger.warning(f"Sales report attempt for non-existent customer ID: {id}")
#     # #         abort(404)
#     # #
#     # #     sales_list = Transaction.query.options(db.joinedload(Transaction.part))\
#     # #                                   .filter_by(customer_id=id, transaction_type='بيع')\
#     # #                                   .order_by(Transaction.date.desc())\
#     # #                                   .all()
#     # #     grand_total = sum(sale.amount for sale in sales_list)
#     # #     return render_template('customer_sales.html', customer=customer, sales_list=sales_list, grand_total=grand_total)
#     # #
#     # # # --- Temporary List/Invoice Preparation Routes ---
#     # #
#     # # @app.route('/list/prepare/<int:customer_id>', methods=['GET', 'POST'])
#     # # def prepare_customer_list(customer_id):
#     # #     """Page to build a temporary list of parts for a customer using session."""
#     # #     # Use db.session.get() instead of Customer.query.get_or_404()
#     # #     customer = db.session.get(Customer, customer_id)
#     # #     if not customer:
#     # #         app.logger.warning(f"Prepare list attempt for non-existent customer ID: {customer_id}")
#     # #         flash(f'العميل بالمعرف {customer_id} غير موجود.', 'error')
#     # #         return redirect(url_for('list_customers'))
#     # #
#     # #     session_key = f'current_list_{customer_id}'
#     # #
#     # #     if request.method == 'POST':
#     # #         try:
#     # #             part_id = int(request.form.get('part_id'))
#     # #             quantity = int(request.form.get('quantity', 1))
#     # #             # Use db.session.get()
#     # #             part = db.session.get(Part, part_id)
#     # #
#     # #             if not part: flash('الجزء المختار غير موجود.', 'error')
#     # #             elif quantity <= 0: flash('الكمية يجب أن تكون أكبر من صفر.', 'error')
#     # #             elif quantity > part.quantity: flash(f'الكمية المطلوبة ({quantity}) غير متوفرة للجزء "{part.name}". المتوفر: {part.quantity}', 'error')
#     # #             else:
#     # #                 current_list = session.get(session_key, [])
#     # #                 found = False
#     # #                 for item in current_list:
#     # #                     if item['part_id'] == part_id:
#     # #                         if item['qty'] + quantity > part.quantity:
#     # #                             flash(f'لا يمكن إضافة {quantity} من "{part.name}". الإجمالي المطلوب ({item["qty"] + quantity}) يتجاوز الكمية المتوفرة حالياً ({part.quantity}).', 'error')
#     # #                         else:
#     # #                             item['qty'] += quantity
#     # #                             item['total'] = round(item['qty'] * item['price'], 2)
#     # #                             flash(f'تم تحديث كمية "{part.name}" في القائمة.', 'success')
#     # #                         found = True
#     # #                         break
#     # #                 if not found:
#     # #                     item_total = round(quantity * part.selling_price, 2)
#     # #                     current_list.append({
#     # #                         'part_id': part.id, 'name': part.name, 'part_number': part.part_number,
#     # #                         'qty': quantity, 'price': part.selling_price, 'total': item_total
#     # #                     })
#     # #                     flash(f'تمت إضافة {quantity} من "{part.name}" إلى القائمة.', 'success')
#     # #
#     # #                 if not found or (found and item['qty'] <= part.quantity):
#     # #                      session[session_key] = current_list
#     # #                      session.modified = True
#     # #                 return redirect(url_for('prepare_customer_list', customer_id=customer_id))
#     # #         except ValueError: flash('الرجاء إدخال كمية صحيحة.', 'error')
#     # #         except Exception as e:
#     # #              flash(f'حدث خطأ أثناء إضافة الجزء: {e}', 'error')
#     # #              app.logger.error(f"Error adding item to list for customer {customer_id}: {e}", exc_info=True)
#     # #
#     # #     # --- GET Request Logic ---
#     # #     if session_key not in session: session[session_key] = []
#     # #     parts_available = Part.query.filter(Part.quantity > 0).order_by(Part.name).all()
#     # #     current_list_items = session.get(session_key, [])
#     # #     grand_total = sum(item['total'] for item in current_list_items)
#     # #     # Use timezone aware datetime object
#     # #     current_time_utc = datetime.now(timezone.utc)
#     # #     return render_template('prepare_list.html',
#     # #                            customer=customer, parts=parts_available, current_list=current_list_items,
#     # #                            grand_total=grand_total, session_key=session_key,
#     # #                            current_time=current_time_utc)
#     # #
#     # #
#     # # @app.route('/list/clear/<int:customer_id>', methods=['POST'])
#     # # def clear_customer_list(customer_id):
#     # #     """Clears the temporary list for a customer from the session."""
#     # #     session_key = f'current_list_{customer_id}'
#     # #     session.pop(session_key, None)
#     # #     session.modified = True
#     # #     flash('تم مسح القائمة الحالية.', 'success')
#     # #     return redirect(url_for('prepare_customer_list', customer_id=customer_id))
#     # #
#     # #
#     # # @app.route('/list/finalize/<int:customer_id>', methods=['POST'])
#     # # def finalize_customer_list(customer_id):
#     # #     """Finalizes the sale: Creates transactions and clears the temporary list."""
#     # #     # Use db.session.get()
#     # #     customer = db.session.get(Customer, customer_id)
#     # #     if not customer:
#     # #         flash(f'العميل بالمعرف {customer_id} غير موجود.', 'error')
#     # #         return redirect(url_for('list_customers'))
#     # #
#     # #     session_key = f'current_list_{customer_id}'
#     # #     current_list_items = session.get(session_key, [])
#     # #     if not current_list_items: flash('القائمة فارغة، لا يوجد شيء لإتمامه.', 'warning'); return redirect(url_for('prepare_customer_list', customer_id=customer_id))
#     # #
#     # #     try:
#     # #         with db.session.no_autoflush:
#     # #             parts_to_update = {}
#     # #             for item in current_list_items:
#     # #                 # Use db.session.get()
#     # #                 part = db.session.get(Part, item['part_id'])
#     # #                 if not part: flash(f'الجزء "{item["name"]}" لم يعد موجوداً. تم إلغاء العملية.', 'error'); return redirect(url_for('prepare_customer_list', customer_id=customer_id))
#     # #                 if item['qty'] > part.quantity: flash(f'الكمية المطلوبة ({item["qty"]}) غير متوفرة الآن للجزء "{item["name"]}" (المتوفر: {part.quantity}). تم إلغاء العملية.', 'error'); return redirect(url_for('prepare_customer_list', customer_id=customer_id))
#     # #                 parts_to_update[part.id] = part
#     # #
#     # #         total_sale_amount = 0
#     # #         transactions_to_add = []
#     # #         for item in current_list_items:
#     # #             part = parts_to_update[item['part_id']]
#     # #             part.quantity -= item['qty']
#     # #             transaction = Transaction( transaction_type='بيع', amount=item['total'], part_id=item['part_id'], customer_id=customer_id )
#     # #             transactions_to_add.append(transaction)
#     # #             total_sale_amount += item['total']
#     # #
#     # #         db.session.add_all(transactions_to_add)
#     # #         db.session.commit()
#     # #         session.pop(session_key, None)
#     # #         session.modified = True
#     # #         # Correct f-string format for flash message
#     # #         flash(f'تم إتمام عملية البيع بنجاح للعميل "{customer.name}" بمبلغ إجمالي {total_sale_amount:.2f}.', 'success')
#     # #         return redirect(url_for('list_customers'))
#     # #
#     # #     except Exception as e:
#     # #         db.session.rollback()
#     # #         app.logger.error(f"Error finalizing list for customer {customer_id}: {e}", exc_info=True)
#     # #         flash('حدث خطأ أثناء إتمام عملية البيع.', 'error')
#     # #         return redirect(url_for('prepare_customer_list', customer_id=customer_id))
#     # #
#     # #
#     # # # --- Reporting Routes ---
#     # # @app.route('/reports/sales_by_type')
#     # # def sales_by_type():
#     # #     """Displays a report summing sales amount by part name."""
#     # #     sales_data = []
#     # #     try:
#     # #         sales_data = db.session.query( Part.name, db.func.sum(Transaction.amount).label('total_sales') )\
#     # #             .select_from(Transaction).join(Part, Part.id == Transaction.part_id)\
#     # #             .filter(Transaction.transaction_type == 'بيع')\
#     # #             .group_by(Part.name)\
#     # #             .order_by(db.desc('total_sales'))\
#     # #             .all()
#     # #     except Exception as e: app.logger.error(f"Error generating sales by type report: {e}", exc_info=True); flash("حدث خطأ أثناء إنشاء تقرير المبيعات حسب النوع.", "error")
#     # #     return render_template('sales_by_type.html', sales_data=sales_data)
#     # #
#     # #
#     # # @app.route('/reports/sales_by_date')
#     # # def sales_by_date():
#     # #     """Displays a report summing sales amount by date."""
#     # #     processed_sales_data = []
#     # #     try:
#     # #         sales_query_result = db.session.query( db.func.date(Transaction.date).label('sale_date_str'), db.func.sum(Transaction.amount).label('daily_total') )\
#     # #             .filter(Transaction.transaction_type == 'بيع')\
#     # #             .group_by(db.func.date(Transaction.date))\
#     # #             .order_by(db.desc(db.func.date(Transaction.date)))\
#     # #             .all()
#     # #         for row in sales_query_result:
#     # #             sale_date_obj = None
#     # #             daily_total = row.daily_total
#     # #             if row.sale_date_str:
#     # #                 try: sale_date_obj = datetime.strptime(row.sale_date_str, '%Y-%m-%d').date()
#     # #                 except ValueError: app.logger.warning(f"Could not parse date string in sales_by_date report: {row.sale_date_str}")
#     # #             processed_sales_data.append({ 'sale_date': sale_date_obj, 'daily_total': daily_total })
#     # #     except Exception as e: app.logger.error(f"Error generating sales by date report: {e}", exc_info=True); flash("حدث خطأ أثناء إنشاء تقرير المبيعات حسب التاريخ.", "error")
#     # #     return render_template('sales_by_date.html', sales_data=processed_sales_data)
#     # #
#     # #
#     # # # --- Main Execution ---
#     # # if __name__ == '__main__':
#     # #     with app.app_context():
#     # #         try:
#     # #             app.logger.info("Checking/Creating database tables...")
#     # #             db.create_all()
#     # #             app.logger.info("Database tables checked/created (Note: create_all won't alter existing tables).")
#     # #             if not Customer.query.first():
#     # #                 app.logger.info("No customers found, creating default 'بيع نقدي' customer...")
#     # #                 try:
#     # #                     cash_customer = Customer(name="بيع نقدي")
#     # #                     db.session.add(cash_customer)
#     # #                     db.session.commit()
#     # #                     app.logger.info("Default 'بيع نقدي' customer created.")
#     # #                 except Exception as e_cust:
#     # #                     db.session.rollback()
#     # #                     app.logger.error(f"Error creating default customer: {e_cust}", exc_info=True)
#     # #         except Exception as e_db:
#     # #             app.logger.error(f"Error during database initialization: {e_db}", exc_info=True)
#     # #
#     # #     app.logger.info("Starting Flask application...")
#     # #     app.run(debug=True, host='0.0.0.0', port=5000) # Use debug=False in production