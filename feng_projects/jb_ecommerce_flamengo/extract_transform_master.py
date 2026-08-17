import pandas as pd


# -----------------------------
# EXTRACT
# -----------------------------
def extract_master(local_arquivo: str) -> pd.DataFrame:
    dtype_map = {
        "homePhone": "string",
        "phone": "string",
        "tradeName": "string",
        "stateRegistration": "string",
        "isNewsletterOptIn": "string",
        "businessPhone": "string",
        "corporateDocument": "string",
        "corporateName": "string",
    }

    df_master = pd.read_csv(
        local_arquivo,
        sep=";",
        dtype=dtype_map,
        low_memory=False,
    )

    return df_master


# -----------------------------
# TRANSFORM (PADRÃO COLUNAS)
# -----------------------------
def padronizar_colunas(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = (
        df.columns
        .str.strip()
        .str.replace(r"([a-z0-9])([A-Z])", r"\1_\2", regex=True)   # camelCase -> snake
        .str.replace(r"[\s\-]+", "_", regex=True)                 # espaço/hífen -> _
        .str.replace(r"[^A-Za-z0-9_]", "", regex=True)            # remove especiais
        .str.upper()
    )
    return df


# -----------------------------
# TRANSFORM (SCHEMA + CONVERSÕES)
# -----------------------------
TIPOS_CUSTOMER = {
    # strings
    "email": "string",
    "firstName": "string",
    "lastName": "string",
    "phone": "string",
    "homePhone": "string",
    "businessPhone": "string",
    "tradeName": "string",
    "stateRegistration": "string",
    "userId": "string",
    "document": "string",
    "localeDefault": "string",
    "attach": "string",
    "carttag": "string",
    "checkouttag": "string",
    "corporateDocument": "string",
    "corporateName": "string",
    "documentType": "string",
    "gender": "string",
    "visitedProductWithStockOutSkusTag": "string",
    "customerClass": "string",
    "priceTables": "string",
    "profilePicture": "string",
    "restrictions": "string",
    "tradePolicy": "string",
    "id": "string",
    "accountId": "string",
    "accountName": "string",
    "dataEntityId": "string",
    "createdBy": "string",
    "updatedBy": "string",
    "lastInteractionBy": "string",
    "tags": "string",
    "auto_filter": "string",
    "brandPurchasedTag": "string",
    "brandVisitedTag": "string",
    "categoryPurchasedTag": "string",
    "categoryVisitedTag": "string",
    "departmentVisitedTag": "string",
    "productPurchasedTag": "string",
    "productVisitedTag": "string",

    # números
    "rclastcartvalue": "Float64",
    "followers": "Int64",
    "birthDateMonth": "Int64",

    # booleanos
    "isCorporate": "boolean",
    "isNewsletterOptIn": "boolean",
    "approved": "boolean",

    # datas
    "birthDate": "datetime64[ns]",
    "rclastsessiondate": "datetime64[ns]",
    "createdIn": "datetime64[ns]",
    "updatedIn": "datetime64[ns]",
    "lastInteractionIn": "datetime64[ns]",
}

DT_COLS_C = [c for c, t in TIPOS_CUSTOMER.items() if t.startswith("datetime")]
INT_COLS_C = [c for c, t in TIPOS_CUSTOMER.items() if t == "Int64"]
FLOAT_COLS_C = [c for c, t in TIPOS_CUSTOMER.items() if t == "Float64"]
BOOL_COLS_C = [c for c, t in TIPOS_CUSTOMER.items() if t == "boolean"]
STR_COLS_C = [c for c, t in TIPOS_CUSTOMER.items() if t == "string"]


def to_str(s: pd.Series) -> pd.Series:
    s = s.astype("string[python]").str.strip()
    s = s.replace({"": pd.NA, "NA": pd.NA, "NaN": pd.NA, "None": pd.NA})
    return s.str.upper()


def to_datetime(s: pd.Series) -> pd.Series:
    s = s.astype("string").str.strip()
    dt = pd.to_datetime(s, errors="coerce", utc=True).dt.tz_convert(None).dt.floor("ms")
    return dt.dt.strftime("%Y-%m-%d %H:%M:%S.%f").str.slice(0, 23)  # yyyy-mm-dd hh:mm:ss.fff  # datetime sem timezone e sem fração


def to_number_str(s: pd.Series) -> pd.Series:
    s = s.astype("string[python]").str.strip()
    s = s.replace({"": pd.NA, "NA": pd.NA, "NaN": pd.NA, "None": pd.NA})
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


def aplicar_schema_master(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [c.strip() for c in df.columns]

    for c in STR_COLS_C:
        if c in df.columns:
            df[c] = to_str(df[c])

    for c in DT_COLS_C:
        if c in df.columns:
            df[c] = to_datetime(df[c])

    for c in FLOAT_COLS_C:
        if c in df.columns:
            df[c] = to_float(df[c])

    for c in INT_COLS_C:
        if c in df.columns:
            df[c] = to_int(df[c])

    for c in BOOL_COLS_C:
        if c in df.columns:
            df[c] = to_bool(df[c])

    return df


def traduzir_colunas(df: pd.DataFrame) -> pd.DataFrame:

    traducao_colunas = {
    "EMAIL": "EMAIL",
    "FIRST_NAME": "NOME",
    "LAST_NAME": "SOBRENOME",
    "PHONE": "TELEFONE",
    "HOME_PHONE": "TELEFONE_RESIDENCIAL",
    "BUSINESS_PHONE": "TELEFONE_COMERCIAL",

    "DOCUMENT": "CPF",
    "DOCUMENT_TYPE": "TIPO_DOCUMENTO",
    "CORPORATE_DOCUMENT": "CNPJ",
    "STATE_REGISTRATION": "INSCRICAO_ESTADUAL",

    "IS_CORPORATE": "FLAG_EMPRESA",
    "CORPORATE_NAME": "RAZAO_SOCIAL",
    "TRADE_NAME": "NOME_FANTASIA",

    "USER_ID": "ID_USUARIO",
    "ID": "ID",
    "ACCOUNT_ID": "ID_CONTA",
    "ACCOUNT_NAME": "NOME_CONTA",
    "DATA_ENTITY_ID": "ID_ENTIDADE_DADOS",

    "IS_NEWSLETTER_OPT_IN": "FLAG_NEWSLETTER",
    "APPROVED": "APROVADO",
    "CUSTOMER_CLASS": "CLASSE_CLIENTE",
    "PRICE_TABLES": "TABELAS_PRECO",
    "TRADE_POLICY": "POLITICA_COMERCIAL",
    "RESTRICTIONS": "RESTRICOES",

    "BIRTH_DATE": "DATA_NASCIMENTO",
    "BIRTH_DATE_MONTH": "MES_NASCIMENTO",
    "GENDER": "SEXO",

    "PROFILE_PICTURE": "FOTO_PERFIL",
    "LOCALE_DEFAULT": "LOCALE_PADRAO",
    "ATTACH": "ANEXO",

    "RCLASTCART": "ID_ULTIMO_CARRINHO",
    "RCLASTCARTVALUE": "VALOR_ULTIMO_CARRINHO",
    "RCLASTSESSION": "ID_ULTIMA_SESSAO",
    "RCLASTSESSIONDATE": "DATA_ULTIMA_SESSAO",

    "BRAND_PURCHASED_TAG": "TAG_MARCA_COMPRADA",
    "BRAND_VISITED_TAG": "TAG_MARCA_VISITADA",
    "CATEGORY_PURCHASED_TAG": "TAG_CATEGORIA_COMPRADA",
    "CATEGORY_VISITED_TAG": "TAG_CATEGORIA_VISITADA",
    "DEPARTMENT_VISITED_TAG": "TAG_DEPARTAMENTO_VISITADO",
    "PRODUCT_PURCHASED_TAG": "TAG_PRODUTO_COMPRADO",
    "PRODUCT_VISITED_TAG": "TAG_PRODUTO_VISITADO",
    "VISITED_PRODUCT_WITH_STOCK_OUT_SKUS_TAG": "TAG_PRODUTO_VISITADO_SEM_ESTOQUE",

    "CARTTAG": "TAG_CARRINHO",
    "CHECKOUTTAG": "TAG_CHECKOUT",
    "TAGS": "TAGS",
    "AUTO_FILTER": "FILTRO_AUTOMATICO",

    "CREATED_BY": "CRIADO_POR",
    "CREATED_IN": "DATA_CRIACAO",
    "UPDATED_BY": "ATUALIZADO_POR",
    "UPDATED_IN": "DATA_ATUALIZACAO",
    "LAST_INTERACTION_BY": "ULTIMA_INTERACAO_POR",
    "LAST_INTERACTION_IN": "DATA_ULTIMA_INTERACAO",

    "FOLLOWERS": "SEGUIDORES"
}
    
    df = df.rename(columns=traducao_colunas)

    return df


def transform_master(df_master: pd.DataFrame) -> pd.DataFrame:
    df_master = df_master.copy()

    df_master = aplicar_schema_master(df_master)
    df_master = padronizar_colunas(df_master)
    df_master = traduzir_colunas(df_master)

    return df_master