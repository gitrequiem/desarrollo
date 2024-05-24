class Config:
    # Configuración de la base de datos
    SQLALCHEMY_DATABASE_URI = 'mysql://api_requiem:api_requiem@localhost:3306/api_requiem'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
