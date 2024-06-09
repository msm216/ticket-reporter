CREATE TABLE `task` (
  `id` varchar2 PRIMARY KEY,
  `execute_on` datetime NOT NULL,
  `ticket_id` varchar2 NOT NULL,
  `description` text,
  `effort_hour` integer
);

CREATE TABLE `ticket` (
  `id` varchar2 PRIMARY KEY,
  `title` varchar(255) UNIQUE,
  `report_on` datetime NOT NULL,
  `project_id` varchar2,
  `description` text,
  `update_on` datetime
);

CREATE TABLE `project` (
  `id` varchar2 PRIMARY KEY,
  `title` varchar2 UNIQUE,
  `create_on` datetime NOT NULL,
  `charger_amount` integer,
  `latitude` float,
  `longitude` float
);

ALTER TABLE `task` ADD FOREIGN KEY (`ticket_id`) REFERENCES `ticket` (`id`);

ALTER TABLE `ticket` ADD FOREIGN KEY (`project_id`) REFERENCES `project` (`id`);
