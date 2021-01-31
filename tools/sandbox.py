from app import db, app
import app.blueprints.printing.models as printModels
x = db.session.query(printModels.PrintOrder)

print(x)
