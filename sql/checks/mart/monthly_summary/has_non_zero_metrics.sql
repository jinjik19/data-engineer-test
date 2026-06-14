SELECT if(
    sum(deposit_amount_usd) = 0
    AND sum(withdrawal_amount_usd) = 0
    AND sum(bet_amount_usd) = 0,
    1,
    0
) AS bad_rows
FROM mart.monthly_summary;