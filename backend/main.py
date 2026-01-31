from src import app, create_default_admin, db, celery

if __name__=="__main__":
    with app.app_context():
        import src.models
        db.create_all()
        print("===========================")
        print("Database initialized!")
        print("===========================")
        print()
        create_default_admin()
    app.run(debug=True, host="0.0.0.0")