SET client_encoding = 'UTF8';

DO $$
DECLARE 
data_path varchar := 'D:/John Mark/Projects/personal_messenger_bot/plugins/toram/static/';

BEGIN
-- food_buff table
CREATE TABLE IF NOT EXISTS temp_food_buff 
    (LIKE food_buff INCLUDING DEFAULTS);


EXECUTE 'COPY temp_food_buff FROM ''' || data_path || 'food_buff.csv'' DELIMITER '','' CSV HEADER';


INSERT INTO food_buff 
SELECT *
FROM temp_food_buff
ON CONFLICT (id)
DO NOTHING;

DROP TABLE IF EXISTS temp_food_buff;


END $$;
