-- Cliente
INSERT INTO clients (dni, full_name, email)
VALUES ('0929668846', 'Jesus Jacome', 'olmedo.bdp@gmail.com')
ON DUPLICATE KEY UPDATE full_name = VALUES(full_name), email = VALUES(email);

SET @cid := (SELECT id FROM clients WHERE dni = '0929668846');

-- Línea
INSERT INTO phone_lines (client_id, phone_number, product_type)
VALUES (@cid, '0969786985', 'MOVIL')
ON DUPLICATE KEY UPDATE client_id = VALUES(client_id);

SET @lid := (SELECT id FROM phone_lines WHERE phone_number = '0969786985');

-- Desactivar plan activo previo (si lo hubiera)
UPDATE data_plans SET is_active = 0 WHERE line_id = @lid AND is_active = 1;

-- Nuevo plan (30 GB por 30 días)
INSERT INTO data_plans (line_id, limit_bytes, used_bytes, start_at, expiration_at, is_active)
VALUES (@lid, 32212254720, 0, NOW(), DATE_ADD(NOW(), INTERVAL 30 DAY), 1);

SET @pid := LAST_INSERT_ID();

-- Acumuladores (1MB social, 2MB entretenimiento, 0 system, 512KB navegación)
INSERT INTO data_usage_accumulators (
  plan_id, used_social_bytes, used_entertainment_bytes, used_system_updates_bytes, used_navigation_search_bytes
)
VALUES (@pid, 1048576, 2097152, 0, 524288)
ON DUPLICATE KEY UPDATE
  used_social_bytes = VALUES(used_social_bytes),
  used_entertainment_bytes = VALUES(used_entertainment_bytes),
  used_system_updates_bytes = VALUES(used_system_updates_bytes),
  used_navigation_search_bytes = VALUES(used_navigation_search_bytes);
