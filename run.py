from app import app

env = app.config['ENVIRONMENT']['flask']
app.run(host=env['host'], port=env['port'], debug=True)