CREATE TABLE IF NOT EXISTS player (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50)
);


CREATE TABLE IF NOT EXISTS address (
  id SERIAL PRIMARY KEY,
  code VARCHAR(20)
    --   probably add wards columns here soon with enough data
);


CREATE TABLE IF NOT EXISTS player_address_mapping (

  player_id SERIAL REFERENCES player (id) UNIQUE,
  address_id SERIAL REFERENCES address (id) UNIQUE

);


CREATE TABLE IF NOT EXISTS food_buff (
  id SMALLSERIAL PRIMARY KEY,
  name VARCHAR(50),
  ingredient_pts SMALLINT,
  effect VARCHAR(50),
  level_1_val SMALLINT,
  level_2_val SMALLINT,
  level_3_val SMALLINT,
  level_4_val SMALLINT,
  level_5_val SMALLINT,
  level_6_val SMALLINT,
  level_7_val SMALLINT,
  level_8_val SMALLINT,
  level_9_val SMALLINT,
  level_10_val SMALLINT,
  thumbnail_path VARCHAR(100)

);


CREATE TABLE IF NOT EXISTS player_food_buff_mapping (
  
  player_id SERIAL REFERENCES player (id),
  food_buff_id SERIAL REFERENCES food_buff (id),

  PRIMARY KEY (player_id, food_buff_id)
);


