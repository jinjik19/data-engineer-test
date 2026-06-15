WITH all_operations AS (
	SELECT
        deposit_date AS operation_date,
        player_id,
        amount,
        currency,
        'deposit' AS operation_type
    FROM staging.deposits

	UNION ALL
	
    SELECT
        withdrawal_date AS operation_date,
        player_id,
        amount,
        currency,
        'withdrawal' AS operation_type
    FROM staging.withdrawals

	UNION ALL
	
    SELECT
        game_date AS operation_date,
        player_id,
        amount,
        currency,
        'bet' AS operation_type
    FROM staging.games
), operations_enriched AS (
	SELECT
        toStartOfMonth(o.operation_date) AS month,
        p.country AS country,
        o.operation_type AS operation_type,
        divideDecimal(
		    toDecimal256(o.amount, 8),
		    toDecimal256(cr.rate_to_usd, 8),
		    8
		) AS amount_usd
    FROM all_operations o
    INNER JOIN staging.players p ON p.id = o.player_id
    INNER JOIN staging.currency_rates cr
       ON cr.date = o.operation_date
       AND cr.currency = o.currency
)
INSERT INTO mart.monthly_summary
SELECT
	month,
	country,
	CAST(
		ROUND(sumIf(amount_usd, operation_type = 'deposit'), 2),
		'Decimal(12, 2)'
	) AS deposit_amount_usd,
	CAST(
		ROUND(sumIf(amount_usd, operation_type = 'withdrawal'), 2),
		'Decimal(12, 2)'
	) AS withdrawal_amount_usd,
	CAST(
		ROUND(sumIf(amount_usd, operation_type = 'bet'), 2),
		'Decimal(12, 2)'
	) AS bet_amount_usd
FROM operations_enriched
GROUP BY month, country
ORDER BY month, country