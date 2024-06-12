class Snowddl:
    """
    Snowddl class loads DDL files for various tables in a database.

    Attributes:
        ddl_dict (dict): dictionary of DDL files for various tables in a database.

    Methods:
        load_ddls: loads DDL files for various tables in a database.
    """

    def __init__(self):
        self.ddl_dict = self.load_ddls()

    @staticmethod
    def load_ddls():
        ddl_files = {
            "BRANCH": "sql/ddl_branch.sql",
            "BRANCH_SUPPLIER": "sql/ddl_branch_supplier.sql",
            "CLIENT": "sql/ddl_client.sql",
            "EMPLOYEE": "sql/ddl_employee.sql",
            "STUDENT": "sql/ddl_student.sql",
            "WORK_WITH": "sql/ddl_works_with.sql",
        }

        ddl_dict = {}
        for table_name, file_name in ddl_files.items():
            with open(file_name, "r") as f:
                ddl_dict[table_name] = f.read()
        return ddl_dict
