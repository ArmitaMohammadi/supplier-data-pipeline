
# Project: Supplier Data Integration & Analysis Pipeline

## Objective
Parts Avatar is looking to integrate a new auto parts supplier to expand our inventory. We have received a sample data feed (`supplier_feed.csv`) containing their product stock levels and costs, along with a separate file (`product_metadata.csv`) that maps supplier part IDs to our internal product information.

Our goal is to build a reliable, automated pipeline to process this data, load it into a database, and perform an initial analysis to determine the viability of this supplier.

## The Challenge
The supplier's data feed is notoriously unreliable. It contains inconsistencies, missing values, and mixed data types that must be handled gracefully. Your task is to design and implement a small-scale ETL (Extract, Transform, Load) pipeline that is robust enough to handle these issues and produce clean, analytics-ready data.

## Datasets
* `data/supplier_feed.csv`: The raw, messy data from the new supplier.
* `data/product_metadata.csv`: Maps the supplier's parts to our internal system.

## Data Cleaning and Transformation

* This section documents the data exploration, cleaning, and transformation steps applied to the supplier feed.  
* The initial examination was performed in a Jupyter notebook to identify issues, and the final cleaning logic was implemented in **`src/transform_data.py`** to ensure automation and reproducibility.

* ## 1. Data Exploration
    Before writing the transformation script, the dataset was analyzed to identify potential flaws such as:

    - Missing or inconsistent values in `cost_price`, `entry_date`, or `stock_level`
    - Mixed numeric formats (e.g., `$25.00` vs. `25.00`)
    - Non-uniform date formats (ISO, US, and text-based)
    - Text-based stock levels such as `"Low Stock"` or `"Unavailable"`
    - Possible duplicate rows

    Although the current version of the dataset does not include missing values or duplicates, these checks were necessary to design a robust transformation process that can handle future data inconsistencies safely.

* ## 2. Handling Missing and Duplicate Values
    - **Duplicates:**  
    Duplicate rows were removed to ensure data integrity.
    - **Missing `cost_price`:**  
    Missing price values were replaced with the average price of the same `product_id`, maintaining internal consistency across products.
    - **Missing `stock_level`:**  
    Missing stock levels were filled with `-1`, representing an unknown or unavailable stock status.
    This approach ensures the data remains complete, even if future supplier feeds contain gaps or duplicated entries.

* ## 3. Cleaning `cost_price`
    The `cost_price` column appeared in two different formats — some values contained a dollar sign (e.g., `$23.5`), while others were numeric.  
    All dollar signs were removed, and values were standardized to a consistent numeric format.  
    This ensures accurate aggregation, comparison, and downstream processing.


* ## 4. Standardizing `entry_date`
    The `entry_date` field contained several inconsistent date formats such as `2023-10-01`, `10/01/23`, and `October 1, 2023`.  
    All valid dates were converted into a single standardized datetime format.  
    Entries that could not be parsed or were missing were left as `NaT` (Not a Time).  

This guarantees that all date values follow a consistent and machine-readable structure.

* ## 5. Normalizing `stock_level`
    The `stock_level` column included mixed text and numeric representations.  
    Text-based entries were mapped to consistent numeric codes to simplify analysis and modeling.

    | Original Label           | Mapped Value | Meaning / Rationale |
    |---------------------------|--------------|----------------------|
    | `Low Stock` / `Low`       | **1**        | Limited availability but not zero. |
    | `Out of Stock`            | **0**        | Product currently unavailable. |
    | `Unavailable`             | **-1**       | Status undefined or not available for sale. |
    | Missing values            | **-1**       | Treated consistently as unavailable. |

    This mapping clearly differentiates between low stock, no stock, and unknown/unavailable statuses.

* ## 6. Final Output
    After transformation:

    - All prices are clean and numeric.  
    - All dates follow a consistent datetime format.  
    - All stock levels are standardized to integer codes.  
    - No duplicates or unhandled missing values remain.  

    The resulting dataset is now consistent, reliable, and ready for loading into the next stage of the ETL pipeline or database integration.


2.  **Load:**
    * Create a simple SQLite database (`parts_avatar.db`).
    * Load the cleaned supplier data and the product metadata into two separate tables in the database. Ensure the data types are correct and consider setting up primary keys.

3.  **Analyze & Visualize:**
    * Write a Python script or a Jupyter Notebook to query the SQLite database and answer the following business questions:
        * What is the average cost price per product category?
        * Which top 5 parts have the highest stock levels right now?
        * How has the number of new parts entries from this supplier changed over time (on a monthly basis)?
    * Create at least two clear and informative visualizations (e.g., using Matplotlib, Seaborn, or Plotly) to present your findings.

4.  **Documentation:**
    * Update this `README.md` file to be a comprehensive report of your project.
    * Explain your data cleaning strategies and justify your decisions.
    * Describe the schema of your database tables.
    * Present your findings from the analysis, including the visualizations you created.
    * Provide clear instructions on how to run your entire pipeline from start to finish.

## Evaluation Criteria
* **Problem-Solving:** The logic and justification behind your data cleaning and transformation decisions.
* **Python & SQL Proficiency:** The quality, efficiency, and organization of your code.
* **Data Engineering Concepts:** The structure and robustness of your ETL pipeline.
* **Data Visualization & Communication:** The clarity and impact of your analysis and visualizations in the README report.

## Disclaimer: Data and Evaluation Criteria
Please be advised that the datasets utilized in this project are synthetically generated and intended for illustrative purposes only. Furthermore, they have been significantly reduced in terms of sample size and the number of features to streamline the exercise. They do not represent or correspond to any actual business data. The primary objective of this evaluation is to assess the problem-solving methodology and the strategic approach employed, not necessarily the best possible tailored solution for the data. 
