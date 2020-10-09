from sanic import Sanic, Blueprint
from sanic.response import text, html, json, file, file_stream
from aiofiles import os as async_os

app = Sanic("App Name")

blueprint = Blueprint("name", url_prefix="/react")

""" Respond with plain text """
@app.route("/text")
async def respond_plain_text(request):
    return text("Hello world!")

""" Respond with json """
@app.route("/json")
async def respond_json(request):
    return json({"yolo": "yikes"})

# """ Respond with react template """
# @app.route("/")
# async def respond_react(request):
#     # Where does it take the javascript and css from?
#     return await file("./build/index.html")

""" Respond with html """
@app.route("/html")
async def respond_html(request):
    # Where does it take the javascript and css from?
    return html('<p>Hello world!</p>')

""" Respond with file """
@app.route("/file")
async def respond_html(request):
    return await file('files/example_image.png')

""" Respond with file streaming """
@app.route("/file_streaming")
async def respond_html(request):
    file_path = 'files/example_image.png'
    file_stat = await async_os.stat(file_path)
    headers = {"Content-Length": str(file_stat.st_size)}

    return await file_stream(
        file_path,
        headers=headers,
        chunked=False,
    )


app.blueprint(blueprint)
app.static("/", "./build/index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)

