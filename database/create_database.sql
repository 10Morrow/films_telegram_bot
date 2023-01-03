create table if not exists films
(
    film_id bigint UNIQUE,
    film_photo_id text,
    film_name text,
    film_link text
);
create table if not exists moderators
(
    moderator_id bigint
);

create table if not exists bot_users
(
    user_id bigint UNIQUE,
    subscribe bool default FALSE
);



