Table player {
  id int [pk]
  name varchar
}

Table player_address_mapping {

  player_id int [ref: - player.id]
  address_id int [ref: - address.id]

  indexes {
    (player_id) [unique]
    (address_id) [unique]
  }
}

Table address {
  id int [pk]
  code int
}

Table food_buff {
  id int [pk]
  name varchar
  ingredient_pts int
  effect varchar
  level_1_val int
  level_2_val int
  level_3_val int
  level_4_val int
  level_5_val int
  level_6_val int
  level_7_val int
  level_8_val int
  level_9_val int
  level_10_val int
  thumbnail_path varchar
}

Table player_food_buff_mapping {
  
  player_id int [ref: <> player.id]
  food_buff_id int [ref: <> food_buff.id]

  indexes {
    (player_id, food_buff_id) [pk]
  }
}

# TODO
- CONVERT ALL OF THIS INTO SCHEMA