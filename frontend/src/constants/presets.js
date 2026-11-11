export const PRESETS = {
  normal: {
    duration: 1.5,
    src_bytes: 1040,
    dst_bytes: 4200,
    failed_logins: 0,
    same_srv_rate: 1.0,
    serror_rate: 0.0,
    flag: 'SF',
    payload: 'GET /index.html HTTP/1.1'
  },
  syn_flood: {
    duration: 0.0,
    src_bytes: 0,
    dst_bytes: 0,
    failed_logins: 0,
    same_srv_rate: 0.05,
    serror_rate: 0.95,
    flag: 'S0',
    payload: ''
  },
  brute_force: {
    duration: 12.0,
    src_bytes: 450,
    dst_bytes: 120,
    failed_logins: 6,
    same_srv_rate: 0.8,
    serror_rate: 0.0,
    flag: 'SF',
    payload: 'POST /api/login - admin/password123'
  },
  sqli: {
    duration: 0.8,
    src_bytes: 2300,
    dst_bytes: 800,
    failed_logins: 0,
    same_srv_rate: 1.0,
    serror_rate: 0.0,
    flag: 'SF',
    payload: "SELECT * FROM users WHERE id = 1 UNION SELECT username, password FROM accounts;"
  }
};

export const ENGINES = [
  { id: 'compare', label: 'All Engines (Compare)' },
  { id: 'rule', label: 'Rule-Based' },
  { id: 'ml', label: 'Machine Learning' },
  { id: 'dl', label: 'Deep Learning' }
];