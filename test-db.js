const { Client } = require('pg');
require('dotenv').config({ path: 'n8n/.env' });

const client = new Client({
  host: process.env.DB_POSTGRESDB_HOST,
  port: 5432, // Test session port
  user: process.env.DB_POSTGRESDB_USER,
  password: process.env.DB_POSTGRESDB_PASSWORD,
  database: process.env.DB_POSTGRESDB_DATABASE,
});

client.connect()
  .then(() => {
    console.log('Connected natively to PostgreSQL');
    return client.end();
  })
  .catch(err => console.error('Connection error', err.stack));
