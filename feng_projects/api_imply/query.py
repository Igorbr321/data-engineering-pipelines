from sqlalchemy import text

DIM_PARTIDA_TABLE = "DW_STG_MKT.GOLD.DIM_PARTIDA_FORM"
FT_COMPRAINGRESSO_TABLE = "DW_STG_MKT.GOLD.FT_COMPRAINGRESSO_IMPLY"

SQL_UPSERT_DIM_PARTIDA = text(f"""
        INSERT INTO {DIM_PARTIDA_TABLE}
        SELECT DISTINCT
                idapresentacao,
                campeonato,
                partida,
                dthr_apresentacao
        FROM {FT_COMPRAINGRESSO_TABLE}
        WHERE idapresentacao NOT IN (
        SELECT DISTINCT idapresentacao
        FROM {DIM_PARTIDA_TABLE}
)
        AND campeonato NOT ILIKE '%tour da%'
        AND campeonato NOT ILIKE '%estacionamento%';
""")