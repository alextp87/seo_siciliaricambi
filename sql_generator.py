
def genera_script_sql_keyphrase(dataframe, output_path="update_keyphrases.sql"):
    with open(output_path, "w", encoding="utf-8") as f:
        for _, row in dataframe.iterrows():
            product_id = row.get("ID", "")
            keyphrase = row.get("Focus Keyphrase", "")
            if product_id and keyphrase:
                query = f"UPDATE ps_ets_seo_product SET key_phrase = \"{keyphrase}\" WHERE id_product = {product_id};\n"
                f.write(query)
    return output_path
