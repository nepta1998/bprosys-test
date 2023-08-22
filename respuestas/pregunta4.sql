-- 4. Teniendo en cuenta los criterios de cruce entre ambas bases conciliables, escriba una sentencia de SQL que contenga la información de CLAP y BANSUR; agregue una columna en la que se evidencie si la transacción cruzó o no con su contrapartida y una columna en la que se inserte un ID autoincremental para el control de la conciliación

SELECT row_number() OVER (ORDER BY bansur."FECHA_TRANSACCION", clap."FECHA_TRANSACCION") id, 
CASE
    WHEN 
	clap."ID_BANCO" = bansur."ID_ADQUIRIENTE" and
	clap."INICIO6_TARJETA" = substring(bansur."TARJETA",1,6) and
	clap."FINAL4_TARJETA" = substring(bansur."TARJETA",7) and
	ABS (clap."MONTO" - bansur."MONTO") <= 0.99  and
	DATE(clap."FECHA_TRANSACCION") = bansur."FECHA_TRANSACCION" 
	THEN true
    ELSE false
END AS transaction_cross, *
FROM clap, bansur WHERE clap."ID_BANCO" = bansur."ID_ADQUIRIENTE";
