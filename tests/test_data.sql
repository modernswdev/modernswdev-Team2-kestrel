INSERT INTO users (email, name, password_hash)
VALUES
  ('test@test.com', 'Daniel Cronin', 'pbkdf2:sha256:50000$TCI4GzcX$0de171a4f4dac32e3364c7ddc7c14f3e2fa61f2d17574483f7ffbb431b4acb2f'),
  ('other@other.com', 'John Doe', 'pbkdf2:sha256:50000$kJPKsz6N$d2d4784f1b030a9761f5ccaeeaca413f27f2ecb76d6168407af962ddce849f79');

INSERT INTO dogs (owner_id, name, age, sex, size, energy_level, temperament)
VALUES
  (1, 'Buddy', 3, 'Male', 'Medium', 'High', 'Friendly'),
  (2, 'Max', 5, 'Male', 'Large', 'Very High', 'Playful'),
  (1, 'Bella', 2, 'Female', 'Small', 'Medium', 'Calm'),
  (2, 'Charlie', 4, 'Male', 'Medium', 'High', 'Energetic'),
  (1, 'Lucy', 1, 'Female', 'Small', 'Low', 'Shy');