drop table if exists english_words_and_meanings;
create table english_words_and_meanings (
  id integer primary key autoincrement,
  word string not null,
  meaning string not null
);