BEGIN;
CREATE TABLE `api_resource` (`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `guid` char(32) NOT NULL UNIQUE, `callbackurl` varchar(120) NOT NULL, `callbackauth` varchar(120) NOT NULL);
CREATE TABLE `api_resourcelease` (`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `expires` datetime NOT NULL, `created` datetime NULL, `modified` datetime NOT NULL, `status` varchar(2) NOT NULL, `reminders` integer NOT NULL, `term` integer NOT NULL, `resource_id` integer NOT NULL);
CREATE TABLE `api_resourcesubscribers` (`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `resource_id` integer NOT NULL);
CREATE TABLE `api_subscriber` (`name` varchar(80) NULL, `email` varchar(80) NOT NULL PRIMARY KEY);
ALTER TABLE `api_resourcesubscribers` ADD COLUMN `subscriber_id` varchar(80) NOT NULL;
ALTER TABLE `api_resourcesubscribers` ALTER COLUMN `subscriber_id` DROP DEFAULT;
ALTER TABLE `api_resourcelease` ADD CONSTRAINT `api_resourceleas_resource_id_3fc540d6c79389a8_fk_api_resource_id` FOREIGN KEY (`resource_id`) REFERENCES `api_resource` (`id`);
ALTER TABLE `api_resourcesubscribers` ADD CONSTRAINT `api_resourcesubs_resource_id_1c8b7ab7060a572b_fk_api_resource_id` FOREIGN KEY (`resource_id`) REFERENCES `api_resource` (`id`);
CREATE INDEX `api_resourcesubscribers_9e0fe247` ON `api_resourcesubscribers` (`subscriber_id`);
ALTER TABLE `api_resourcesubscribers` ADD CONSTRAINT `api_resou_subscriber_id_6002f17b58519ed5_fk_api_subscriber_email` FOREIGN KEY (`subscriber_id`) REFERENCES `api_subscriber` (`email`);

COMMIT;
