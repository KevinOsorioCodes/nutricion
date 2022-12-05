module.exports = {
    apps : [{
       name : "Not oficial",
       script: 'manage.py',
       args: 'runserver 172.31.6.17:7001 --insecure',
       interpreter: 'python3',
    }]
  }