{
  "version": 2,
  "builds": [
    {
      "src": "e/wsgi.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "e/wsgi.py"
    }
  ],
  "env": {
    "SECRET_KEY": "secret123",
    "DEBUG": "False"
  }
}