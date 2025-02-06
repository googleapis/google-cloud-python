import argparse
import csv
import os
import sys

import google.api_core.exceptions
from google.cloud import bigquery


def preprocess_csv(input_file_path, output_file_path):
    try:
        with open(
            input_file_path, mode="r", newline="", encoding="utf-8"
        ) as infile, open(
            output_file_path, mode="w", newline="", encoding="utf-8"
        ) as outfile:
            reader = csv.reader(infile, delimiter="|")
            writer = csv.writer(outfile, delimiter="|")

            for row in reader:
                writer.writerow(row[:-1])
    except Exception as e:
        print(f"An error occurred: {e}")


def get_schema(table_name):
    schema = {
        "customer_address": [
            bigquery.SchemaField("ca_address_sk", "INTEGER", mode="REQUIRED"),
            bigquery.SchemaField("ca_address_id", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("ca_street_number", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("ca_street_name", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("ca_street_type", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("ca_suite_number", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("ca_city", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("ca_county", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("ca_state", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("ca_zip", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("ca_country", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("ca_gmt_offset", "FLOAT", mode="NULLABLE"),
            bigquery.SchemaField("ca_location_type", "STRING", mode="NULLABLE"),
        ],
        "customer_demographics": [
            bigquery.SchemaField("cd_demo_sk", "INTEGER", mode="REQUIRED"),
            bigquery.SchemaField("cd_gender", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("cd_marital_status", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("cd_education_status", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("cd_purchase_estimate", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("cd_credit_rating", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("cd_dep_count", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("cd_dep_employed_count", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("cd_dep_college_count", "INTEGER", mode="NULLABLE"),
        ],
        "date_dim": [
            bigquery.SchemaField("d_date_sk", "INTEGER", mode="REQUIRED"),
            bigquery.SchemaField("d_date_id", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("d_date", "DATE", mode="NULLABLE"),
            bigquery.SchemaField("d_month_seq", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("d_week_seq", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("d_quarter_seq", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("d_year", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("d_dow", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("d_moy", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("d_dom", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("d_qoy", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("d_fy_year", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("d_fy_quarter_seq", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("d_fy_week_seq", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("d_day_name", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("d_quarter_name", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("d_holiday", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("d_weekend", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("d_following_holiday", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("d_first_dom", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("d_last_dom", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("d_same_day_ly", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("d_same_day_lq", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("d_current_day", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("d_current_week", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("d_current_month", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("d_current_quarter", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("d_current_year", "STRING", mode="NULLABLE"),
        ],
        "warehouse": [
            bigquery.SchemaField("w_warehouse_sk", "INTEGER", mode="REQUIRED"),
            bigquery.SchemaField("w_warehouse_id", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("w_warehouse_name", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("w_warehouse_sq_ft", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("w_street_number", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("w_street_name", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("w_street_type", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("w_suite_number", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("w_city", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("w_county", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("w_state", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("w_zip", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("w_country", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("w_gmt_offset", "FLOAT", mode="NULLABLE"),
        ],
        "ship_mode": [
            bigquery.SchemaField("sm_ship_mode_sk", "INTEGER", mode="REQUIRED"),
            bigquery.SchemaField("sm_ship_mode_id", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("sm_type", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("sm_code", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("sm_carrier", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("sm_contract", "STRING", mode="NULLABLE"),
        ],
        "time_dim": [
            bigquery.SchemaField("t_time_sk", "INTEGER", mode="REQUIRED"),
            bigquery.SchemaField("t_time_id", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("t_time", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("t_hour", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("t_minute", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("t_second", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("t_am_pm", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("t_shift", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("t_sub_shift", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("t_meal_time", "STRING", mode="NULLABLE"),
        ],
        "reason": [
            bigquery.SchemaField("r_reason_sk", "INTEGER", mode="REQUIRED"),
            bigquery.SchemaField("r_reason_id", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("r_reason_desc", "STRING", mode="NULLABLE"),
        ],
        "income_band": [
            bigquery.SchemaField("ib_income_band_sk", "INTEGER", mode="REQUIRED"),
            bigquery.SchemaField("ib_lower_bound", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("ib_upper_bound", "INTEGER", mode="NULLABLE"),
        ],
        "item": [
            bigquery.SchemaField("i_item_sk", "INTEGER", mode="REQUIRED"),
            bigquery.SchemaField("i_item_id", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("i_rec_start_date", "DATE", mode="NULLABLE"),
            bigquery.SchemaField("i_rec_end_date", "DATE", mode="NULLABLE"),
            bigquery.SchemaField("i_item_desc", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("i_current_price", "FLOAT", mode="NULLABLE"),
            bigquery.SchemaField("i_wholesale_cost", "FLOAT", mode="NULLABLE"),
            bigquery.SchemaField("i_brand_id", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("i_brand", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("i_class_id", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("i_class", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("i_category_id", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("i_category", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("i_manufact_id", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("i_manufact", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("i_size", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("i_formulation", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("i_color", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("i_units", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("i_container", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("i_manager_id", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("i_product_name", "STRING", mode="NULLABLE"),
        ],
        "store": [
            bigquery.SchemaField("s_store_sk", "INTEGER", mode="REQUIRED"),
            bigquery.SchemaField("s_store_id", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("s_rec_start_date", "DATE", mode="NULLABLE"),
            bigquery.SchemaField("s_rec_end_date", "DATE", mode="NULLABLE"),
            bigquery.SchemaField("s_closed_date_sk", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("s_store_name", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("s_number_employees", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("s_floor_space", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("s_hours", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("s_manager", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("s_market_id", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("s_geography_class", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("s_market_desc", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("s_market_manager", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("s_division_id", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("s_division_name", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("s_company_id", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("s_company_name", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("s_street_number", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("s_street_name", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("s_street_type", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("s_suite_number", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("s_city", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("s_county", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("s_state", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("s_zip", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("s_country", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("s_gmt_offset", "FLOAT", mode="NULLABLE"),
            bigquery.SchemaField("s_tax_precentage", "FLOAT", mode="NULLABLE"),
        ],
        "call_center": [
            bigquery.SchemaField("cc_call_center_sk", "INTEGER", mode="REQUIRED"),
            bigquery.SchemaField("cc_call_center_id", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("cc_rec_start_date", "DATE", mode="NULLABLE"),
            bigquery.SchemaField("cc_rec_end_date", "DATE", mode="NULLABLE"),
            bigquery.SchemaField("cc_closed_date_sk", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("cc_open_date_sk", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("cc_name", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("cc_class", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("cc_employees", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("cc_sq_ft", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("cc_hours", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("cc_manager", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("cc_mkt_id", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("cc_mkt_class", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("cc_mkt_desc", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("cc_market_manager", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("cc_division", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("cc_division_name", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("cc_company", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("cc_company_name", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("cc_street_number", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("cc_street_name", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("cc_street_type", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("cc_suite_number", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("cc_city", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("cc_county", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("cc_state", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("cc_zip", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("cc_country", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("cc_gmt_offset", "FLOAT", mode="NULLABLE"),
            bigquery.SchemaField("cc_tax_percentage", "FLOAT", mode="NULLABLE"),
        ],
        "customer": [
            bigquery.SchemaField("c_customer_sk", "INTEGER", mode="REQUIRED"),
            bigquery.SchemaField("c_customer_id", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("c_current_cdemo_sk", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("c_current_hdemo_sk", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("c_current_addr_sk", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("c_first_shipto_date_sk", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("c_first_sales_date_sk", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("c_salutation", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("c_first_name", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("c_last_name", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("c_preferred_cust_flag", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("c_birth_day", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("c_birth_month", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("c_birth_year", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("c_birth_country", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("c_login", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("c_email_address", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("c_last_review_date_sk", "STRING", mode="NULLABLE"),
        ],
        "web_site": [
            bigquery.SchemaField("web_site_sk", "INTEGER", mode="REQUIRED"),
            bigquery.SchemaField("web_site_id", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("web_rec_start_date", "DATE", mode="NULLABLE"),
            bigquery.SchemaField("web_rec_end_date", "DATE", mode="NULLABLE"),
            bigquery.SchemaField("web_name", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("web_open_date_sk", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("web_close_date_sk", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("web_class", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("web_manager", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("web_mkt_id", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("web_mkt_class", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("web_mkt_desc", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("web_market_manager", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("web_company_id", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("web_company_name", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("web_street_number", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("web_street_name", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("web_street_type", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("web_suite_number", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("web_city", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("web_county", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("web_state", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("web_zip", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("web_country", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("web_gmt_offset", "FLOAT", mode="NULLABLE"),
            bigquery.SchemaField("web_tax_percentage", "FLOAT", mode="NULLABLE"),
        ],
        "store_returns": [
            bigquery.SchemaField("sr_returned_date_sk", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("sr_return_time_sk", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("sr_item_sk", "INTEGER", mode="REQUIRED"),
            bigquery.SchemaField("sr_customer_sk", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("sr_cdemo_sk", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("sr_hdemo_sk", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("sr_addr_sk", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("sr_store_sk", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("sr_reason_sk", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("sr_ticket_number", "INTEGER", mode="REQUIRED"),
            bigquery.SchemaField("sr_return_quantity", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("sr_return_amt", "FLOAT", mode="NULLABLE"),
            bigquery.SchemaField("sr_return_tax", "FLOAT", mode="NULLABLE"),
            bigquery.SchemaField("sr_return_amt_inc_tax", "FLOAT", mode="NULLABLE"),
            bigquery.SchemaField("sr_fee", "FLOAT", mode="NULLABLE"),
            bigquery.SchemaField("sr_return_ship_cost", "FLOAT", mode="NULLABLE"),
            bigquery.SchemaField("sr_refunded_cash", "FLOAT", mode="NULLABLE"),
            bigquery.SchemaField("sr_reversed_charge", "FLOAT", mode="NULLABLE"),
            bigquery.SchemaField("sr_store_credit", "FLOAT", mode="NULLABLE"),
            bigquery.SchemaField("sr_net_loss", "FLOAT", mode="NULLABLE"),
        ],
        "household_demographics": [
            bigquery.SchemaField("hd_demo_sk", "INTEGER", mode="REQUIRED"),
            bigquery.SchemaField("hd_income_band_sk", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("hd_buy_potential", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("hd_dep_count", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("hd_vehicle_count", "INTEGER", mode="NULLABLE"),
        ],
        "web_page": [
            bigquery.SchemaField("wp_web_page_sk", "INTEGER", mode="REQUIRED"),
            bigquery.SchemaField("wp_web_page_id", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("wp_rec_start_date", "DATE", mode="NULLABLE"),
            bigquery.SchemaField("wp_rec_end_date", "DATE", mode="NULLABLE"),
            bigquery.SchemaField("wp_creation_date_sk", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("wp_access_date_sk", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("wp_autogen_flag", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("wp_customer_sk", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("wp_url", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("wp_type", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("wp_char_count", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("wp_link_count", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("wp_image_count", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("wp_max_ad_count", "INTEGER", mode="NULLABLE"),
        ],
        "promotion": [
            bigquery.SchemaField("p_promo_sk", "INTEGER", mode="REQUIRED"),
            bigquery.SchemaField("p_promo_id", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("p_start_date_sk", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("p_end_date_sk", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("p_item_sk", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("p_cost", "FLOAT", mode="NULLABLE"),
            bigquery.SchemaField("p_response_target", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("p_promo_name", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("p_channel_dmail", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("p_channel_email", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("p_channel_catalog", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("p_channel_tv", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("p_channel_radio", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("p_channel_press", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("p_channel_event", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("p_channel_demo", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("p_channel_details", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("p_purpose", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("p_discount_active", "STRING", mode="NULLABLE"),
        ],
        "catalog_page": [
            bigquery.SchemaField("cp_catalog_page_sk", "INTEGER", mode="REQUIRED"),
            bigquery.SchemaField("cp_catalog_page_id", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("cp_start_date_sk", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("cp_end_date_sk", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("cp_department", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("cp_catalog_number", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("cp_catalog_page_number", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("cp_description", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("cp_type", "STRING", mode="NULLABLE"),
        ],
        "inventory": [
            bigquery.SchemaField("inv_date_sk", "INTEGER", mode="REQUIRED"),
            bigquery.SchemaField("inv_item_sk", "INTEGER", mode="REQUIRED"),
            bigquery.SchemaField("inv_warehouse_sk", "INTEGER", mode="REQUIRED"),
            bigquery.SchemaField("inv_quantity_on_hand", "INTEGER", mode="NULLABLE"),
        ],
        "catalog_returns": [
            bigquery.SchemaField("cr_returned_date_sk", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("cr_returned_time_sk", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("cr_item_sk", "INTEGER", mode="REQUIRED"),
            bigquery.SchemaField("cr_refunded_customer_sk", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("cr_refunded_cdemo_sk", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("cr_refunded_hdemo_sk", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("cr_refunded_addr_sk", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField(
                "cr_returning_customer_sk", "INTEGER", mode="NULLABLE"
            ),
            bigquery.SchemaField("cr_returning_cdemo_sk", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("cr_returning_hdemo_sk", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("cr_returning_addr_sk", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("cr_call_center_sk", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("cr_catalog_page_sk", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("cr_ship_mode_sk", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("cr_warehouse_sk", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("cr_reason_sk", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("cr_order_number", "INTEGER", mode="REQUIRED"),
            bigquery.SchemaField("cr_return_quantity", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("cr_return_amount", "FLOAT", mode="NULLABLE"),
            bigquery.SchemaField("cr_return_tax", "FLOAT", mode="NULLABLE"),
            bigquery.SchemaField("cr_return_amt_inc_tax", "FLOAT", mode="NULLABLE"),
            bigquery.SchemaField("cr_fee", "FLOAT", mode="NULLABLE"),
            bigquery.SchemaField("cr_return_ship_cost", "FLOAT", mode="NULLABLE"),
            bigquery.SchemaField("cr_refunded_cash", "FLOAT", mode="NULLABLE"),
            bigquery.SchemaField("cr_reversed_charge", "FLOAT", mode="NULLABLE"),
            bigquery.SchemaField("cr_store_credit", "FLOAT", mode="NULLABLE"),
            bigquery.SchemaField("cr_net_loss", "FLOAT", mode="NULLABLE"),
        ],
        "web_returns": [
            bigquery.SchemaField("wr_returned_date_sk", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("wr_returned_time_sk", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("wr_item_sk", "INTEGER", mode="REQUIRED"),
            bigquery.SchemaField("wr_refunded_customer_sk", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("wr_refunded_cdemo_sk", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("wr_refunded_hdemo_sk", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("wr_refunded_addr_sk", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField(
                "wr_returning_customer_sk", "INTEGER", mode="NULLABLE"
            ),
            bigquery.SchemaField("wr_returning_cdemo_sk", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("wr_returning_hdemo_sk", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("wr_returning_addr_sk", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("wr_web_page_sk", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("wr_reason_sk", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("wr_order_number", "INTEGER", mode="REQUIRED"),
            bigquery.SchemaField("wr_return_quantity", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("wr_return_amt", "FLOAT", mode="NULLABLE"),
            bigquery.SchemaField("wr_return_tax", "FLOAT", mode="NULLABLE"),
            bigquery.SchemaField("wr_return_amt_inc_tax", "FLOAT", mode="NULLABLE"),
            bigquery.SchemaField("wr_fee", "FLOAT", mode="NULLABLE"),
            bigquery.SchemaField("wr_return_ship_cost", "FLOAT", mode="NULLABLE"),
            bigquery.SchemaField("wr_refunded_cash", "FLOAT", mode="NULLABLE"),
            bigquery.SchemaField("wr_reversed_charge", "FLOAT", mode="NULLABLE"),
            bigquery.SchemaField("wr_account_credit", "FLOAT", mode="NULLABLE"),
            bigquery.SchemaField("wr_net_loss", "FLOAT", mode="NULLABLE"),
        ],
        "web_sales": [
            bigquery.SchemaField("ws_sold_date_sk", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("ws_sold_time_sk", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("ws_ship_date_sk", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("ws_item_sk", "INTEGER", mode="REQUIRED"),
            bigquery.SchemaField("ws_bill_customer_sk", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("ws_bill_cdemo_sk", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("ws_bill_hdemo_sk", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("ws_bill_addr_sk", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("ws_ship_customer_sk", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("ws_ship_cdemo_sk", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("ws_ship_hdemo_sk", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("ws_ship_addr_sk", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("ws_web_page_sk", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("ws_web_site_sk", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("ws_ship_mode_sk", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("ws_warehouse_sk", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("ws_promo_sk", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("ws_order_number", "INTEGER", mode="REQUIRED"),
            bigquery.SchemaField("ws_quantity", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("ws_wholesale_cost", "FLOAT", mode="NULLABLE"),
            bigquery.SchemaField("ws_list_price", "FLOAT", mode="NULLABLE"),
            bigquery.SchemaField("ws_sales_price", "FLOAT", mode="NULLABLE"),
            bigquery.SchemaField("ws_ext_discount_amt", "FLOAT", mode="NULLABLE"),
            bigquery.SchemaField("ws_ext_sales_price", "FLOAT", mode="NULLABLE"),
            bigquery.SchemaField("ws_ext_wholesale_cost", "FLOAT", mode="NULLABLE"),
            bigquery.SchemaField("ws_ext_list_price", "FLOAT", mode="NULLABLE"),
            bigquery.SchemaField("ws_ext_tax", "FLOAT", mode="NULLABLE"),
            bigquery.SchemaField("ws_coupon_amt", "FLOAT", mode="NULLABLE"),
            bigquery.SchemaField("ws_ext_ship_cost", "FLOAT", mode="NULLABLE"),
            bigquery.SchemaField("ws_net_paid", "FLOAT", mode="NULLABLE"),
            bigquery.SchemaField("ws_net_paid_inc_tax", "FLOAT", mode="NULLABLE"),
            bigquery.SchemaField("ws_net_paid_inc_ship", "FLOAT", mode="NULLABLE"),
            bigquery.SchemaField("ws_net_paid_inc_ship_tax", "FLOAT", mode="NULLABLE"),
            bigquery.SchemaField("ws_net_profit", "FLOAT", mode="NULLABLE"),
        ],
        "catalog_sales": [
            bigquery.SchemaField("cs_sold_date_sk", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("cs_sold_time_sk", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("cs_ship_date_sk", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("cs_bill_customer_sk", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("cs_bill_cdemo_sk", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("cs_bill_hdemo_sk", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("cs_bill_addr_sk", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("cs_ship_customer_sk", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("cs_ship_cdemo_sk", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("cs_ship_hdemo_sk", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("cs_ship_addr_sk", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("cs_call_center_sk", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("cs_catalog_page_sk", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("cs_ship_mode_sk", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("cs_warehouse_sk", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("cs_item_sk", "INTEGER", mode="REQUIRED"),
            bigquery.SchemaField("cs_promo_sk", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("cs_order_number", "INTEGER", mode="REQUIRED"),
            bigquery.SchemaField("cs_quantity", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("cs_wholesale_cost", "FLOAT", mode="NULLABLE"),
            bigquery.SchemaField("cs_list_price", "FLOAT", mode="NULLABLE"),
            bigquery.SchemaField("cs_sales_price", "FLOAT", mode="NULLABLE"),
            bigquery.SchemaField("cs_ext_discount_amt", "FLOAT", mode="NULLABLE"),
            bigquery.SchemaField("cs_ext_sales_price", "FLOAT", mode="NULLABLE"),
            bigquery.SchemaField("cs_ext_wholesale_cost", "FLOAT", mode="NULLABLE"),
            bigquery.SchemaField("cs_ext_list_price", "FLOAT", mode="NULLABLE"),
            bigquery.SchemaField("cs_ext_tax", "FLOAT", mode="NULLABLE"),
            bigquery.SchemaField("cs_coupon_amt", "FLOAT", mode="NULLABLE"),
            bigquery.SchemaField("cs_ext_ship_cost", "FLOAT", mode="NULLABLE"),
            bigquery.SchemaField("cs_net_paid", "FLOAT", mode="NULLABLE"),
            bigquery.SchemaField("cs_net_paid_inc_tax", "FLOAT", mode="NULLABLE"),
            bigquery.SchemaField("cs_net_paid_inc_ship", "FLOAT", mode="NULLABLE"),
            bigquery.SchemaField("cs_net_paid_inc_ship_tax", "FLOAT", mode="NULLABLE"),
            bigquery.SchemaField("cs_net_profit", "FLOAT", mode="NULLABLE"),
        ],
        "store_sales": [
            bigquery.SchemaField("ss_sold_date_sk", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("ss_sold_time_sk", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("ss_item_sk", "INTEGER", mode="REQUIRED"),
            bigquery.SchemaField("ss_customer_sk", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("ss_cdemo_sk", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("ss_hdemo_sk", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("ss_addr_sk", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("ss_store_sk", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("ss_promo_sk", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("ss_ticket_number", "INTEGER", mode="REQUIRED"),
            bigquery.SchemaField("ss_quantity", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("ss_wholesale_cost", "FLOAT", mode="NULLABLE"),
            bigquery.SchemaField("ss_list_price", "FLOAT", mode="NULLABLE"),
            bigquery.SchemaField("ss_sales_price", "FLOAT", mode="NULLABLE"),
            bigquery.SchemaField("ss_ext_discount_amt", "FLOAT", mode="NULLABLE"),
            bigquery.SchemaField("ss_ext_sales_price", "FLOAT", mode="NULLABLE"),
            bigquery.SchemaField("ss_ext_wholesale_cost", "FLOAT", mode="NULLABLE"),
            bigquery.SchemaField("ss_ext_list_price", "FLOAT", mode="NULLABLE"),
            bigquery.SchemaField("ss_ext_tax", "FLOAT", mode="NULLABLE"),
            bigquery.SchemaField("ss_coupon_amt", "FLOAT", mode="NULLABLE"),
            bigquery.SchemaField("ss_net_paid", "FLOAT", mode="NULLABLE"),
            bigquery.SchemaField("ss_net_paid_inc_tax", "FLOAT", mode="NULLABLE"),
            bigquery.SchemaField("ss_net_profit", "FLOAT", mode="NULLABLE"),
        ],
    }

    return schema[table_name]


def load_data_to_bigquery(table_name, file_paths, client, dataset_ref, temp_file):
    """Loads data from a list of files into a BigQuery table."""
    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=0,  # No header in .dat files
        field_delimiter="|",
        schema=get_schema(table_name),
    )

    table_ref = dataset_ref.table(table_name)
    table = bigquery.Table(table_ref)
    client.create_table(table)

    # Load data from each file
    for file_path in sorted(file_paths):
        preprocess_csv(file_path, temp_file)
        with open(temp_file, "rb") as source_file:
            job = client.load_table_from_file(
                source_file, table_ref, job_config=job_config
            )
            job.result()
        print(
            f"Loaded data from {file_path} into table {project_id}:{dataset_id}.{table_name}"
        )


if __name__ == "__main__":
    """
    Loads TPC-DS data to BigQuery.

    This script loads TPC-DS data generated with source code from
    https://www.tpc.org/tpc_documents_current_versions/current_specifications5.asp
    into BigQuery.

    Note: If the dataset already exists, the script will exit without uploading data.

    Usage:
        python tpcds_upload_helper.py --project_id <project_id> --dataset_id <dataset_id> --ds_path <local_data_path>
        python tpcds_upload_helper.py -d <dataset_id> -p <project_id> -s <local_data_path>
    """
    parser = argparse.ArgumentParser(description="Load TPC-DS data to BigQuery")
    parser.add_argument(
        "--project_id", "-p", required=True, help="Google Cloud project ID"
    )
    parser.add_argument("--dataset_id", "-d", required=True, help="BigQuery dataset ID")
    parser.add_argument(
        "--ds_path", "-s", required=True, help="Path to the TPC-DS data directory"
    )
    args = parser.parse_args()

    project_id = args.project_id
    dataset_id = args.dataset_id
    ds_path = args.ds_path
    temp_file = "temp.csv"

    # Initialize BigQuery client
    client = bigquery.Client(project=project_id)
    dataset_ref = client.dataset(dataset_id)
    try:
        # Quit if dataset exists
        client.get_dataset(dataset_ref)
        print(f"Dataset {project_id}:{dataset_id} already exists. Skipping.")
        sys.exit(1)
    except google.api_core.exceptions.NotFound:
        # Create the dataset if it doesn't exist
        dataset = bigquery.Dataset(dataset_ref)
        client.create_dataset(dataset)
        print(f"Created dataset {project_id}:{dataset_id}")

    # Iterate through the folders
    for table_name in sorted(os.listdir(ds_path)):
        table_path = os.path.join(ds_path, table_name)
        table_name = table_name.split(".")[0]
        if os.path.isdir(table_path):
            file_paths = [
                os.path.join(table_path, f)
                for f in os.listdir(table_path)
                if f.endswith(".dat")
            ]
            load_data_to_bigquery(
                table_name, file_paths, client, dataset_ref, temp_file
            )

    try:
        os.remove(temp_file)
        print("Removed temporary file: temp.csv")
    except FileNotFoundError:
        print("Temporary file not found.")
