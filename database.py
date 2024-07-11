#-------------------------------------------------------------------------------
# Darie-Dragos Mitoiu
# Database v1.0.0 15/02/2019
# A database module designed for a tailoring and alterations business
#-------------------------------------------------------------------------------


# Importing libraries
import pyodbc


class Database:
    """This class will allow the creation of a microsoft access database object
    with the objective to send and pull data from the database."""

    def __init__(self, database, user, password):
        self.database = database
        self.user = user
        self.password = password
        # Declaring the microsoft access driver
        self.driver = "DRIVER={Microsoft Access Driver " \
                      "(*.mdb, *.accdb)};DBQ=%s;UID=%s;PWD=%s" % \
                      (self.database, self.user, self.password)
        # Creating the database connection
        self.connection = pyodbc.connect(self.driver)
        # Creating database cursor
        self.cursor = self.connection.cursor()
        # Creating database tables
        self.create_users_table()
        self.create_customers_table()
        self.create_tailors_table()
        self.create_projects_table()
        self.create_alterations_table()

    def create_users_table(self):
        """This method will allow the creation of the users table."""

        try:
            # Execute the sql
            self.cursor.execute("""create table users(
                                   id autoincrement primary key,
                                   username varchar(100),
                                   password varchar(100),
                                   permission_level integer,
                                   email varchar(100));""")

            # Commit the sql
            self.connection.commit()
        except:
            message = "An error occurred while creating users table..."
            return message

    def create_customers_table(self):
        """This method will allow the creation of the customers table."""

        try:
            # Execute the sql
            self.cursor.execute("""create table customers(
                                   id autoincrement primary key,
                                   first_name varchar(100),
                                   last_name varchar(100),
                                   address varchar(100),
                                   postcode varchar(100),
                                   phone varchar(50),
                                   email varchar(100),
                                   neck varchar(20),
                                   chest varchar(20),
                                   shoulders varchar(20),
                                   sleeve varchar(20),
                                   biceps varchar(20),
                                   wrist varchar(20),
                                   waist varchar(20),
                                   hips varchar(20),
                                   shirt_length varchar(20),
                                   trouser_waist varchar(20),
                                   trouser_outseam varchar(20),
                                   trouser_inseam varchar(20),
                                   crotch varchar(20),
                                   thigh varchar(20),
                                   knee varchar(20));""")
            # Commit the sql
            self.connection.commit()
        except:
            message = "An error occurred while creating customers table..."
            return message

    def create_tailors_table(self):
        """This method will allow the creation of the tailors table."""

        try:
            # Execute the sql
            self.cursor.execute("""create table tailors(
                                   id autoincrement primary key,
                                   first_name varchar(100),
                                   last_name varchar(100),
                                   address varchar(100),
                                   postcode varchar(100),
                                   phone varchar(50),
                                   email varchar(100));""")
            # Commit the sql
            self.connection.commit()
        except:
            message = "An error occurred while creating tailors table..."
            return message

    def create_projects_table(self):
        """This method will allow the creation of the projects table."""

        try:
            # Execute the sql
            self.cursor.execute("""create table projects(
                                   id autoincrement primary key,
                                   name varchar(100),
                                   product varchar(100),
                                   material varchar(100),
                                   colour varchar(100),
                                   start_date date,
                                   delivery_date date,
                                   price varchar(50),
                                   customer_id int,
                                   tailor_id int,
                                   foreign key (customer_id)
                                   references customers(id),
                                   foreign key (tailor_id)
                                   references tailors(id));""")
            # Commit the sql
            self.connection.commit()
        except:
            message = "An error occurred while creating projects table..."
            return message

    def create_alterations_table(self):
        """This method will allow the creation of the alterations table."""

        try:
            # Execute the sql
            self.cursor.execute("""create table alterations(
                                   id autoincrement primary key,
                                   name varchar(100),
                                   product varchar(100),
                                   material varchar(100),
                                   colour varchar(100),
                                   start_date date,
                                   delivery_date date,
                                   price varchar(50),
                                   customer_id int,
                                   tailor_id int,
                                   foreign key (customer_id)
                                   references customers(id),
                                   foreign key (tailor_id)
                                   references tailors(id));""")
            # Commit the sql
            self.connection.commit()
        except:
            message = "An error occurred while creating alterations table..."
            return message

    def add_user(self, username, password, permission_level, email):
        """This method will allow the insertion of a new user to database."""

        try:
            # Execute the sql
            self.cursor.execute("""insert into users(username, password,
                                permission_level, email) values(?, ?, ?, ?);""",
                                (username, password, permission_level, email))
            # Commit the sql
            self.connection.commit()
        except:
            message = "An error occurred while adding an user..."
            return message

    def view_customers(self):
        """This method will return the content of the customers table."""

        # Execute the sql
        self.cursor.execute("""select * from customers;""")
        # Hold all the data from database returned after the sql and return it
        data = self.cursor.fetchall()
        return data

    def view_tailors(self):
        """This method will return the content of the tailors table."""

        # Execute the sql
        self.cursor.execute("""select * from tailors;""")
        # Hold all the data from database returned after the sql and return it
        data = self.cursor.fetchall()
        return data

    def view_projects(self):
        """This method will return the content of the projects table."""

        # Execute the sql
        self.cursor.execute("""select * from projects;""")
        # Hold all the data from database returned after the sql and return it
        data = self.cursor.fetchall()
        return data

    def view_alterations(self):
        """This method will return the content of the alterations table."""

        # Execute the sql
        self.cursor.execute("""select * from alterations;""")
        # Hold all the data from database returned after the sql and return it
        data = self.cursor.fetchall()
        return data

    def view_users(self):
        """This method will return the content of the users table."""

        # Execute the sql
        self.cursor.execute("""select * from users;""")
        # Hold all the data from database returned after the sql and return it
        data = self.cursor.fetchall()
        return data

    def add_customer(self, first_name, last_name, address,
                     postcode, phone, email, neck, chest,
                     shoulders, sleeve, biceps, wrist,
                     waist, hips, shirt_length, trouser_waist,
                     trouser_outseam, trouser_inseam, crotch,
                     thigh, knee):
        """This method will allow the insertion of a new customer."""

        try:
            # Execute the sql
            self.cursor.execute("""insert into customers(first_name, last_name,
                                address, postcode, phone, email, neck, chest,
                                shoulders, sleeve, biceps, wrist, waist, hips,
                                shirt_length, trouser_waist, trouser_outseam,
                                trouser_inseam, crotch, thigh, knee)
                                values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                                ?, ?, ?, ?, ?, ?, ?, ?);""",
                                (first_name, last_name, address, postcode,
                                 phone, email, neck, chest, shoulders, sleeve,
                                 biceps, wrist, waist, hips, shirt_length,
                                 trouser_waist, trouser_outseam, trouser_inseam,
                                 crotch, thigh, knee))
            # Commit the sql
            self.connection.commit()
        except:
            message = "An error occurred while adding a customer..."
            return message

    def update_customer(self, first_name, last_name, address,
                     postcode, phone, email, neck, chest,
                     shoulders, sleeve, biceps, wrist,
                     waist, hips, shirt_length, trouser_waist,
                     trouser_outseam, trouser_inseam, crotch,
                     thigh, knee, customer_id):

        """This method will allow the data actualization for a customer."""
        try:
            # Execute the sql
            self.cursor.execute("""update customers set first_name = ?,
                                last_name = ?, address = ?, postcode = ?,
                                phone = ?, email = ?, neck = ?, chest = ?,
                                shoulders = ?, sleeve = ?, biceps = ?,
                                wrist = ?, waist = ?, hips = ?,
                                shirt_length = ?, trouser_waist = ?,
                                trouser_outseam = ?, trouser_inseam = ?,
                                crotch = ?, thigh = ?, knee = ?
                                where ID = ?;""",
                                (first_name, last_name, address, postcode,
                                 phone, email, neck, chest, shoulders, sleeve,
                                 biceps, wrist, waist, hips, shirt_length,
                                 trouser_waist, trouser_outseam, trouser_inseam,
                                 crotch, thigh, knee, customer_id))
            # Commit the sql
            self.connection.commit()
        except:
            message = "An error occurred while updating a customer..."
            return message

    def update_tailor(self, first_name, last_name, address,
                     postcode, phone, email, tailor_id):
        """This method will allow the data actualization for a tailor."""

        try:
            # Execute the sql
            self.cursor.execute("""update tailors set first_name = ?,
                                last_name = ?, address = ?, postcode = ?,
                                phone = ?, email = ? where ID = ?;""",
                                (first_name, last_name, address, postcode,
                                 phone, email, tailor_id))
            # Commit the sql
            self.connection.commit()
        except:
            message = "An error occurred while updating a tailor..."
            return message

    def update_project(self, name, product, material,
                       colour, start_date, delivery_date,
                       price, customer_id, tailor_id,
                       project_id):
        """This method will allow the data actualization for a project."""

        try:
            # Execute the sql
            self.cursor.execute("""update projects set name = ?,
                                product = ?, material = ?, colour = ?,
                                start_date = ?, delivery_date = ?,
                                price = ?, customer_id = ?, tailor_id = ?
                                where ID = ?;""",
                                (name, product, material, colour,
                                 start_date, delivery_date, price,
                                 customer_id, tailor_id, project_id))
            # Commit the sql
            self.connection.commit()
        except:
            message = "An error occurred while updating a project..."
            return message

    def update_alteration(self, name, product, material,
                          colour, start_date, delivery_date,
                          price, customer_id, tailor_id,
                          project_id):
        """This method will allow the data actualization for an alteration."""

        try:
            # Execute the sql
            self.cursor.execute("""update alterations set name = ?,
                                product = ?, material = ?, colour = ?,
                                start_date = ?, delivery_date = ?,
                                price = ?, customer_id = ?, tailor_id = ?
                                where ID = ?;""",
                                (name, product, material, colour,
                                 start_date, delivery_date, price,
                                 customer_id, tailor_id, project_id))
            # Commit the sql
            self.connection.commit()
        except:
            message = "An error occurred while updating an alteration..."
            return message

    def update_user(self, username, password, permission_level, email, user_id):
        """This method will allow the data actualization for an user."""

        try:
            # Execute the sql
            self.cursor.execute("""update users set username = ?,
                                password = ?, permission_level = ?, email = ?
                                where ID = ?;""",
                                (username, password, permission_level, email,
                                 user_id))
            # Commit the sql
            self.connection.commit()
        except:
            message = "An error occurred while updating an user..."
            return message

    def get_customer(self, customer_id):
        """This method will allow the data retrieving for a customer."""

        # Execute the sql
        self.cursor.execute("select * from customers where ID = ?",
                            (customer_id,))
        # Hold the data returned after the execution of the sql and return it
        data = self.cursor.fetchall()
        return data

    def get_tailor(self, tailor_id):
        """This method will allow the data retrieving for a tailor."""

        # Execute the sql
        self.cursor.execute("select * from tailors where ID = ?",
                            (tailor_id,))
        # Hold the data returned after the execution of the sql and return it
        data = self.cursor.fetchall()
        return data

    def get_project(self, project_id):
        """This method will allow the data retrieving for a project."""

        # Execute the sql
        self.cursor.execute("select * from projects where ID = ?",
                            (project_id,))
        # Hold the data returned after the execution of the sql and return it
        data = self.cursor.fetchall()
        return data

    def get_all_projects(self):
        """This method will allow the data retrieving for all projects."""

        # Execute the sql
        self.cursor.execute("select * from projects;")
        # Hold the data returned after the execution of the sql and return it
        data = self.cursor.fetchall()
        return data

    def get_all_alterations(self):
        """This method will allow the data retrieving for all alterations."""

        # Execute the sql
        self.cursor.execute("select * from alterations;")
        # Hold the data returned after the execution of the sql and return it
        data = self.cursor.fetchall()
        return data

    def get_alteration(self, alteration_id):
        """This method will allow the data retrieving for an alterations."""

        # Execute the sql
        self.cursor.execute("select * from alterations where ID = ?",
                            (alteration_id,))
        # Hold the data returned after the execution of the sql and return it
        data = self.cursor.fetchall()
        return data

    def get_projects_alterations(self, project_id, project_name,
                                 alteration_id, alteration_name):
        """This method will allow the data retrieving for both projects and
        alterations tables."""

        # Execute the sql
        self.cursor.execute("""select * from projects
                            where ID = ? and name = ?
                            UNION ALL
                            select * from alterations
                            where ID = ? and name = ?;""",
                            (project_id, project_name,
                            alteration_id, alteration_name))
        # Hold the data returned after the execution of the sql and return it
        data = self.cursor.fetchall()
        return data

    def get_user_id(self, user_id):
        """This method will allow the data retrieving for a user."""

        # Execute the sql
        self.cursor.execute("select * from users where ID = ?",
                            (user_id,))
        # Hold the data returned after the execution of the sql and return it
        data = self.cursor.fetchall()
        return data

    def get_project_customer(self, customer_id):
        """This method will allow the data retrieving for a project."""

        # Execute the sql
        self.cursor.execute("select * from projects where customer_id = ?",
                            (customer_id,))
        # Hold the data returned after the execution of the sql and return it
        data = self.cursor.fetchall()
        return data

    def get_alteration_customer(self, customer_id):
        """This method will allow the data retrieving for an alteration."""

        # Execute the sql
        self.cursor.execute("select * from alterations where customer_id = ?",
                            (customer_id,))
        # Hold the data returned after the execution of the sql and return it
        data = self.cursor.fetchall()
        return data

    def delete_customer(self, customer_id):
        """This method will allow the deletion of a customer in database."""

        try:
            # Execute the sql
            self.cursor.execute("""delete from customers where ID = ?;""",
                                (customer_id,))
            # Commit the sql
            self.connection.commit()
        except:
            message = "An error occurred while deleting a customer..."
            return message

    def delete_tailor(self, tailor_id):
        """This method will allow the deletion of a tailor in database."""

        try:
            # Execute the sql
            self.cursor.execute("""delete from tailors where ID = ?;""",
                                (tailor_id,))
            # Commit the sql
            self.connection.commit()
        except:
            message = "An error occurred while deleting a tailor..."
            return message

    def delete_project(self, project_id):
        """This method will allow the deletion of a project in database."""

        try:
            # Execute the sql
            self.cursor.execute("""delete from projects where ID = ?;""",
                                (project_id,))
            # Commit the sql
            self.connection.commit()
        except:
            message = "An error occurred while deleting a project..."
            return message

    def delete_alteration(self, alteration_id):
        """This method will allow the deletion of an alteration in database."""

        try:
            # Execute the sql
            self.cursor.execute("""delete from alterations where ID = ?;""",
                                (alteration_id,))
            # Commit the sql
            self.connection.commit()
        except:
            message = "An error occurred while deleting an alteration..."
            return message

    def delete_user(self, user_id):
        """This method will allow the deletion of an user in database."""

        try:
            # Execute the sql
            self.cursor.execute("""delete from users where ID = ?;""",
                                (user_id,))
            # Commit the sql
            self.connection.commit()
        except:
            message = "An error occurred while deleting an user..."
            return message

    def search_customer_first_name(self, first_name):
        """This method will allow the retrieving of data for a customer."""

        # Execute the sql
        self.cursor.execute("select * from customers where first_name like ?",
                            (first_name,))
        # Hold the data returned after the execution of the sql and return it
        data = self.cursor.fetchall()
        return data

    def search_customer_last_name(self, last_name):
        """This method will allow the retrieving of data for a customer."""

        # Execute the sql
        self.cursor.execute("select * from customers where last_name like ?",
                            (last_name,))
        # Hold the data returned after the execution of the sql and return it
        data = self.cursor.fetchall()
        return data

    def search_customer_address(self, address):
        """This method will allow the retrieving of data for a customer."""

        # Execute the sql
        self.cursor.execute("select * from customers where address like ?",
                            (address,))
        # Hold the data returned after the execution of the sql and return it
        data = self.cursor.fetchall()
        return data

    def search_customer_postcode(self, postcode):
        """This method will allow the retrieving of data for a customer."""

        # Execute the sql
        self.cursor.execute("select * from customers where postcode like ?",
                            (postcode,))
        # Hold the data returned after the execution of the sql and return it
        data = self.cursor.fetchall()
        return data

    def search_customer_phone(self, phone):
        """This method will allow the retrieving of data for a customer."""

        # Execute the sql
        self.cursor.execute("select * from customers where phone like ?",
                            (phone,))
        # Hold the data returned after the execution of the sql and return it
        data = self.cursor.fetchall()
        return data

    def search_customer_email(self, email):
        """This method will allow the retrieving of data for a customer."""

        # Execute the sql
        self.cursor.execute("select * from customers where email like ?",
                            (email,))
        # Hold the data returned after the execution of the sql and return it
        data = self.cursor.fetchall()
        return data

    def add_tailor(self, first_name, last_name, address,
                   postcode, phone, email):
        """This method will allow the insertion of a new tailor to database."""

        try:
            # Execute the sql
            self.cursor.execute("""insert into tailors(first_name, last_name,
                                address, postcode, phone, email)
                                values(?, ?, ?, ?, ?, ?);""",
                                (first_name, last_name, address, postcode,
                                 phone, email))
            # Commit the sql
            self.connection.commit()
        except:
            message = "An error occurred while adding a tailor..."
            return message

    def add_project(self, name, product, material, colour,
                    date, delivery_date, price, customer_id, tailor_id):
        """This method will allow the insertion of a new project to database."""

        try:
            # Execute the sql
            self.cursor.execute("""insert into projects(name, product,
                                material, colour, start_date, delivery_date,
                                price, customer_id, tailor_id)
                                values(?, ?, ?, ?, ?, ?, ?, ?, ?);""",
                                (name, product, material, colour,
                                 date, delivery_date, price,
                                 customer_id, tailor_id))
            # Commit the sql
            self.connection.commit()
        except:
            message = "An error occurred while adding a project..."
            return message

    def add_alteration(self, name, product, material, colour,
                       date, delivery_date, price, customer_id, tailor_id):
        """This method will allow the insertion of an alteration to database."""

        try:
            # Execute the sql
            self.cursor.execute("""insert into alterations(name, product,
                                material, colour, start_date, delivery_date,
                                price, customer_id, tailor_id)
                                values(?, ?, ?, ?, ?, ?, ?, ?, ?);""",
                                (name, product, material, colour,
                                 date, delivery_date, price,
                                 customer_id, tailor_id))
            # Commit the sql
            self.connection.commit()
        except:
            message = "An error occurred while adding an alteration..."
            return message

    def search_tailor_first_name(self, first_name):
        """This method will allow the data retrieving for a tailor."""

        # Execute the sql
        self.cursor.execute("select * from tailors where first_name like ?",
                            (first_name,))
        # Hold the data returned after the execution of the sql and return it
        data = self.cursor.fetchall()
        return data

    def search_tailor_last_name(self, last_name):
        """This method will allow the data retrieving for a tailor."""

        # Execute the sql
        self.cursor.execute("select * from tailors where last_name like ?",
                            (last_name,))
        # Hold the data returned after the execution of the sql and return it
        data = self.cursor.fetchall()
        return data

    def search_tailor_address(self, address):
        """This method will allow the data retrieving for a tailor."""

        # Execute the sql
        self.cursor.execute("select * from tailors where address like ?",
                            (address,))
        # Hold the data returned after the execution of the sql and return it
        data = self.cursor.fetchall()
        return data

    def search_tailor_postcode(self, postcode):
        """This method will allow the data retrieving for a tailor."""

        # Execute the sql
        self.cursor.execute("select * from tailors where postcode like ?",
                            (postcode,))
        # Hold the data returned after the execution of the sql and return it
        data = self.cursor.fetchall()
        return data

    def search_tailor_phone(self, phone):
        """This method will allow the data retrieving for a tailor."""

        # Execute the sql
        self.cursor.execute("select * from tailors where phone like ?",
                            (phone,))
        # Hold the data returned after the execution of the sql and return it
        data = self.cursor.fetchall()
        return data

    def search_tailor_email(self, email):
        """This method will allow the data retrieving for a tailor."""

        # Execute the sql
        self.cursor.execute("select * from tailors where email like ?",
                            (email,))
        # Hold the data returned after the execution of the sql and return it
        data = self.cursor.fetchall()
        return data

    def search_project_name(self, name):
        """This method will allow the data retrieving for a project."""

        # Execute the sql
        self.cursor.execute("select * from projects where name like ?",
                            (name,))
        # Hold the data returned after the execution of the sql and return it
        data = self.cursor.fetchall()
        return data

    def search_project_product(self, product):
        """This method will allow the data retrieving for a project."""

        # Execute the sql
        self.cursor.execute("select * from projects where product like ?",
                            (product,))
        # Hold the data returned after the execution of the sql and return it
        data = self.cursor.fetchall()
        return data

    def search_project_material(self, material):
        """This method will allow the data retrieving for a project."""

        # Execute the sql
        self.cursor.execute("select * from projects where material like ?",
                            (material,))
        # Hold the data returned after the execution of the sql and return it
        data = self.cursor.fetchall()
        return data

    def search_project_colour(self, colour):
        """This method will allow the data retrieving for a project."""

        # Execute the sql
        self.cursor.execute("select * from projects where colour like ?",
                            (colour,))
        # Hold the data returned after the execution of the sql and return it
        data = self.cursor.fetchall()
        return data

    def search_project_start_date(self, start_date):
        """This method will allow the data retrieving for a project."""

        # Execute the sql
        self.cursor.execute("select * from projects where start_date like ?",
                            (start_date,))
        # Hold the data returned after the execution of the sql and return it
        data = self.cursor.fetchall()
        return data

    def search_project_delivery(self, delivery):
        """This method will allow the data retrieving for a project."""

        # Execute the sql
        self.cursor.execute("select * from projects where delivery_date like ?",
                            (delivery,))
        # Hold the data returned after the execution of the sql and return it
        data = self.cursor.fetchall()
        return data

    def search_project_price(self, price):
        """This method will allow the data retrieving for a project."""

        # Execute the sql
        self.cursor.execute("select * from projects where price like ?",
                            (price,))
        # Hold the data returned after the execution of the sql and return it
        data = self.cursor.fetchall()
        return data

    def search_alteration_name(self, name):
        """This method will allow the data retrieving for an alteration."""

        # Execute the sql
        self.cursor.execute("select * from alterations where name like ?",
                            (name,))
        # Hold the data returned after the execution of the sql and return it
        data = self.cursor.fetchall()
        return data

    def search_alteration_product(self, product):
        """This method will allow the data retrieving for an alteration."""

        # Execute the sql
        self.cursor.execute("select * from alterations where product like ?",
                            (product,))
        # Hold the data returned after the execution of the sql and return it
        data = self.cursor.fetchall()
        return data

    def search_alteration_material(self, material):
        """This method will allow the data retrieving for an alteration."""

        # Execute the sql
        self.cursor.execute("select * from alterations where material like ?",
                            (material,))
        # Hold the data returned after the execution of the sql and return it
        data = self.cursor.fetchall()
        return data

    def search_alteration_colour(self, colour):
        """This method will allow the data retrieving for an alteration."""

        # Execute the sql
        self.cursor.execute("select * from alterations where colour like ?",
                            (colour,))
        # Hold the data returned after the execution of the sql and return it
        data = self.cursor.fetchall()
        return data

    def search_alteration_start_date(self, start_date):
        """This method will allow the data retrieving for an alteration."""

        # Execute the sql
        self.cursor.execute("select * from alterations where start_date like ?",
                            (start_date,))
        # Hold the data returned after the execution of the sql and return it
        data = self.cursor.fetchall()
        return data

    def search_alteration_delivery(self, delivery):
        """This method will allow the data retrieving for an alteration."""

        # Execute the sql
        self.cursor.execute("select * from alterations where delivery_date like ?",
                            (delivery,))
        # Hold the data returned after the execution of the sql and return it
        data = self.cursor.fetchall()
        return data

    def search_alteration_price(self, price):
        """This method will allow the data retrieving for an alteration."""

        # Execute the sql
        self.cursor.execute("select * from alterations where price like ?",
                            (price,))
        # Hold the data returned after the execution of the sql and return it
        data = self.cursor.fetchall()
        return data

    def search_user_username(self, username):
        """This method will allow the data retrieving for an user."""

        # Execute the sql
        self.cursor.execute("select * from users where username like ?",
                            (username,))
        # Hold the data returned after the execution of the sql and return it
        data = self.cursor.fetchall()
        return data

    def search_user_permission(self, permission_level):
        """This method will allow the data retrieving for an user."""

        # Execute the sql
        self.cursor.execute("select * from users where permission_level like ?",
                            (permission_level,))
        # Hold the data returned after the execution of the sql and return it
        data = self.cursor.fetchall()
        return data

    def search_user_email(self, email):
        """This method will allow the data retrieving for an user."""

        # Execute the sql
        self.cursor.execute("select * from users where email like ?",
                            (email,))
        # Hold the data returned after the execution of the sql and return it
        data = self.cursor.fetchall()
        return data

    def get_customer_name(self, first_name, last_name, address):
        """This method will allow the data retrieving for a customer."""

        # Execute the sql
        self.cursor.execute("""select * from customers
                            where first_name like ? and
                            last_name like ? and
                            address like ?;""",
                            (first_name, last_name, address))
        # Hold the data returned after the execution of the sql and return it
        data = self.cursor.fetchall()
        return data

    def get_tailor_name(self, first_name, last_name, address):
        """This method will allow the data retrieving for a tailor."""

        # Execute the sql
        self.cursor.execute("""select * from tailors
                            where first_name like ? and
                            last_name like ? and
                            address like ?;""",
                            (first_name, last_name, address))
        # Hold the data returned after the execution of the sql and return it
        data = self.cursor.fetchall()
        return data

    def get_projects_profit(self, start_date, end_date):
        """This method will allow the data retrieving for a project."""

        # Execute the sql
        self.cursor.execute("""select start_date, sum(price) from projects
                            where start_date between ? and ?
                            group by start_date;""",
                            (start_date, end_date))
        # Hold the data returned after the execution of the sql and return it
        data = self.cursor.fetchall()
        return data

    def get_a_profit(self, start_date, end_date):
        """This method will allow the data retrieving for an alteration."""

        # Execute the sql
        self.cursor.execute("""select start_date, sum(price) from alterations
                            where start_date between ? and ?
                            group by start_date;""",
                            (start_date, end_date))
        # Hold the data returned after the execution of the sql and return it
        data = self.cursor.fetchall()
        return data

    def get_user(self, username):
        """This method will allow the data retrieving for an user."""

        # Execute the sql
        self.cursor.execute("select * from users where username = ?",
                            (username,))
        # Hold the data returned after the execution of the sql and return it
        data = self.cursor.fetchall()
        return data
