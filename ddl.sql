CREATE TABLE IF NOT EXISTS measures (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    value REAL NOT NULL,
    measure_type TEXT NOT NULL,
    detail TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (id)
);

CREATE TABLE IF NOT EXISTS alarms (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    measure_value INTEGER NOT NULL,
    config_value REAL NOT NULL,
    measure_type TEXT NOT NULL,
    alarm_type TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (id)
);

CREATE TABLE IF NOT EXISTS alarm_definitions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    config_value REAL NOT NULL,
    alarm_type TEXT NOT NULL,
    measure_type TEXT NOT NULL,
    sound_path TEXT NOT NULL,
    created_at DATETIME NOT NULL,
    updated_at DATETIME,
    enabled BOOLEAN,
    UNIQUE (alarm_type, measure_type)
);

CREATE TABLE IF NOT EXISTS configurations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    value TEXT NOT NULL,
    treatment_as TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (name)
);

CREATE TABLE IF NOT EXISTS step_definitions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    position TEXT NOT NULL,
    duration INTEGER NOT NULL,
    period INTEGER NOT NULL,
    lead INTEGER NOT NULL,
    sensor_type TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (id, position)
);

CREATE TABLE IF NOT EXISTS sensors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    brand TEXT NOT NULL,
    reference TEXT NOT NULL,
    sensor_type TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS measurement_specs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    unit TEXT NOT NULL,
    measure_type TEXT NOT NULL,
    sensor_id INTEGER NOT NULL,
    FOREIGN KEY (sensor_id) REFERENCES sensors(id) ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS worker_flow_status (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    times_executed INTEGER NOT NULL,
    position TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    measure_type TEXT,
    alarm_type TEXT
);

INSERT INTO configurations (name, value, treatment_as)
VALUES
('DEVICE_IP', 'https://eb53b229-f0e4-42da-9957-a7df9990fe9c.mock.pstmn.io', 'STRING'),
('isolationVoltage', '500', 'STRING'),
('soundPath', 'for_emit_sound', 'STRING');

INSERT INTO step_definitions (position,duration,period,lead, sensor_type)
values 
('FIRST',1,25,1,'RES'),
('SECOND',1,25,1,'ISO'),
('THIRD',1,25,1,'WELL');

INSERT INTO worker_flow_status (times_executed,"position") VALUES
(1,'FIRST');