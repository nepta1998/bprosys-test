-- 1. Escriba el código de SQL que le permite conocer el monto y la cantidad de las transacciones que SIMETRIK considera como conciliables para la base de CLAP

select sum(monto), count(id) from (
	SELECT 
	clap."ID_BANCO" as id, 
	clap."MONTO" as monto, 
	MAX(clap."FECHA_TRANSACCION") AS last_date
	from clap WHERE 
	upper(clap."TIPO_TRX")='PAGADA'
	group by 
	clap."ID_BANCO", 
	clap."MONTO"
) s;


