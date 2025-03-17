# Database Documentation

## Overview

The Gulf South Platform uses MySQL 8.0+ as its database, with SQLAlchemy ORM for database operations. The database is configured to use UTF-8 character encoding for proper handling of special characters and emojis.

## Database Configuration

```python
# Database connection settings
DB_HOST=localhost
DB_USER=gulf_south_user
DB_PASSWORD=your_password
DB_NAME=gulf_south_platform

# Character set and collation
CHARACTER_SET=utf8mb4
COLLATION=utf8mb4_unicode_ci
```

## Schema

### Users Table
```sql
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    is_active BOOLEAN DEFAULT TRUE,
    is_superuser BOOLEAN DEFAULT FALSE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX ix_users_email (email),
    INDEX ix_users_id (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

### Conversations Table
```sql
CREATE TABLE conversations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user1_id INT NOT NULL,
    user2_id INT NOT NULL,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user1_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (user2_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX ix_conversations_user1_id (user1_id),
    INDEX ix_conversations_user2_id (user2_id),
    INDEX ix_conversations_id (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

### Messages Table
```sql
CREATE TABLE messages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    conversation_id INT NOT NULL,
    sender_id INT NOT NULL,
    content TEXT NOT NULL,
    read BOOLEAN DEFAULT FALSE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE,
    FOREIGN KEY (sender_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX ix_messages_conversation_id (conversation_id),
    INDEX ix_messages_sender_id (sender_id),
    INDEX ix_messages_id (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

### Notifications Table
```sql
CREATE TABLE notifications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    type VARCHAR(50) NOT NULL,
    message VARCHAR(255) NOT NULL,
    data JSON,
    read BOOLEAN DEFAULT FALSE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX ix_notifications_user_id (user_id),
    INDEX ix_notifications_id (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

## Relationships

### User Relationships
- A user can have multiple conversations (as user1 or user2)
- A user can send multiple messages
- A user can have multiple notifications

### Conversation Relationships
- A conversation belongs to two users (user1 and user2)
- A conversation can have multiple messages

### Message Relationships
- A message belongs to one conversation
- A message has one sender (user)

### Notification Relationships
- A notification belongs to one user

## Indexes

The following indexes are created for optimal query performance:

1. Users Table:
   - `ix_users_email`: For fast email lookups
   - `ix_users_id`: For fast user ID lookups

2. Conversations Table:
   - `ix_conversations_user1_id`: For fast user1 lookups
   - `ix_conversations_user2_id`: For fast user2 lookups
   - `ix_conversations_id`: For fast conversation ID lookups

3. Messages Table:
   - `ix_messages_conversation_id`: For fast conversation message lookups
   - `ix_messages_sender_id`: For fast sender lookups
   - `ix_messages_id`: For fast message ID lookups

4. Notifications Table:
   - `ix_notifications_user_id`: For fast user notification lookups
   - `ix_notifications_id`: For fast notification ID lookups

## Character Set and Collation

The database uses UTF-8 (utf8mb4) character set with case-insensitive collation (utf8mb4_unicode_ci) to support:
- Full Unicode character set
- Emojis and special characters
- Case-insensitive searches
- Proper sorting of international characters

## Backup and Recovery

### Backup
```bash
mysqldump -u gulf_south_user -p gulf_south_platform > backup.sql
```

### Recovery
```bash
mysql -u gulf_south_user -p gulf_south_platform < backup.sql
```

## Maintenance

### Optimize Tables
```sql
OPTIMIZE TABLE users, conversations, messages, notifications;
```

### Analyze Tables
```sql
ANALYZE TABLE users, conversations, messages, notifications;
```

### Check Tables
```sql
CHECK TABLE users, conversations, messages, notifications;
``` 