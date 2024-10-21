from shop import app,db
from dotenv import load_dotenv
import os
load_dotenv()

if __name__ == "__main__":
    
    with app.app_context():
        db.create_all()
        
    app.run(debug=os.getenv('FLASK_DEBUG')=='1')
    

