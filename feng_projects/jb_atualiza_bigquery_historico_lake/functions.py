import logging
import pandas as pd

from sqlalchemy import text
from snowflake.connector.pandas_tools import pd_writer
from utils import connect_bigquery, connect_dw_lake_spfc


def pipeline(team, property_id, date_str, table):
    try:
        logging.info(f"Buscando dados {team}.{table}")
        df = get_data(property_id, date_str, table)
        logging.info(f"{len(df)} dados pra inserir {team}.{table}")
        insert_data(df, team, date_str, table)
        logging.info(f"Dados inseridos {team}.{table}")
    except Exception as e:
        logging.error(f"Erro {team}.{table}: {e}")
        raise


def get_data(property_id, date_str, table):
    """
    Faz uma query no BigQuery e retorna um DataFrame com os dados

    Parâmetros:
        bq_client (google.cloud.bigquery.client.Client): client do BigQuery
        query (str): query a ser executada

    Retorna:
        pandas.DataFrame: DataFrame com os dados
    """

    if table == "bigquery_base":
        query = f"""
        select
            a.event_date,
            FORMAT_DATE('%Y-%m-%d', PARSE_DATE('%Y%m%d', CAST(event_date AS STRING))) AS EVENT_BR_TIMESTAMP,
            a.event_name,
            a.user_id,
            a.user_pseudo_id,
            (
            select
                kv.value.string_value
            FROM
                UNNEST(event_params) AS kv
            WHERE
                kv.key = 'transaction_id'
            ) AS transaction_id,
            (
            select
                kv.value.string_value
            FROM
                UNNEST(event_params) AS kv
            WHERE
                kv.key = 'page_referrer'
            ) AS page_referrer,
            (
            select
                kv.value.string_value
            FROM
                UNNEST(event_params) AS kv
            WHERE
                kv.key = 'page_location'
            ) AS page_location,
            (
                select
                kv.value.string_value
                FROM
                UNNEST(event_params) AS kv
                WHERE
                kv.key = 'page_title'
            ) AS page_title,
            (
                select
                kv.value.string_value
                FROM
                UNNEST(event_params) AS kv
                WHERE
                kv.key = 'btn_plano'
            ) AS btn_plano,
            (
                select
                kv.value.string_value
                FROM
                UNNEST(event_params) AS kv
                WHERE
                kv.key = 'btn_text'
            ) AS btn_text,
            (
                select
                kv.value.string_value
                FROM
                UNNEST(event_params) AS kv
                WHERE
                kv.key = 'btn_section'
            ) AS btn_section,
            CASE
                WHEN (
                    select kv.value.string_value
                    FROM UNNEST(event_params) AS kv
                    WHERE kv.key = 'payment_type'
                ) IS NOT NULL THEN (
                    select kv.value.string_value
                    FROM UNNEST(event_params) AS kv
                    WHERE kv.key = 'payment_type'
                )
                WHEN (
                    select kv.value.string_value
                    FROM UNNEST(event_params) AS kv
                    WHERE kv.key = 'is_pix'
                ) = 'true' THEN 'PIX'
                WHEN (
                    select kv.value.string_value
                    FROM UNNEST(event_params) AS kv
                    WHERE kv.key = 'is_credit_card'
                ) = 'true' THEN 'CARTÃO DE CRÉDITO'
                ELSE 'unknown'
            end as payment_type,
            (
                select
                kv.value.string_value
                FROM
                UNNEST(event_params) AS kv
                WHERE
                kv.key = 'section'
            ) AS section,
            (
                select
                kv.value.string_value
                FROM
                UNNEST(event_params) AS kv
                WHERE
                kv.key = 'source_platform'
            ) AS source_platform,
            (select value.int_value FROM UNNEST(event_params) WHERE key = "ga_session_id") AS ga_session_id,
            a.device.category,
            a.device.mobile_brand_name,
            a.device.mobile_marketing_name,
            a.device.operating_system,
            a.device.operating_system_version,
            a.device.web_info.browser,
            geo.city,
            geo.country,
            geo.sub_continent,
            traffic_source.name as traffic_source_name,
            traffic_source.medium as traffic_source_medium,
            traffic_source.source as traffic_source_source,
            (
                select 
                kv.item_name
                FROM UNNEST(items) as kv
            ) as item_name,
            (
                select 
                kv.item_category3
                FROM UNNEST(items) as kv
            ) as periodicity,
            (
                select 
                kv.item_category4
                FROM UNNEST(items) as kv
            ) as operation,
            (
                select 
                kv.coupon
                FROM UNNEST(items) as kv
            ) as coupon,
            a.collected_traffic_source.manual_campaign_id as collected_campaign_id,
            a.collected_traffic_source.manual_campaign_name as collected_campaign,
            a.collected_traffic_source.manual_source as collected_source,
            a.collected_traffic_source.manual_medium as collected_medium,
            a.session_traffic_source_last_click.cross_channel_campaign.campaign_id as cross_channel_campaign_id,
            a.session_traffic_source_last_click.cross_channel_campaign.campaign_name as cross_channel_campaign,
            a.session_traffic_source_last_click.cross_channel_campaign.source as cross_channel_source,
            -- a.session_traffic_source_last_click.cross_channel_campaign.medium as cross_channel_medium
            CASE
                WHEN UPPER(TRIM(REGEXP_REPLACE(a.session_traffic_source_last_click.cross_channel_campaign.medium, r'[()]', ''))) LIKE '%CPC%' THEN 'MIDIA PAGA'
                WHEN UPPER(TRIM(REGEXP_REPLACE(a.session_traffic_source_last_click.cross_channel_campaign.medium, r'[()]', ''))) IN ('PAID') THEN 'MIDIA PAGA'
                WHEN UPPER(TRIM(REGEXP_REPLACE(a.session_traffic_source_last_click.cross_channel_campaign.medium, r'[()]', ''))) IN (
                'BOTAO','BOTÃO','SPFC','DATA NOT AVAILABLE','CUPOM','PRE_HOME','ST','2024_NOVIDADES','CBAAFE',
                'EVENT-DISCOVERY-PLATFORM','MORUMBIBRANCO'
                ) THEN 'NI'
                WHEN UPPER(TRIM(REGEXP_REPLACE(a.session_traffic_source_last_click.cross_channel_campaign.medium, r'[()]', ''))) IN ('NONE','REFERRAL') THEN 'SEM REFERENCIA'
                WHEN UPPER(TRIM(REGEXP_REPLACE(a.session_traffic_source_last_click.cross_channel_campaign.medium, r'[()]', ''))) = 'ORGANIC' THEN 'ORGÂNICO'
                WHEN UPPER(TRIM(REGEXP_REPLACE(a.session_traffic_source_last_click.cross_channel_campaign.medium, r'[()]', ''))) IN (
                'EMAIL','ATIVOS','SOCIOSATIVOS','BASE_LEADS','LEADSSP','SOCIOS','LEADS','SOCIOSINATIVOS','LEADSOFFSP'
                ) THEN 'EMAIL'
                WHEN UPPER(TRIM(REGEXP_REPLACE(a.session_traffic_source_last_click.cross_channel_campaign.medium, r'[()]', ''))) IN (
                'BANNER','SPFCTICKET_HELPCENTER','BOTAO_PLANOBRANCO','BOTAO_RODAPE','SPFCTICKET'
                ) THEN 'SPFCTICKET'
                WHEN UPPER(TRIM(REGEXP_REPLACE(a.session_traffic_source_last_click.cross_channel_campaign.medium, r'[()]', ''))) = 'APP_BANNER' THEN 'APLICATIVO'
                WHEN UPPER(TRIM(REGEXP_REPLACE(a.session_traffic_source_last_click.cross_channel_campaign.medium, r'[()]', ''))) = 'WHATSAPP_STNASOITAVAS' THEN 'WHATSAPP'
                WHEN UPPER(TRIM(REGEXP_REPLACE(a.session_traffic_source_last_click.cross_channel_campaign.medium, r'[()]', ''))) = 'SOCIAL' THEN 'REDE SOCIAL'
                WHEN UPPER(TRIM(REGEXP_REPLACE(a.session_traffic_source_last_click.cross_channel_campaign.medium, r'[()]', ''))) = 'DIRECT' THEN 'ACESSO DIRETO'
                WHEN UPPER(TRIM(REGEXP_REPLACE(a.session_traffic_source_last_click.cross_channel_campaign.medium, r'[()]', ''))) = 'NOT SET' THEN 'NOT SET'
                ELSE a.session_traffic_source_last_click.cross_channel_campaign.medium
                end as cross_channel_medium,
                (
                select
                    kv.value.string_value
                from
                    unnest(event_params) as kv
                where
                    kv.key = 'has_credit_card'
                ) as has_credit_card,
                (
                select
                    kv.value.string_value
                from
                    unnest(event_params) as kv
                where
                    kv.key = 'has_address'
                ) as has_address
            from `{"analyitics-comunicacao-fla" if property_id == "337970043" else "bigquery-projetos"}.analytics_{property_id}.events_{date_str.replace("-", "")}` as a
            where a.event_name not in (
            'pageView',
            'buttonClicked',
            'button_clicked-ancora_assine_a_peticao-p',
            'button_clicked-assinar_a_petição-page_ho',
            'button_clicked-fazer_download_do_selo-pa',
            'button_clicked-seja_sócio-torcedor-page_',
            'file_download');
        """

    elif table == "bigquery_automation_crm":
        query = f"""
        WITH views AS (
            SELECT
                event_date,
                campaign_name_cross,
                city,
                SUM(screen_page_views) AS views
            FROM (
                SELECT
                    event_date,
                    user_pseudo_id,
                    geo.city AS city,
                    session_traffic_source_last_click.cross_channel_campaign.campaign_name AS campaign_name_cross,
                    COUNT(CASE WHEN event_name = 'page_view' THEN 1 END) AS screen_page_views
                FROM `{"analyitics-comunicacao-fla" if property_id == "337970043" else "bigquery-projetos"}.analytics_{property_id}.events_{date_str.replace("-", "")}`
                GROUP BY 1,2,3,4
            )
            GROUP BY 1,2,3
        ),

        sessions AS (
            SELECT
                event_date,
                campaign_name_cross,
                city,
                COUNT(DISTINCT CONCAT(user_pseudo_id, "-", ga_session_id)) AS sessions
            FROM (
                SELECT
                    event_date,
                    user_pseudo_id,
                    geo.city AS city,
                    session_traffic_source_last_click.cross_channel_campaign.campaign_name AS campaign_name_cross,
                    (
                        SELECT value.int_value
                        FROM UNNEST(event_params)
                        WHERE key = "ga_session_id"
                    ) AS ga_session_id
                FROM `{"analyitics-comunicacao-fla" if property_id == "337970043" else "bigquery-projetos"}.analytics_{property_id}.events_{date_str.replace("-", "")}`
            )
            GROUP BY 1,2,3
        ),

        active_users AS (
            SELECT
                event_date,
                campaign_name_cross,
                city,
                COUNT(DISTINCT active_users) AS active_users
            FROM (
                SELECT
                    event_date,
                    user_pseudo_id,
                    geo.city AS city,
                    session_traffic_source_last_click.cross_channel_campaign.campaign_name AS campaign_name_cross,
                    MAX(
                        CASE
                            WHEN is_active_user THEN user_pseudo_id
                            ELSE NULL
                        END
                    ) AS active_users
                FROM `{"analyitics-comunicacao-fla" if property_id == "337970043" else "bigquery-projetos"}.analytics_{property_id}.events_{date_str.replace("-", "")}`
                GROUP BY 1,2,3,4
            )
            GROUP BY 1,2,3
        ),

        outros AS (
            SELECT
                event_date,
                campaign_name_cross,
                city,
                SUM(add_to_cart) AS add_to_cart,
                COUNT(DISTINCT total_purchasers) AS total_purchasers,
                SUM(revenue) AS revenue
            FROM (
                SELECT
                    event_date,
                    user_pseudo_id,
                    geo.city AS city,
                    session_traffic_source_last_click.cross_channel_campaign.campaign_name AS campaign_name_cross,
                    SUM(
                        CASE
                            WHEN event_name = 'add_to_cart' THEN 1
                            ELSE 0
                        END
                    ) AS add_to_cart,
                    MAX(
                        CASE
                            WHEN event_name = 'purchase' THEN user_pseudo_id
                            ELSE NULL
                        END
                    ) AS total_purchasers,
                    SUM(ecommerce.purchase_revenue) AS revenue
                FROM `{"analyitics-comunicacao-fla" if property_id == "337970043" else "bigquery-projetos"}.analytics_{property_id}.events_{date_str.replace("-", "")}`
                GROUP BY 1,2,3,4
            )
            GROUP BY 1,2,3
        )

        SELECT
            FORMAT_DATE(
                '%Y-%m-%d',
                PARSE_DATE('%Y%m%d', CAST(event_date AS STRING))
            ) AS EVENT_BR_TIMESTAMP,
            campaign_name_cross AS CAMPAIGN_NAME_CROSS,
            city AS CITY,
            IFNULL(v.views, 0) AS views,
            IFNULL(s.sessions, 0) AS sessions,
            IFNULL(au.active_users, 0) AS active_users,
            IFNULL(ac.add_to_cart, 0) AS add_to_cart,
            IFNULL(ac.total_purchasers, 0) AS total_purchasers,
            IFNULL(ac.revenue, 0) AS revenue

        FROM views v
        FULL OUTER JOIN sessions s
            USING (event_date, campaign_name_cross, city)

        FULL OUTER JOIN active_users au
            USING (event_date, campaign_name_cross, city)

        FULL OUTER JOIN outros ac
            USING (event_date, campaign_name_cross, city)

        ORDER BY
            event_date,
            campaign_name_cross,
            city
        """

    bq_client = connect_bigquery(
        "FLA_CREDENTIALS_JSON" if property_id == "337970043" else "CREDENTIALS_JSON"
    )

    query_job = bq_client.query(query)

    if property_id == "337970043":
        df = query_job.result().to_dataframe(create_bqstorage_client=False)
    else:
        df = query_job.result().to_dataframe(create_bqstorage_client=True)

    # limitar strings a 250 caracteres
    for col in df.select_dtypes(include=["object", "string"]):
        df[col] = df[col].where(df[col].notna(), None)  # mantém nulos
        df[col] = df[col].apply(lambda x: x[:250] if isinstance(x, str) else x)

    logging.info(df.tail())

    return df


def insert_data(df, team: str, date_str: str, table: str) -> None:
    df = df.copy()
    df.columns = df.columns.map(str).str.upper()

    if "EVENT_DATE" in df.columns:
        df["EVENT_DATE"] = df["EVENT_DATE"].astype(str)

    schema = "BRONZE"

    CONN_BY_TEAM = {
        "SÃO PAULO": connect_dw_lake_spfc,  # <- sem ()
    }

    team_key = (team or "").strip().upper()
    connect_fn = CONN_BY_TEAM.get(team_key)
    if not connect_fn:
        raise ValueError(f"Time não mapeado: {team!r}. Válidos: {list(CONN_BY_TEAM.keys())}")

    conn = connect_fn()  

    with conn.begin() as sql:
        sql.execute(
            text(f"""
                DELETE FROM {schema}.{table}
                WHERE EVENT_BR_TIMESTAMP::DATE = :date_str
            """),
            {"date_str": date_str},
        )

        df.to_sql(
            name=table,
            con=sql,
            schema=schema,
            if_exists="append",
            index=False,
            method=pd_writer,
        )


