CREATE TABLE IF NOT EXISTS app_user (
    id SERIAL PRIMARY KEY,
    username VARCHAR NOT NULL UNIQUE,
    full_name VARCHAR,
    email VARCHAR,
    hashed_password VARCHAR NOT NULL,
    disabled BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE INDEX IF NOT EXISTS ix_app_user_username ON app_user (username);
CREATE INDEX IF NOT EXISTS ix_app_user_email ON app_user (email);

CREATE TABLE IF NOT EXISTS task (
    id SERIAL PRIMARY KEY,
    title VARCHAR NOT NULL,
    description VARCHAR NOT NULL,
    owner VARCHAR NOT NULL,
    status VARCHAR NOT NULL DEFAULT 'pendente',
    comments JSON NOT NULL DEFAULT '[]',
    CONSTRAINT ck_task_status CHECK (status IN ('pendente', 'fazendo', 'concluido'))
);

CREATE INDEX IF NOT EXISTS ix_task_owner ON task (owner);
CREATE INDEX IF NOT EXISTS ix_task_status ON task (status);

INSERT INTO app_user (
    username,
    full_name,
    email,
    hashed_password,
    disabled
) VALUES (
    'admin',
    'Administrador',
    'admin@example.com',
    '$argon2id$v=19$m=65536,t=3,p=4$xMAjJNH/OaJHia+5E0xatw$dNndWKB/ryf07wsnSy84frcdYRGA0J20g0CiLqxWGqU',
    FALSE
) ON CONFLICT (username) DO NOTHING;

INSERT INTO task (id, title, description, owner, status, comments) VALUES
    (1, 'um titulo da minha primeira task', 'uma descricao da minha primeira task', 'Joao', 'pendente', '["asdasdas", "sdfsdfsdfsdf", "asdasd6556"]'),
    (2, 'um titulo da minha segunda task', 'uma descricao da minha segunda task', 'Joao', 'pendente', '["asdasdas", "sdfsdfsdfsdf", "asdasd6556"]'),
    (4, 'um titulo da minha quarta task', 'uma descricao da minha quarta task', 'Pedro', 'concluido', '["comment1"]'),
    (5, 'um titulo da minha quinta task', 'uma descricao da minha quinta task', 'Ana', 'fazendo', '[]'),
    (6, 'um titulo da minha sexta task', 'uma descricao da minha sexta task', 'Carlos', 'pendente', '["comment1", "comment2", "comment3"]'),
    (7, 'um titulo da minha setima task', 'uma descricao da minha setima task', 'Joao', 'concluido', '["comment1"]'),
    (8, 'um titulo da minha oitava task', 'uma descricao da minha oitava task', 'Rafael', 'fazendo', '["comment1", "comment2"]'),
    (9, 'um titulo da minha nona task', 'uma descricao da minha nona task', 'Lucas', 'pendente', '[]'),
    (10, 'um titulo da minha decima task', 'uma descricao da minha decima task', 'Marina', 'concluido', '["comment1", "comment2", "comment3", "comment4"]'),
    (11, 'um titulo da minha decima primeira task', 'uma descricao da minha decima primeira task', 'Beatriz', 'fazendo', '["comment1"]'),
    (12, 'um titulo da minha decima segunda task', 'uma descricao da minha decima segunda task', 'Felipe', 'pendente', '["comment1", "comment2"]')
ON CONFLICT (id) DO NOTHING;

SELECT setval('task_id_seq', COALESCE((SELECT MAX(id) FROM task), 1), true);
SELECT setval('app_user_id_seq', COALESCE((SELECT MAX(id) FROM app_user), 1), true);
