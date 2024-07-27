# Summer-2024-Database-Systems
File Descriptions

1. base.html:
* The root template file.
* Defines the basic structure of all pages, including the HTML head and body sections.
* Provides a background image for the entire application.
Contains a block body_base to be extended by other templates.
form_layout.html:
Extends base.html.
Designed for forms and user input pages.
Contains a style block to format forms, including centering text and inputs.
Provides blocks title_form and body_form to be customized by specific form pages.
table_layout.html:
Extends base.html.
Designed for pages displaying tabular data.
Contains a style block to format tables, ensuring a consistent look and feel.
Provides blocks title_table and body_table to be customized by specific table pages.
How to Use These Files

To create a new form or table page, you will extend form_layout.html or table_layout.html and customize the provided blocks.
