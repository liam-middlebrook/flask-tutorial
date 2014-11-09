from tutorial.site import app

if __name__ == "__main__":
    app.debug = True
    app.run(threaded=True)
