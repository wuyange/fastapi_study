from app import creat_app

app = creat_app()

if __name__ == "__main__":
    import uvicorn
    import os
    app_modeel_name = os.path.basename(__file__).replace(".py", "")
    uvicorn.run(f"{app_modeel_name}:app", host='127.0.0.1', port=80, reload=True, workers=4)
