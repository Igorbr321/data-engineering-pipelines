import re
import pandas as pd


def extract_pedidos(path_jan_jun: str, path_jul_dez: str, path_jan_2026: str) -> pd.DataFrame:
    dtype_jan_jun = {
        "Phone": "string",
        "Cancelled By": "string",
        "Cancellation Reason": "string",
    }

    dtype_jul_dez = {
        "Corporate Name": "string",
        "Delivered": "string",
    }

    df_jan_jun = pd.read_csv(path_jan_jun, sep=";", dtype=dtype_jan_jun, low_memory=False)
    df_jul_dez = pd.read_csv(path_jul_dez, sep=";", dtype=dtype_jul_dez, low_memory=False)
    df_jan_2026 = pd.read_csv(path_jan_2026, sep=";", low_memory=False)

    return pd.concat([df_jan_jun, df_jul_dez, df_jan_2026], ignore_index=True)


TIPOS = {
    # strings
    "Origin": "string",
    "Order": "string",
    "Client Name": "string",
    "Client Last Name": "string",
    "Client Document": "string",
    "Email": "string",
    "Phone": "string",
    "UF": "string",
    "City": "string",
    "Address Identification": "string",
    "Address Type": "string",
    "Receiver Name": "string",
    "Street": "string",
    "Number": "string",
    "Complement": "string",
    "Neighborhood": "string",
    "Reference": "string",
    "Postal Code": "string",
    "SLA Type": "string",
    "Courrier": "string",
    "Delivery Deadline": "string",
    "Status": "string",
    "UtmMedium": "string",
    "UtmSource": "string",
    "UtmCampaign": "string",
    "Coupon": "string",
    "Payment System Name": "string",
    "ID_SKU": "string",
    "Category Ids Sku": "string",
    "Reference Code": "string",
    "SKU Name": "string",
    "SKU Path": "string",
    "Item Attachments": "string",
    "List Id": "string",
    "List Type Name": "string",
    "Discounts Names": "string",
    "Call Center Email": "string",
    "Call Center Code": "string",
    "Tracking Number": "string",
    "Host": "string",
    "GiftRegistry ID": "string",
    "Seller Name": "string",
    "Status TimeLine": "string",
    "Obs": "string",
    "UtmiPart": "string",
    "UtmiCampaign": "string",
    "UtmiPage": "string",
    "Seller Order Id": "string",
    "Acquirer": "string",
    "Authorization Id": "string",
    "TID": "string",
    "NSU": "string",
    "Card First Digits": "string",
    "Card Last Digits": "string",
    "Payment Approved By": "string",
    "Cancelled By": "string",
    "Cancellation Reason": "string",
    "Gift Card Name": "string",
    "Gift Card Caption": "string",
    "Corporate Name": "string",
    "Corporate Document": "string",
    "TransactionId": "string",
    "PaymentId": "string",
    "PaymentOrigin": "string",
    "SalesChannel": "string",
    "marketingTags": "string",
    "Currency Code": "string",
    "Invoice Numbers": "string",
    "Country": "string",
    "Input Invoices Numbers": "string",
    "Output Invoices Numbers": "string",
    "Status raw value (temporary)": "string",

    # inteiros
    "Sequence": "Int64",
    "Installments": "Int64",
    "Quantity_SKU": "Int64",

    # floats
    "Payment Value": "Float64",
    "SKU Value": "Float64",
    "SKU Selling Price": "Float64",
    "SKU Total Price": "Float64",
    "Service (Price/ Selling Price)": "Float64",
    "Shipping List Price": "Float64",
    "Shipping Value": "Float64",
    "Total Value": "Float64",
    "Discounts Totals": "Float64",
    "SKU RewardValue": "Float64",
    "Taxes": "Float64",

    # booleanos
    "Delivered": "boolean",
    "Is Marketplace cetified": "boolean",
    "Is Checked In": "boolean",

    # datas
    "Creation Date": "datetime64[ns]",
    "Estimate Delivery Date": "datetime64[ns]",
    "Last Change Date": "datetime64[ns]",
    "Authorized Date": "datetime64[ns]",
    "Cancellation Data": "datetime64[ns]",
}

DT_COLS = [c for c, t in TIPOS.items() if t.startswith("datetime")]
INT_COLS = [c for c, t in TIPOS.items() if t == "Int64"]
FLOAT_COLS = [c for c, t in TIPOS.items() if t == "Float64"]
BOOL_COLS = [c for c, t in TIPOS.items() if t == "boolean"]
STR_COLS = [c for c, t in TIPOS.items() if t == "string"]


def to_str(s: pd.Series) -> pd.Series:
    s = s.astype("string[python]").str.strip()
    s = s.replace({"": pd.NA, "NA": pd.NA, "NaN": pd.NA, "None": pd.NA})
    return s.str.upper()


def to_datetime(s: pd.Series) -> pd.Series:
    s = s.astype("string").str.strip()
    dt = pd.to_datetime(s, errors="coerce", utc=True).dt.tz_convert(None).dt.floor("ms")
    return dt.dt.strftime("%Y-%m-%d %H:%M:%S.%f").str.slice(0, 23)


def to_number_str(s: pd.Series) -> pd.Series:
    s = to_str(s)
    s = s.str.replace(r"[^\d,\.\-]", "", regex=True)

    both = s.str.contains(",", na=False) & s.str.contains(r"\.", na=False)
    s = s.mask(both, s.str.replace(".", "", regex=False))

    return s.str.replace(",", ".", regex=False)


def to_float(s: pd.Series) -> pd.Series:
    return pd.to_numeric(to_number_str(s), errors="coerce").astype("Float64")


def to_int(s: pd.Series) -> pd.Series:
    s2 = to_number_str(s).str.split(".", n=1).str[0]
    return pd.to_numeric(s2, errors="coerce").astype("Int64")


def to_bool(s: pd.Series) -> pd.Series:
    s = s.astype("string[python]").str.strip().str.lower()
    m = {
        "true": True, "false": False,
        "1": True, "0": False,
        "sim": True, "não": False, "nao": False,
        "s": True, "n": False,
        "verdadeiro": True, "falso": False,
        "t": True, "f": False,
        "ok": True,
    }
    return s.map(m).astype("boolean")


def aplicar_schema(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [c.strip() for c in df.columns]

    for c in STR_COLS:
        if c in df.columns:
            df[c] = to_str(df[c])

    for c in DT_COLS:
        if c in df.columns:
            df[c] = to_datetime(df[c])

    for c in FLOAT_COLS:
        if c in df.columns:
            df[c] = to_float(df[c])

    for c in INT_COLS:
        if c in df.columns:
            df[c] = to_int(df[c])

    for c in BOOL_COLS:
        if c in df.columns:
            df[c] = to_bool(df[c])

    return df


def padronizar_colunas_pedidos(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    def norm(c: str) -> str:
        c = c.strip()
        c = re.sub(r"[()/]", " ", c)
        c = re.sub(r"[\s\-]+", "_", c)
        c = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", c)
        c = re.sub(r"[^A-Za-z0-9_]", "", c)
        c = c.upper()

        if c == "ORDER":
            c = "ORDER_ID"
        c = c.replace("ID_SKU", "SKU_ID")
        c = c.replace("QUANTITY_SKU", "SKU_QUANTITY")
        c = c.replace("COURRIER", "COURIER")
        c = c.replace("IS_MARKETPLACE_CETIFIED", "IS_MARKETPLACE_CERTIFIED")
        c = c.replace("CLIENT_NAME", "CLIENT_FIRST_NAME")
        c = c.replace("ADDRESS_IDENTIFICATION", "ADDRESS_ID")
        c = c.replace("GIFTREGISTRY_ID", "GIFT_REGISTRY_ID")
        c = c.replace("MARKETINGTAGS", "MARKETING_TAGS")
        c = c.replace("STATUS_RAW_VALUE_TEMPORARY", "STATUS_RAW_VALUE_TEMP")

        return c

    df.columns = [norm(c) for c in df.columns]
    return df


def traduzir_colunas(df: pd.DataFrame) -> pd.DataFrame:

    traducao_colunas = {
    "ORIGIN": "ORIGEM_PEDIDO",
    "ORDER_ID": "ID_PEDIDO",
    "SEQUENCE": "SEQUENCIA_ITEM",
    "CREATION_DATE": "DT_CRIACAO_PEDIDO",
    "CLIENT_FIRST_NAME": "NOME",
    "CLIENT_LAST_NAME": "SOBRENOME",
    "CLIENT_DOCUMENT": "CPF",
    "EMAIL": "EMAIL",
    "PHONE": "TELEFONE",
    "UF": "UF",
    "CITY": "CIDADE",
    "ADDRESS_ID": "ID_ENDERECO",
    "ADDRESS_TYPE": "TIPO_ENDERECO",
    "RECEIVER_NAME": "NOME_DESTINATARIO",
    "STREET": "LOGRADOURO",
    "NUMBER": "NUMERO_ENDERECO",
    "COMPLEMENT": "COMPLEMENTO_ENDERECO",
    "NEIGHBORHOOD": "BAIRRO",
    "REFERENCE": "REFERENCIA_ENDERECO",
    "POSTAL_CODE": "CEP",
    "SLA_TYPE": "TIPO_SLA_ENTREGA",
    "COURIER": "TRANSPORTADORA",
    "ESTIMATE_DELIVERY_DATE": "DT_PREVISTA_ENTREGA",
    "DELIVERY_DEADLINE": "DT_LIMITE_ENTREGA",
    "STATUS": "STATUS_PEDIDO",
    "LAST_CHANGE_DATE": "DT_ULTIMA_ATUALIZACAO",
    "UTM_MEDIUM": "UTM_MEDIUM",
    "UTM_SOURCE": "UTM_SOURCE",
    "UTM_CAMPAIGN": "UTM_CAMPAIGN",
    "COUPON": "CUPOM_DESCONTO",
    "PAYMENT_SYSTEM_NAME": "SISTEMA_PAGAMENTO",
    "INSTALLMENTS": "QTD_PARCELAS",
    "PAYMENT_VALUE": "VL_PAGAMENTO",
    "SKU_QUANTITY": "QTD_SKU",
    "SKU_ID": "ID_SKU",
    "CATEGORY_IDS_SKU": "IDS_CATEGORIA_SKU",
    "REFERENCE_CODE": "CODIGO_REFERENCIA",
    "SKU_NAME": "NOME_SKU",
    "SKU_VALUE": "VL_SKU",
    "SKU_SELLING_PRICE": "VL_VENDA_SKU",
    "SKU_TOTAL_PRICE": "VL_TOTAL_SKU",
    "SKU_PATH": "CAMINHO_CATEGORIA_SKU",
    "ITEM_ATTACHMENTS": "ANEXOS_ITEM",
    "LIST_ID": "ID_LISTA",
    "LIST_TYPE_NAME": "TIPO_LISTA",
    "SERVICE_PRICE_SELLING_PRICE_": "VL_SERVICO",
    "SHIPPING_LIST_PRICE": "VL_LISTA_FRETE",
    "SHIPPING_VALUE": "VL_FRETE",
    "TOTAL_VALUE": "VL_TOTAL_PEDIDO",
    "DISCOUNTS_TOTALS": "VL_TOTAL_DESCONTOS",
    "DISCOUNTS_NAMES": "NOMES_DESCONTOS",
    "CALL_CENTER_EMAIL": "EMAIL_CALL_CENTER",
    "CALL_CENTER_CODE": "CODIGO_CALL_CENTER",
    "TRACKING_NUMBER": "CODIGO_RASTREIO",
    "HOST": "HOST_ORIGEM",
    "GIFT_REGISTRY_ID": "ID_LISTA_PRESENTE",
    "SELLER_NAME": "NOME_VENDEDOR",
    "STATUS_TIME_LINE": "HISTORICO_STATUS",
    "OBS": "OBSERVACAO",
    "UTMI_PART": "UTMI_PART",
    "UTMI_CAMPAIGN": "UTMI_CAMPAIGN",
    "UTMI_PAGE": "UTMI_PAGE",
    "SELLER_ORDER_ID": "ID_PEDIDO_VENDEDOR",
    "ACQUIRER": "ADQUIRENTE",
    "AUTHORIZATION_ID": "ID_AUTORIZACAO",
    "TID": "ID_TRANSACAO_TID",
    "NSU": "NSU_TRANSACAO",
    "CARD_FIRST_DIGITS": "CARTAO_PRIMEIROS_DIGITOS",
    "CARD_LAST_DIGITS": "CARTAO_ULTIMOS_DIGITOS",
    "PAYMENT_APPROVED_BY": "APROVADO_POR",
    "CANCELLED_BY": "CANCELADO_POR",
    "CANCELLATION_REASON": "MOTIVO_CANCELAMENTO",
    "GIFT_CARD_NAME": "NOME_GIFT_CARD",
    "GIFT_CARD_CAPTION": "DESCRICAO_GIFT_CARD",
    "AUTHORIZED_DATE": "DT_AUTORIZACAO_PAGAMENTO",
    "CORPORATE_NAME": "RAZAO_SOCIAL",
    "CORPORATE_DOCUMENT": "DOCUMENTO_EMPRESA",
    "TRANSACTION_ID": "ID_TRANSACAO",
    "PAYMENT_ID": "ID_PAGAMENTO",
    "PAYMENT_ORIGIN": "ORIGEM_PAGAMENTO",
    "SALES_CHANNEL": "CANAL_VENDA",
    "MARKETING_TAGS": "TAGS_MARKETING",
    "DELIVERED": "FLAG_ENTREGUE",
    "SKU_REWARD_VALUE": "VL_RECOMPENSA_SKU",
    "IS_MARKETPLACE_CERTIFIED": "FLAG_MARKETPLACE_CERTIFICADO",
    "IS_CHECKED_IN": "FLAG_CHECKIN",
    "CURRENCY_CODE": "CODIGO_MOEDA",
    "TAXES": "VL_IMPOSTOS",
    "INVOICE_NUMBERS": "NUMEROS_NOTA_FISCAL",
    "COUNTRY": "PAIS",
    "INPUT_INVOICES_NUMBERS": "NF_ENTRADA",
    "OUTPUT_INVOICES_NUMBERS": "NF_SAIDA",
    "STATUS_RAW_VALUE_TEMP_": "STATUS_BRUTO",
    "CANCELLATION_DATA": "DT_CANCELAMENTO"
}
    
    df = df.rename(columns=traducao_colunas)

    return df

def transform_pedidos(df: pd.DataFrame) -> pd.DataFrame:
    df = aplicar_schema(df)
    df = padronizar_colunas_pedidos(df)
    df = traduzir_colunas(df)
    return df