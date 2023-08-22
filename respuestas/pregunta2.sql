-- 2. Escriba el código de SQL que le permite conocer el monto y la cantidad de las transacciones que SIMETRIK considera como conciliables para la base de BANSUR

select sum(monto), count(id) from (
	SELECT 
	bansur."ID_ADQUIRIENTE" as id, 
	bansur."MONTO" as monto, 
	MAX(bansur."FECHA_TRANSACCION") AS last_date
	from bansur WHERE 
	upper(bansur."TIPO_TRX")='PAGO'
	group by 
	bansur."ID_ADQUIRIENTE", 
	bansur."MONTO"
) s;
