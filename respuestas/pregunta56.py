import pandas as pd

# load csv's
df_bansur = pd.read_csv('BANSUR.csv', dtype={
    'TARJETA': object,
    'ID_ADQUIRIENTE': object,
    'TIPO_TRX': object,
    'CODIGO_AUTORIZACION': object
})
df_bansur["FECHA_TRANSACCION"] = pd.to_datetime(
    df_bansur["FECHA_TRANSACCION"], format="%Y%m%d"
).dt.date
df_bansur["FECHA_RECEPCION"] = pd.to_datetime(
    df_bansur["FECHA_RECEPCION"]
).dt.date


df_clap = pd.read_csv('CLAP.csv', dtype={
    'INICIO6_TARJETA': object,
    'FINAL4_TARJETA': object,
    'TIPO_TRX': object,
    'CODIGO_AUTORIZACION': object,
    'ID_BANCO': object})
df_clap["FECHA_TRANSACCION"] = pd.to_datetime(df_clap["FECHA_TRANSACCION"])
df_clap["FECHA_RECEPCION_BANCO"] = pd.to_datetime(
    df_clap["FECHA_RECEPCION_BANCO"]
).dt.date
df_clap = df_clap.rename(columns={'FECHA_TRANSACCION': 'FECHA_TRANSACCION_CLAP',
                                  'MONTO': 'MONTO_CLAP',
                                  'TIPO_TRX': 'TIPO_TRX_CLAP',
                                  'CODIGO_AUTORIZACION': 'CODIGO_AUTORIZACION_CLAP'
                                  })

df = pd.merge(df_clap, df_bansur, left_on='ID_BANCO',
              right_on='ID_ADQUIRIENTE')

df = df[
    (df["INICIO6_TARJETA"] == df["TARJETA"].str.slice(start=0, stop=6)) &
    (df["FINAL4_TARJETA"] == df["TARJETA"].str.slice(start=6)) &
    (abs(df["MONTO"] - df["MONTO_CLAP"]) <= 0.99) &
    (df["FECHA_TRANSACCION"] == df["FECHA_TRANSACCION_CLAP"].dt.date)
]

count_clap = df_clap.shape[0]
count_cross = df.shape[0]
count_bansur = df_bansur.shape[0]


print("Porcentaje de transacciones de la base conciliable de CLAP cruzó contra la liquidación de BANSUR",
      (count_cross/count_clap)*100)

print("porcentaje de transacciones de la base conciliable de BANSUR no cruzó contra la liquidación de CLAP",
      ((count_bansur-count_cross)/count_bansur)*100)
