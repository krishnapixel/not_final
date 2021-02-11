import bottle
import appcode

@bottle.route("/")
def any_name():
  return bottle.static_file("index.html", root="")

@bottle.route("/plots.js")
def second():
  return bottle.static_file("plots.js", root="")

@bottle.route("/permitsByMonth")
def barGraph():
    return appcode.permitsByMonth()

@bottle.route("/permitsByYear")
def linegraph():
    return appcode.permitsByYear()

'''@bottle.route("/permitsScatter")
def scatterGraph():
    return appcode.permitsScatter()'''

bottle.run(host="0.0.0.0", port=8080, debug=True)