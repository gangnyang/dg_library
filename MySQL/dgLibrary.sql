CREATE TABLE `books` (
  `id` int PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `author` varchar(100) NOT NULL,
  `title` varchar(255) NOT NULL,
  `publicate_year` varchar(255) DEFAULT null,
  `regist_day` datetime DEFAULT null,
  `status` ENUM ('available', 'borrowed') DEFAULT null,
  `borrowed` int DEFAULT '0',
  `isbn` varchar(20) DEFAULT null,
  `interloaned_from_external` tinyint(1) DEFAULT '0',
  `return_due_external` date DEFAULT null,
  `external_book_id` int DEFAULT null,
  `image` varchar(255)
);

CREATE TABLE `comments` (
  `id` int PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `book_id` int NOT NULL,
  `user_id` int NOT NULL,
  `parent_id` int NOT NULL,
  `context` text,
  `created` timestamp DEFAULT (CURRENT_TIMESTAMP),
  `updated` timestamp DEFAULT (CURRENT_TIMESTAMP)
);

CREATE TABLE `external_books` (
  `id` int PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `author` varchar(100) NOT NULL,
  `title` varchar(255) NOT NULL,
  `publicate_year` varchar(100) DEFAULT null,
  `regist_day` datetime DEFAULT null,
  `status` ENUM ('available', 'borrowed') DEFAULT null,
  `isbn` varchar(20) DEFAULT null
);

CREATE TABLE `interloan` (
  `id` int PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `external_book_id` int NOT NULL,
  `request_date` timestamp DEFAULT (CURRENT_TIMESTAMP),
  `status` ENUM ('request', 'progress', 'complete') DEFAULT null
);

CREATE TABLE `librarians` (
  `id` int PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `librarian_name` varchar(10) NOT NULL,
  `work_details` varchar(30) DEFAULT null,
  `hire_date` date DEFAULT null
);

CREATE TABLE `loan` (
  `id` int PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `book_id` int NOT NULL,
  `loan_date` date DEFAULT null,
  `will_return_date` date DEFAULT null,
  `returned_date` date DEFAULT null,
  `overdue` tinyint(1) DEFAULT '0',
  `status` ENUM ('progress', 'returned', 'overdue') DEFAULT null
);

CREATE TABLE `program_librarians` (
  `id` int PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `program_id` int NOT NULL,
  `librarian_id` int NOT NULL
);

CREATE TABLE `program_participants` (
  `id` int PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `program_id` int NOT NULL,
  `user_id` int NOT NULL,
  `joined` datetime DEFAULT null
);

CREATE TABLE `programs` (
  `id` int PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `description` text,
  `event_date` datetime DEFAULT null,
  `participants` int DEFAULT null
);

CREATE TABLE `users` (
  `id` int PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `name` varchar(30) NOT NULL,
  `username` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL,
  `phone` varchar(15) DEFAULT null,
  `role` ENUM ('user', 'root') DEFAULT 'user',
  `created` timestamp DEFAULT (CURRENT_TIMESTAMP)
);

CREATE UNIQUE INDEX `isbn` ON `books` (`isbn`);

CREATE INDEX `external_book_id` ON `books` (`external_book_id`);

CREATE INDEX `book_id` ON `comments` (`book_id`);

CREATE INDEX `user_id` ON `comments` (`user_id`);

CREATE UNIQUE INDEX `isbn` ON `external_books` (`isbn`);

CREATE INDEX `user_id` ON `interloan` (`user_id`);

CREATE INDEX `external_book_id` ON `interloan` (`external_book_id`);

CREATE INDEX `user_id` ON `loan` (`user_id`);

CREATE INDEX `book_id` ON `loan` (`book_id`);

CREATE INDEX `program_id` ON `program_librarians` (`program_id`);

CREATE INDEX `librarian_id` ON `program_librarians` (`librarian_id`);

CREATE INDEX `program_id` ON `program_participants` (`program_id`);

CREATE INDEX `user_id` ON `program_participants` (`user_id`);

ALTER TABLE `comments` ADD CONSTRAINT `comments_ibfk_1` FOREIGN KEY (`book_id`) REFERENCES `books` (`id`);

ALTER TABLE `comments` ADD CONSTRAINT `comments_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

ALTER TABLE `comments` ADD CONSTRAINT `comments_ibfk_3` FOREIGN KEY (`parent_id`) REFERENCES `comments` (`id`);

ALTER TABLE `interloan` ADD CONSTRAINT `interloan_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

ALTER TABLE `interloan` ADD CONSTRAINT `interloan_ibfk_2` FOREIGN KEY (`external_book_id`) REFERENCES `external_books` (`id`);

ALTER TABLE `loan` ADD CONSTRAINT `loan_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

ALTER TABLE `loan` ADD CONSTRAINT `loan_ibfk_2` FOREIGN KEY (`book_id`) REFERENCES `books` (`id`);

ALTER TABLE `program_librarians` ADD CONSTRAINT `program_librarians_ibfk_1` FOREIGN KEY (`program_id`) REFERENCES `programs` (`id`);

ALTER TABLE `program_librarians` ADD CONSTRAINT `program_librarians_ibfk_2` FOREIGN KEY (`librarian_id`) REFERENCES `librarians` (`id`);

ALTER TABLE `program_participants` ADD CONSTRAINT `program_participants_ibfk_1` FOREIGN KEY (`program_id`) REFERENCES `programs` (`id`);

ALTER TABLE `program_participants` ADD CONSTRAINT `program_participants_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

ALTER TABLE `external_books` ADD CONSTRAINT `external_books_ibfk_1` FOREIGN KEY (`id`) REFERENCES `books` (`id`);
