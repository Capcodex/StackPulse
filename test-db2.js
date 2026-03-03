const { Client } = require('pg');

const client = new Client({
  host: 'db.gxuoceuryofmiuyrkmfn.supabase.co',
  port: 5432,
  user: 'postgres',
  password: 'tEGkwqdLfKIpIfXL',
  database: 'postgres',
});

client.connect()
  .then(() => {
    console.log('Connected directly to PostgreSQL (IPv6)');
    return client.query('SELECT 1 as val');
  })
  .then(res => {
    console.log('Query success:', res.rows);
    return client.end();
  })
  .catch(err => {
    console.error('Connection error', err.message);
    process.exit(1);
  });
