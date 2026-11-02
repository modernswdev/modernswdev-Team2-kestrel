INSERT INTO users (email, username, password_hash)
VALUES
  ('test@test.com', 'test', 'pbkdf2:sha256:50000$TCI4GzcX$0de171a4f4dac32e3364c7ddc7c14f3e2fa61f2d17574483f7ffbb431b4acb2f'),
  ('other@other.com', 'other', 'pbkdf2:sha256:50000$kJPKsz6N$d2d4784f1b030a9761f5ccaeeaca413f27f2ecb76d6168407af962ddce849f79');

INSERT INTO dogs (owner_id, name, age, sex, zip_code, size, energy_level, temperament)
VALUES
  (1, 'Buddy', 3, 'Male', '72204', 3, 4, 4),
  (2, 'Max', 5, 'Male', '72032', 4, 5, 4),
  (1, 'Bella', 2, 'Female', '72204', 2, 3, 3),
  (2, 'Charlie', 4, 'Male', '72103', 3, 4, 5),
  (1, 'Lucy', 1, 'Female', '72204', 2, 1, 1);