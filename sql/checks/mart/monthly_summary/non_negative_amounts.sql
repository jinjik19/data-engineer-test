SELECT count() AS bad_rows
FROM mart.monthly_summary
WHERE deposit_amount_usd < 0
   OR withdrawal_amount_usd < 0
   OR bet_amount_usd < 0;