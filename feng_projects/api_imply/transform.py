import pandas as pd

# Tratamento de tipos e padronização de colunas para o schema alvo
def to_string(df: pd.DataFrame, col: str, upper: bool = False) -> None:
    if col in df.columns:
        s = df[col].astype("string")
        s = s.str.strip()
        if upper:
            s = s.str.upper()
        df[col] = s

def to_float(df: pd.DataFrame, col: str) -> None:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce").astype("float64")

def to_int_nullable(df: pd.DataFrame, col: str) -> None:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce").astype("Int64")

def to_bool(df: pd.DataFrame, col: str) -> None:
    if col in df.columns:
        s = df[col]
        # trata casos comuns: True/False, 1/0, 'S'/'N'
        if s.dtype == object or str(s.dtype).startswith(("string", "category")):
            s = s.astype("string").str.strip().str.upper()
            df[col] = s.map({
                "S": True, "N": False,
                "TRUE": True, "FALSE": False,
                "1": True, "0": False
            })
        df[col] = df[col].astype("boolean")


def transform_df(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # padroniza nomes
    df.columns = df.columns.astype(str).str.strip().str.upper()

    # renomeia para o schema alvo
    rename_map = {
        "TITULO": "CAMPEONATO",
        "DSCAPRESENTACAO": "PARTIDA",
        "DSCINTERNA": "TIPO_INGRESSO",
        "DSCTIPOPRODUTO": "TIPO_PRODUTO",
    }
    df = df.rename(columns=rename_map)

    # normaliza vazios
    df = df.replace({"": None})

    # VARCHAR / STRING
    for c in [
        "IDEVENTO","CAMPEONATO","IDAPRESENTACAO","PARTIDA","NOME","CPF","EMAIL","CELULAR","TELEFONE",
        "DSCPESSOA_TIPO","CODIGO","TIPO_INGRESSO","TIPO_PRODUTO","LOCALIZADOR_ITEM","STATUS","DSCFORMAPAG",
        "LOCALIZADOR","DSCEQUIPAMENTO","PORTADOR_NOME","PORTADOR_DOCUMENTO","TIPO_INGRESSO_BASE","SETOR_INGRESSO",
        "FLAG_ACOMPANHANTE","SEXO","END_ESTADO","ESTADO_CIVIL","IDACESSO","REGIAO","ESTADIO"
    ]:
        to_string(df, c, upper=True)

    # DOUBLE
    for c in [
        "VALOR","VALOR_JUROS","VALOR_TAXA","VALOR_DESCONTO","VALOR_CANCELADO","VALOR_PAGO","VALOR_TOTAL"
    ]:
        to_float(df, c)

    # NUMBER(38,0) -> inteiro anulável
    for c in ["CARTAO","LOCALIZADOR_BLOCO","LOCALIZADOR_FILA","LOCALIZADOR_LUGAR", "USER_BEPASS"]:
        to_int_nullable(df, c)

    # BOOLEAN
    for c in ["ACESSO_ENTROU"]:
        to_bool(df, c)




    return df
