-- Create employee table
CREATE TABLE IF NOT EXISTS employeeTable (
    employeeid VARCHAR(255) PRIMARY KEY NOT NULL,
    employeeName VARCHAR(400),
    employeeNumber VARCHAR(30),
    DateOfChange DATE,
    OrganizationSector VARCHAR(255) CHECK (OrganizationSector IN (
        'Health care',
        'Precision manufacturing',
        'Engineering',
        'Finance/accounting',
        'Information technology'
    )),
    BranchId bigint NOT NULL,
    FOREIGN KEY(BranchId) REFERENCES goodwillbranch(BranchId)
);

-- Create login password table
CREATE TABLE IF NOT EXISTS loginpaswd (
    id VARCHAR(255) PRIMARY KEY NOT NULL,
    password VARCHAR(255) NOT NULL,
    FOREIGN KEY(id) REFERENCES employeeTable(employeeid) ON DELETE CASCADE
);